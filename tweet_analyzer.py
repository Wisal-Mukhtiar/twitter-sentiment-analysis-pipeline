import pandas as pd
import numpy as np


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing tweets
    """

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweet'])
        # can add other attributes of tweets to the df as follows once the df is created
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['likes'] = np.array([self.get_likes(tweet) for tweet in tweets])
        return df

    def get_likes(self, tweet):
        try:
            likes = tweet._json["retweeted_status"]["favorite_count"]
        except KeyError:
            likes = tweet.favorite_count

        return likes
