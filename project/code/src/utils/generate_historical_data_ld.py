import pytz
import datetime
import time
import base64
import os
from pathlib import Path

import core.bikelane_conditions as bike
import core.beach_conditions as beach
import core.sea_conditions as sea
import core.weather_observed_aemet as weather
import core.pred_beach_conditions as pred_beach
import core.walking_routes as walking
import core.air_quality_observed_temp as air_quality_temp
import core.air_quality_observed_airquality as air_quality_aqi


def get_base64_encoded_image(image_path):
    print(Path(image_path))
    print(repr(image_path))
    print(type(image_path))
    print("file: {0}".format(os.path.isfile(Path(image_path))))
    print("directory: {0}".format(os.path.isdir(image_path)))

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def generate_bikelane_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name = 'bikelaneconditions'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        bike.execute_bikelane_conditions(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)

def generate_beach_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name = 'beachconditions'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        beach.execute_beach_conditions(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)

def generate_beach_prediction_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name = 'beachpredictions'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        pred_beach.execute_beach_conditions_pred(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=24)

def generate_sea_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name = 'seaconditions'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        sea.execute_sea_random_conditions(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=2)

def generate_weather_observed_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = 'weatherobservedaemet'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        weather.execute_random_weather_observed_aemet(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=2)

def generate_walking_routes_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = 'walkingroutes'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        walking.execute_walking_routes(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=24)

def generate_air_quality_temp_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = 'airqualityobservedtemp'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        air_quality_temp.execute_air_quality_observed_temp(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)

def generate_air_quality_aqi_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = 'airqualityobservedairquality'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        air_quality_aqi.execute_air_quality_observed_airquality(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)
        time.sleep(1)

if __name__ == "__main__":
    generate_beach_historical_data()
    generate_beach_prediction_historical_data()
    generate_bikelane_historical_data()
    generate_sea_historical_data()
    generate_walking_routes_historical_data()
    generate_weather_observed_historical_data()
    generate_air_quality_temp_historical_data()
    generate_air_quality_aqi_historical_data()
    
    
    




