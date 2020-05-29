import GetOldTweets3 as got
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
stopWords = set(stopwords.words('english'))

import re


def getkeywordCount(tweet):
    # Remove non alphanumeric characters
    tweet = re.sub(r'[^\w]', ' ', tweet)
    # make tokens
    wordTokens = word_tokenize(tweet)
    # remove stopwords &
    # perform lemmatisation
    lemmatizer = WordNetLemmatizer()
    filtered = [
        lemmatizer.lemmatize(w) for w in wordTokens if not w in stopWords
    ]
    # tag parts of speech
    tagged = nltk.pos_tag(filtered)
    keywords = [w[0] for w in tagged if w[1][0] in ["N", "J", "V", "R"]]
    return len(keywords)


def getTopTweets(username, startDate, endDate, noTopTweets=5):
    # Scrap Tweets
    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(
        startDate).setUntil(endDate)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    df = pd.DataFrame([tweet.__dict__ for tweet in tweets])
    originalDF = df

    df = df.drop(["username", "id", "author_id", "formatted_date"], axis=1)

    # Get keyword count
    df['keywordCount'] = df.apply(lambda x: getkeywordCount(x["text"]), axis=1)

    # Normalize counts
    for feature in ["retweets", "favorites", "replies", 'keywordCount']:
        df[feature + "NormalisedCount"] = df[feature] / (
            df[feature].max())  #-df[feature].min())

    # ## Find out if the tweet is a retweet to some other persons tweet
    # #### We do this because retweeted tweets get a far greater reach and thus skews the scores
    df["ifTo"] = df.apply(lambda x: 0.6 if x["to"] else 1, axis=1)

    ## Get time elapsed since every tweet.
    ### We hypothise that older tweets get more exposure
    df["formatted_date"] = df.apply(
        lambda x: x["formatted_date"][:-10] + x["formatted_date"][-4:], axis=1)
    df["timeElapsedHours"] = df.apply(
        lambda x: (pd.Timestamp(endDate) - pd.to_datetime(x["formatted_date"])
                   ).total_seconds() // 3600,
        axis=1)
    df["timeElapsedScore"] = 1 + 0.04 * (7 * 12 -
                                         df["timeElapsedHours"]) / 7 / 24

    # ## Assign Score to tweet on basis of normalised count of retweets, favorites, replies and keyword count
    df["score"] = (1.5 * df["retweetsNormalisedCount"] +
                   1.2 * df["repliesNormalisedCount"] +
                   1 * df["favoritesNormalisedCount"] + 2 *
                   df["keywordCount"]) * df["ifTo"] * df["timeElapsedScore"]
    sortedDF = df.sort_values(by=['score'], inplace=False, ascending=False)

    return sortedDF.head(noTopTweets)


if __name__ == '__main__':
    username = '@JoeBiden'
    startDate = "2020-05-07"
    endDate = "2020-05-18"

    topN = getTopTweets(username, startDate, endDate, noTopTweets=5)