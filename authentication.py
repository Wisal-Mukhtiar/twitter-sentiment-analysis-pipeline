from tweepy import OAuthHandler

import twitter_credentials


class TwitterAuthenticator():
    """
    class to authenticate the account
    """

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_SECRET)
        return auth
