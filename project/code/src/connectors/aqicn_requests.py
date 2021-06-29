import connectors.opendata_connector as connector
import config.config as cnf
config = cnf.Config()

AQICN_API_KEY=config.aqicn_api_key
AQICN_BASE_URI=config.aqicn_base_uri
SOURCE='AQICN'

# Functions that request weather information from AQICN api
def request_data_aqi(city):
	uri = AQICN_BASE_URI + '/feed/' + city + '/?token=' + AQICN_API_KEY
	data = connector.request_data(uri,SOURCE)
	print(data)
    
