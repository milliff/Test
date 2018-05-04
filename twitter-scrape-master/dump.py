import settings
import tweepy
from datafreeze import freeze
from textblob import TextBlob
import dataset

db = dataset.connect(settings.CONNECTION_STRING)

result = db[settings.TABLE_NAME].all()
freeze(result, format='csv', filename=settings.CSV_NAME)
