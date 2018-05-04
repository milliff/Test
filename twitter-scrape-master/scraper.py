# -*- coding: utf-8 -*-
import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import pandas as pd
from datetime import datetime

#db = dataset.connect(settings.CONNECTION_STRING)

all_tweets = []
tweet_count = 0
class StreamListener(tweepy.StreamListener):

    #def __init__(self):
    #    print(self.api)
    #    self.all_tweets = []

    def on_status(self, status):
        if status.retweeted:
            return
        global tweet_count
        tweet_count += 1
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        #table = db[settings.TABLE_NAME]
        try:
            global all_tweets
            all_tweets.append({
                 "user_description":description,
                 "user_location":loc,
                 "coordinates":coords,
                 "text":text,
                 "geo":geo,
                 "user_name":name,
                 "user_created":user_created,
                 "user_followers":followers,
                 "id_str":id_str,
                 "created":created,
                 "retweet_count":retweets,
                 "user_bg_color":bg_color,
                 "polarity":sent.polarity,
                 "subjectivity":sent.subjectivity})
            #table.insert(dict(
            #    user_description=description,
            #    user_location=loc,
            #    coordinates=coords,
            #    text=text,
            #    geo=geo,
            #    user_name=name,
            #    user_created=user_created,
            #    user_followers=followers,
            #    id_str=id_str,
            #    created=created,
            #    retweet_count=retweets,
            #    user_bg_color=bg_color,
            #    polarity=sent.polarity,
            #    subjectivity=sent.subjectivity,
            #))
        except ProgrammingError as err:
            print(err)
        if tweet_count > 5000:
            return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
our_api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=our_api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS, languages=['en'])

today = str(datetime.today())
tweets_df = pd.DataFrame(all_tweets)
tweets_df.to_csv("all_tweets_{0}.csv".format(today))

