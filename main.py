from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API

from authentication import TwitterAuthenticator


class TwitterClient():

    def __init__(self, twitter_user):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweet(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, user_id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


class StdOutListener(Stream):

    """
    base class processing the data and errors 

    """

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, fetched_tweets_filename):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'ab') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print(f"Error on data {str(e)}")
        return True

    def on_error(self, status):
        # the status is returned when an app is rate limited for making too many requests.
        if status == 402:
            return False  # shuts the connection

        print(status)


class TwitterStream():
    """ 
    class for processing tweets: connection to API via Stream

    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, key_word_list):
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = StdOutListener(auth.consumer_key, auth.consumer_secret,
                                auth.access_token, auth.access_token_secret, fetched_tweets_filename)
        stream.filter(track=key_word_list)


if __name__ == "__main__":
    key_word_list = ['United States', 'Russia', 'Ukraine']
    fetched_tweets_filename = 'fetched_tweets.json'

    # twitter_streamer = TwitterStream()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, key_word_list)

    twitter_client = TwitterClient('Pycon')
    print(twitter_client.get_user_timeline_tweet(1))
