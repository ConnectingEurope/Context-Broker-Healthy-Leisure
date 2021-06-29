
import pytz
import requests
import datetime
import time
import random
import base64
import os
from pathlib import Path

import config.config as cnf
import connectors.orion_connector as orion
import utils.generate_information as generate
import core.nereo_classes as classes
import core.bikelane_conditions as bike
import core.beach_conditions as beach
import core.sea_conditions as sea
import core.weather_observed_aemet as weather
import core.pred_beach_conditions as pred_beach
import core.walking_routes as walking
import core.air_quality_observed_temp as air_quality_temp
import core.air_quality_observed_airquality as air_quality_aqi
import connectors.aemet_requests as aemet_request
import connectors.mysql_connector as mysql

config = cnf.Config()
CB_URI = config.context_broker_uri
SUBS_URI = config.subscription_uri
ID_CITY_BENIDORM = config.id_aemet_benidorm

def format_environment_airquality_sensor(object_environment_conditions, id_sensor, measured_datetime):
    datetime_measurement, air_quality_index = generate.generate_air_quality_index_random()
    object_environment_conditions.airQualityIndex = air_quality_index
    object_environment_conditions.airQualityLevel = generate.generate_air_quality_index(air_quality_index)
    object_environment_conditions.dateObserved = measured_datetime
    object_environment_conditions.dataProvider = id_sensor

    return object_environment_conditions
def format_environment_temperature_humidity_sensor(object_environment_conditions, id_sensor, measured_datetime):
	object_sea_conditions.source = "http://www.aemet.es"
	object_sea_conditions.dateObserved = string_measured_datetime
	object_sea_conditions.waveLevel = generate.generate_wave_level(310)
	object_sea_conditions.surfaceTemperature = generate.generate_sea_temperature_random(datetime_measured_datetime)
		
	return object_sea_conditions
def delete_data(list_services):
    for service_name in list_services:
        print(service_name)
        list_response = orion.delete_data(CB_URI, service_name)
        for response in list_response:
            print(response.status_code)
            #print(response.content)

        list_response = orion.delete_data(SUBS_URI, service_name)
        for response in list_response:
            print(response.status_code)
            #print(response.content)       
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

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        air_quality_aqi.execute_air_quality_observed_airquality(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)
        time.sleep(1)

def generate_recommender_historical_data():
    print("GG")

def generate_notifications_historical_data():
    print("GG")

if __name__ == "__main__":
    '''list_services = [  'bikelaneconditions', 
                       'beachconditions', 
                       'beachpredictions', 
                       'seaconditions', 
                       'walkingroutes',
                       'bikelaneconditions', 
                       'airqualityobservedtemp',
                       'airqualityobservedairquality',
                       'weatherobservedaemet']'''
    list_services = ['airqualityobservedairquality']
    #delete_data(list_services)

    generate_beach_historical_data()
    generate_beach_prediction_historical_data()
    generate_bikelane_historical_data()
    generate_sea_historical_data()
    generate_walking_routes_historical_data()
    generate_weather_observed_historical_data()
    generate_air_quality_temp_historical_data()
    generate_air_quality_aqi_historical_data()
    
    
    




