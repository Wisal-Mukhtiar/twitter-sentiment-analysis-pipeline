import pandas as pd
import numpy as np


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing tweets
    """

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])
        # can add other attributes of tweets to the df as follows once the df is created
        df['id'] = np.array([tweet.id for tweet in tweets])

        return df
