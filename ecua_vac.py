import tweepy
import time
import pandas as pd

from auth import consumer_key,consumer_secret,key,secret

# twitter auth process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

# import data from github re
df=pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/vacunas/vacunas.csv")

# defining variables
# interval = 60 * 60 * 24  # every 24 hours
interval = 5  # every 5 seconds, for testing
lim_dias=135
vaxs_1dosis=df["primera_dosis"].iloc[-1]
vaxs_2dosis=df["segunda_dosis"].iloc[-1]
left_2_vax= int(9e6-vaxs_1dosis)
fecha_rep=df["fecha"].iloc[-1]
count=1

while True:
    print('A Guillermo Lasso le quedan {} dias para vacunar {} de personas. Hasta el {} el MSP ha reportado {} personas vacunadas con 1 dosis y {} de personas con segunda dosis. Su ofrecimiento en campaña: 9M de vacunadxs en 100 dias'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
    api.update_status('A Guillermo Lasso le quedan {} dias para vacunar {} de personas. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis y {} de personas con segunda dosis. Su ofrecimiento en campaña: 9M de vacunadxs en 100 dias #accountabilitybot #AI4good'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
    lim_dias -= 1
    count +=1
    time.sleep(interval)
