from tweepy import OAuthHandler
from tweepy import Client
import twitter_credentials


class TwitterAuthenticator():
    """
    class to authenticate the account
    """

    def __init__(self):
        self.auth = auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                                        twitter_credentials.CONSUMER_SECRET)
        self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                                   twitter_credentials.ACCESS_SECRET)

    def authenticate_twitter_app(self):
        return self.auth

    def get_twitter_client(self):
        client = Client(consumer_key=self.auth.consumer_key, consumer_secret=self.auth.consumer_secret,
                        access_token=self.auth.access_token, access_token_secret=self.auth.access_token_secret)
        return client
