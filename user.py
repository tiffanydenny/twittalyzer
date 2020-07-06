from database import ConnectionFromPool
import oauth2
from twitter_utils import consumer
import json


class User:
    def __init__(self, username, oauth_token, oauth_token_secret, id):
        self.username = username
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "User: {}".format(self.username)

    def save_to_db(self):
        with ConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users (username, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                           (self.username, self.oauth_token, self.oauth_token_secret))


    @classmethod
    def load_from_db_by_username(cls, username):
        with ConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(username=user_data[1], oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])


    def twitter_request(self, uri, type='GET'):
        # Create authorized token object used to perform Twitter API calls on behalf of user
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make twitter API calls
        response, content = authorized_client.request(uri, type)
        if response.status != 200:
            print("An error occurred while searching.")
        return json.loads(content.decode('utf-8'))

