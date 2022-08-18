import pandas as pd


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing tweets
    """

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])

        return df
