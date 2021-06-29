import time

import core.sea_conditions as sea
import core.weather_observed_aemet as woa
import core.walking_routes as wr
import core.bikelane_conditions as bike
import core.beach_conditions as beach
import core.air_quality_observed_airquality as aqi
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

SEA_SERVICE_NAME = config.sea_service
WEATHER_SERVICE_NAME = config.weather_observed_service
WALKING_SERVICE_NAME = config.walking_service
BIKE_LANE_SERVICE_NAME = config.bikelane_service
BEACH_SERVICE_NAME = config.beach_service
AQI_SERVICE = config.aqo_aqi_service
HOUR_TO_PUBLISH = config.hour_to_publish_walking

if __name__ == "__main__":
    seconds_to_wait = 1*60*60 #4h
    print("START - EXECUTION EVERY {0} seconds.".format(seconds_to_wait))

    while True:
        string_datetime_now, date_datetime_now = generate.datetime_time_tz()

        print("{0} {1} 005".format(string_datetime_now, SEA_SERVICE_NAME))
        sea.execute_sea_conditions(SEA_SERVICE_NAME, "005")

        print("{0} {1} 006".format(string_datetime_now, SEA_SERVICE_NAME))
        sea.execute_sea_conditions(SEA_SERVICE_NAME, "006")

        print("{0} {1}".format(string_datetime_now, WEATHER_SERVICE_NAME))
        woa.execute_weather_observed_aemet(WEATHER_SERVICE_NAME)
        
        if date_datetime_now.hour == HOUR_TO_PUBLISH:
            print("{0} {1}".format(string_datetime_now, WALKING_SERVICE_NAME))
            wr.execute_walking_routes_no_occupancy(WALKING_SERVICE_NAME, date_datetime_now)

            print("{0} {1}".format(string_datetime_now, BIKE_LANE_SERVICE_NAME))
            bike.execute_bikelane_conditions(BIKE_LANE_SERVICE_NAME, date_datetime_now, "007", 0)
            bike.execute_bikelane_conditions(BIKE_LANE_SERVICE_NAME, date_datetime_now, "008", 0)
            bike.execute_bikelane_conditions(BIKE_LANE_SERVICE_NAME, date_datetime_now, "009", 0)

            print("{0} {1}".format(string_datetime_now, BEACH_SERVICE_NAME))
            beach.execute_beach_conditions(BEACH_SERVICE_NAME, date_datetime_now, "010", 0)

            print("{0} {1}".format(string_datetime_now, AQI_SERVICE))
            aqi.execute_air_quality_observed_airquality(AQI_SERVICE, date_datetime_now)

        print("SLEEP {0}".format(seconds_to_wait))
        time.sleep(seconds_to_wait)