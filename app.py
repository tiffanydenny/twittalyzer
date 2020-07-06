from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database
from flask_paginate import Pagination, get_page_parameter
import requests

app = Flask(__name__)
app.secret_key = '1234'

Database.initialize(database='learning', user='postgres', password='Data1234', host='localhost', port=5433)

@app.before_request
def load_user():
    if 'username' in session:
        g.user = User.load_from_db_by_username(session['username'])

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    if 'username' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_username(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['username'] = user.username

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)

@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        search = True
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en+exclude:retweets+exclude:replies&count=100'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    count=0
    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
        count +=1

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=count, search=search, record_name='tweets')

    return render_template('search.html', content=tweet_texts, pagination=pagination)

app.run(port=8910, debug=True)