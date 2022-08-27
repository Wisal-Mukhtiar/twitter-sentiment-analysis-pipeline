import numpy as np
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
from tweepy.pagination import Paginator

from authentication import TwitterAuthenticator
from tweet_analyzer import TweetAnalyzer


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_api_client = API(self.auth)
        self.twitter_user = twitter_user
        self.twitter_client = TwitterAuthenticator().get_twitter_client()

    def get_twitter_client_api(self):
        return self.twitter_api_client

    def get_twitter_client(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_api_client.user_timeline, user_id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_api_client.get_friends).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timline_tweets = []
        for tweet in Cursor(self.twitter_api_client.home_timeline).items(num_tweets):
            home_timline_tweets.append(tweet)
        return home_timline_tweets

    def get_recent_tweets(self, topic, num_tweets):
        recent_tweets = []
        for tweet in Paginator(self.twitter_client.search_recent_tweets, topic,
                               max_results=100, user_auth=True).flatten(num_tweets):
            recent_tweets.append(tweet)
        return recent_tweets

    def get_tweets_by_keywords(self, keywords, num_tweets):
        tweets_by_keywords = []
        for tweet in Cursor(self.twitter_api_client.search_tweets, q=keywords).items(num_tweets):
            tweets_by_keywords.append(tweet)
        return tweets_by_keywords


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
    twitter_client = TwitterClient()
    tweets = twitter_client.get_tweets_by_keywords('Pakistan', 5)

    tweets_analyzer = TweetAnalyzer()
    df = tweets_analyzer.tweets_to_dataframe(tweets)
