from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token


Database.initialize(database='learning', user='postgres', password='Data1234', host='localhost', port=5433)

username = input("Enter your e-mail: ")
user = User.load_from_db_by_username(username)

if not user:
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

