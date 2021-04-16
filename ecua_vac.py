import tweepy
import time

from auth import consumer_key,consumer_secret,key,secret

# interval = 60 * 60 * 24  # every 24 hours
interval = 15  # every 15 seconds, for testing


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


count=1

while True:
    print("this is count number {}".format(count))
    api.update_status('posting from python test tweet {}'.format(count))
    count +=1
    time.sleep(interval)
