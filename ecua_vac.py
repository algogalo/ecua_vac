import tweepy

from auth import consumer_key,consumer_secret,key,secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
api.update_status('posting from python test')
