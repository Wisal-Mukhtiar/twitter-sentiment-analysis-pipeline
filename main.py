from tweepy import OAuthHandler
from tweepy import Stream

from authentication import TwitterAuthenticator


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

    twitter_streamer = TwitterStream()
    twitter_streamer.stream_tweets(fetched_tweets_filename, key_word_list)
