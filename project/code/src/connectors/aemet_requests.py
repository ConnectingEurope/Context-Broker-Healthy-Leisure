import connectors.opendata_connector as connector
import config.config as cnf
config = cnf.Config()

AEMET_API_KEY=config.aemet_api_key
BEACH_INFO_BASE_URI=config.aemet_beachinfo_base_uri
WEATHER_DAILY_BASE_URI=config.aemet_city_weather_prediction_daily_base_uri
SOURCE='AEMET'

# Functions that request beach information from AEMET
def request_beach_info(id_beach):
	uri = BEACH_INFO_BASE_URI + id_beach + '/?api_key=' + AEMET_API_KEY
	data = connector.request_data(uri,SOURCE)
	beach_conditions = data[0]

	return beach_conditions

# Functions that request weather information from AEMET
def request_weather_info(id_city):
	uri = WEATHER_DAILY_BASE_URI + id_city + '/?api_key=' + AEMET_API_KEY
	data = connector.request_data(uri,SOURCE)
	weather_conditions = data[0]
	
	return weather_conditions
    
