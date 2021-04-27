import tweepy
import time
import pandas as pd
import datetime
import re

from auth import consumer_key,consumer_secret,key,secret,user_ID

#chequea el numero de caracteres en el tweet. si es muy largo lo corta
def trimtweet(tweet):
    if(len(tweet) <= 280):
         return tweet
    return tweet.substring(0, 277) + "..."

# twitter auth process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)
bot_id = api.me().id #1382664940587261954

# intervalo entre tuits
interval = 60 * 60 * 24  # every 24 hours
# interval = 5  # every 5 seconds, for testing

#define numero de dias hasta el 1 de septiembre
def calc_dias():
    today = datetime.date.today()
    future = datetime.date(2021,9,1)
    diff = future - today
    dias=diff.days
    return  dias

#formatea el numero poniendo un punto entre cada millar
def format_num(num):
    return "{:,}".format(num).replace(',','.')

while True:
    df=pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/vacunas/vacunas.csv")
    fecha_rep=df["fecha"].iloc[-1]
    ult_fecha_datos = datetime.datetime.strptime(df["fecha"].iloc[-1], '%d/%m/%Y')

    #revisa el la fecha de los datos del tweet anterior. notifica si el tuit es repetido.
    lastTweet = api.user_timeline(id = bot_id, count = 1)
    if (len(lastTweet) > 0):
        text = lastTweet[0].text
        m = re.search('Hasta el (?P<date>\d{2}/\d{2}/\d{4}) el MSP', text)
        if m:
            ult_fecha_tweet = datetime.datetime.strptime(m.group('date'), '%d/%m/%Y')
            if ult_fecha_tweet >= ult_fecha_datos:
                mensaje="Ya se tweeteo la ultima fecha disponible fecha {}".format(ult_fecha_datos)
                print(mensaje)
                api.send_direct_message(user_ID, mensaje)
                time.sleep(interval)
                continue

    vaxs_1dosis=df["primera_dosis"].iloc[-1]
    vaxs_2dosis=df["segunda_dosis"].iloc[-1]
    left_2_vax= int(9e6-vaxs_1dosis)
    lim_dias=calc_dias()

    #escenario1 en el que todavia tiene tiempo pero no acaba de vacunar
    if (left_2_vax > 0 and lim_dias > 0):
        tweet= 'A G.Lasso le quedan {} días para vacunar {} personas. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis. Su ofrecimiento en campaña: 9M de vacunadxs en 100 días'
        tweet=tweet.format(lim_dias,format_num(left_2_vax),fecha_rep,format_num(vaxs_1dosis),format_num(vaxs_2dosis))
        tweet=trimtweet(tweet)
        print(tweet, flush=True)
        api.send_direct_message(user_ID, tweet)
        api.update_status(tweet)
        time.sleep(interval)

    #escenario2 en el que se le acabo el tiempo. recordatorio de cuantos dias va sin cumplir so objetivo
    elif (left_2_vax > 0 and lim_dias <= 0):
        tweet='Hace {} días G.Lasso debería haber vacunado 9M de personas y todavia le faltan {} personas para llegar a 9M. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis #accountabilitybot #AI4good'
        print(tweet.format(abs(lim_dias), format_num(left_2_vax), fecha_rep,format_num(vaxs_1dosis),format_num(vaxs_2dosis)),flush=True)
        tweet=tweet.format(abs(lim_dias), format_num(left_2_vax), fecha_rep,format_num(vaxs_1dosis),format_num(vaxs_2dosis))
        tweet=trimtweet(tweet)
        api.send_direct_message(user_ID, tweet)
        api.update_status(tweet)
        time.sleep(interval)

    #escenario3 en el que vacuna a 9M antes de que se acabe el tiempo
    else: #!((a and b) or (a and !b)) = !a
        tweet= 'Guillermo Lasso logró vacunar al menos 9M personas en sus primeros 100 días de gobierno. Voy a buscar algo más que hacer. Chao #accountabilitybot #AI4good'
        tweet = trimtweet(tweet)
        print(tweet,flush=True)
        api.send_direct_message(user_ID,tweet)
        api.update_status(tweet)
        time.sleep(interval)

#to run in the back ground <sudo nohup python3 ecua_vac.py &>
# to check real time log file <sudo tail -f nohup.out>
