import tweepy
import time
import pandas as pd
import datetime

from auth import consumer_key,consumer_secret,key,secret

# twitter auth process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

# import data from github rep
df=pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/vacunas/vacunas.csv")

# defining variables
# interval = 60 * 60 * 24  # every 24 hours
interval = 5  # every 5 seconds, for testing

#define numero de dias hasta el 1 de septiembre
today = datetime.date.today()
future = datetime.date(2021,9,1)
diff = future - today
lim_dias=diff.days


fecha_rep=df["fecha"].iloc[-1]
count=1

while True:
    vaxs_1dosis=df["primera_dosis"].iloc[-1]
    vaxs_2dosis=df["segunda_dosis"].iloc[-1]
    left_2_vax= int(9e6-vaxs_1dosis)
    if left_2_vax > 0:
        print('A Guillermo Lasso le quedan {} dias para vacunar {} personas. Hasta el {} el MSP ha reportado {} personas vacunadas con 1 dosis, {} personas con segunda dosis. Su ofrecimiento en campaña: 9M de vacunadxs en 100 dias'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis),flush=True)
        # api.update_status('A Guillermo Lasso le quedan {} dias para vacunar {} personas. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis. Su ofrecimiento en campaña: 9M de personas vacunadas en 100 dias #accountabilitybot #AI4good'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
        lim_dias -= 1
        count +=1
        time.sleep(interval)
    if left_2_vax <= 0:
        print('Guillermo Lasso logró vacunar al menos 9M personas en sus primeros 100 dias de gobierno. Voy a buscar algo más que hacer. Chao'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis),flush=True)
        # api.update_status('A Guillermo Lasso le quedan {} dias para vacunar {} personas. Hasta el {} el MSP ha reportado {} personas vacunadas con primera dosis, {} personas con segunda dosis. Su ofrecimiento en campaña: 9M de personas vacunadas en 100 dias #accountabilitybot #AI4good'.format(lim_dias, left_2_vax, fecha_rep,vaxs_1dosis,vaxs_2dosis))
        lim_dias -= 1
        count +=1
        time.sleep(interval)

#to run in the back ground <sudo nohup python3 ecua_vac.py &>
# to check real time log file <sudo tail -f nohup.out>

    # if left_2_vax <= 0
        # print("Guillermo Lasso logró vacunar al menos 9M personas en sus primeros 100 dias de gobierno, voy a buscar algo más que hacer".),flush=True)
