# pip install - U textblob
# pip install tweepy
# pip install matplotlib

from flask import Flask, render_template, redirect, url_for, request

import pandas as pd
import tweepy
import spacy
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

tweet_ml_data = {}

# function to display data of each tweet , this is the main dictionary for extraction of data .


def printtweetdata(n, ith_tweet):
    tweet_ml_data[ith_tweet[0]] = [ith_tweet[7], ith_tweet[2], '']

# function to perform data extraction


def scrape(words, date_since, numtweet):

    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])

    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search, q=words, lang="en",
                           since=date_since, tweet_mode='extended').items(numtweet)

    # .Cursor() returns an iterable object. Each item in the iterator has various attributes that you can access to  get information about each tweet
    list_tweets = [tweet for tweet in tweets]

    # Counter to maintain Tweet Count
    i = 1

    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet

        # Function call to print tweet data on screen
        printtweetdata(i, ith_tweet)
        i = i+1


if __name__ == '__main__':

    # Enter your own credentials obtained
    # from your developer account
    consumer_key = "8AO6OU5ubyi4XO47b1C7Sjdlz"
    consumer_secret = "FS1usPrfPolvjLXbwGka5N8TWkOZhUsdxGmmTwuO016koesUSt"
    access_key = "1151573806680592384-OUFeUtpsRFZM6jQxl1AG99NEjlY0Kt"
    access_secret = "KKHmkHkDGVaDof8XK4fKKI52DmNl4vZlaXnx85WRfd4Lr"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()
    print("Enter Date since The Tweets are required in yyyy-mm--dd")
    date_since = input()

    # number of tweets you want to extract in one run
    numtweet = 100
    scrape(words, date_since, numtweet)
    print('Scraping has completed!')
negative_list = []
p = []
s = []
su = []
for i in tweet_ml_data:
    j = 0
    polarity = TextBlob(tweet_ml_data[i][0]).sentiment.polarity
    sentiment = TextBlob(tweet_ml_data[i][0]).sentiment
    subjectivity = TextBlob(tweet_ml_data[i][0]).sentiment.subjectivity
    if polarity > 0:
        tweet_ml_data[i][2] = "Positive"
    else:
        tweet_ml_data[i][2] = "Negative"
        negative_list.append(tweet_ml_data[i][0])
        p.append(polarity)
        s.append(sentiment)
        su.append(subjectivity)
print(tweet_ml_data)
x = np.array(p)
y = np.array(su)

plt.scatter(x, y)
plt.show()
