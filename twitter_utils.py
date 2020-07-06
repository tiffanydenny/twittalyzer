import oauth2
import constants
import urllib.parse as urlparse

# Create a consumer that uses the key and secret to ID our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    # client performs requests only
    client = oauth2.Client(consumer)

    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occurred attempting to retrieve request token from Twitter.")

    # Get request token parsing query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # Ask user to auth app and provide PIN
    print("Go to: ")
    print(get_oauth_verifier_url(request_token))

    return input("Enter the PIN: ")

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTH_URL, request_token['oauth_token'])

def get_access_token(request_token, oauth_verifier):
    # Create token object containing request token and verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    # Create client with our consumer(app) and newly verified token
    client = oauth2.Client(consumer, token)
    # Ask Twitter for access token based on verified request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))