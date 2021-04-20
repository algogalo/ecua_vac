import tweepy
import time
import pandas as pd
import datetime

from auth import consumer_key,consumer_secret,key,secret

# twitter auth process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

# defining variables
interval = 60 * 60 * 24  # every 24 hours
# interval = 5  # every 5 seconds, for testing

#define numero de dias hasta el 1 de septiembre
today = datetime.date.today()
future = datetime.date(2021,9,1)
diff = future - today
lim_dias=diff.days

while True:
    df=pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/vacunas/vacunas.csv")
    fecha_rep=df["fecha"].iloc[-1]
    vaxs_1dosis=df["primera_dosis"].iloc[-1]
    vaxs_2dosis=df["segunda_dosis"].iloc[-1]
    left_2_vax= int(9e6-vaxs_1dosis)

    #escenario1 en el que todavia tiene tiempo pero no acaba de vacunar
    if (left_2_vax > 0 and lim_dias > 0):
        tweet='A G.Lasso le quedan {} días para vacunar {} personas. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis. Su ofrecimiento en campaña: 9M de vacunadxs en 100 días'
        print(tweet.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis),flush=True)
        api.update_status(tweet.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
        lim_dias -= 1
        time.sleep(interval)

    #escenario2 en el que se le acabo el tiempo. recordatorio de cuantos dias va sin cumplir so objetivo
    elif (left_2_vax > 0 and lim_dias <= 0):
        tweet='Hace {} días G.Lasso debería haber vacunado 9M de personas y todavia le faltan {} personas para llegar a 9M. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis #accountabilitybot #AI4good'
        print(tweet.format(abs(lim_dias), left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis),flush=True)
        api.update_status(tweet.format(abs(lim_dias), left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
        lim_dias -= 1
        time.sleep(interval)

    #escenario3 en el que vacuna a 9M antes de que se acabe el tiempo
    elif left_2_vax <= 0:
        tweet='Guillermo Lasso logró vacunar al menos 9M personas en sus primeros 100 días de gobierno. Voy a buscar algo más que hacer. Chao #accountabilitybot #AI4good'
        print(tweet,flush=True)
        api.update_status(tweet)
        time.sleep(interval)

#to run in the back ground <sudo nohup python3 ecua_vac.py &>
# to check real time log file <sudo tail -f nohup.out>
