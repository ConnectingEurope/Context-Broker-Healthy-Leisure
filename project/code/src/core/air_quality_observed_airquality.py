import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
API_NOTIFY_URI = config.api_notify_uri
region_name = config.region
country_info = config.country
notify_elastic = True
notify_api = True
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed_airquality_random(service_name, date_observed):
    method_name = 'execute_air_quality_observed_airquality_random'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    id_aqi = config.sensor_info["011"]["id"]
    aqi_name = config.sensor_info["011"]["name"]
    aqi_description = config.sensor_info["011"]["description"]
    general_latitude = config.sensor_info["011"]["latitude"]
    general_longitude = config.sensor_info["011"]["longitude"]
    list_sub_parameters_elastic = config.aqo_aqi_elastic_subs
    list_sub_parameters_api = config.aqo_aqi_api_subs

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQuaityObserved
    air_quality_observed_benidorm = classes.AirQualityObservedGeneralAQI(id_aqi, region_name, country_info, aqi_name, aqi_description, general_latitude, general_longitude)
    
    #Generate random values for pm10, pm25
    data_pm10 = generate.generate_random_pm10(date_observed)
    data_pm25 = generate.generate_random_pm25(date_observed)

    air_quality_agents = ['pm10', 'pm25']
    air_quality_values = [data_pm10, data_pm25]

    #Generate dictionaries for the request (could be a for)
    dict_air_quality_observed = air_quality_observed_benidorm.__dict__

    #Format new parameter values to python class
    dict_data_model_air_quality_observed = format_data.format_air_quality_observed_airquality_sensor(dict_air_quality_observed, string_date_observed, air_quality_agents, air_quality_values)
    
    list_dicts = [dict_data_model_air_quality_observed]
    #print(dict_air_quality_observed_benidorm)
    #Publish payloads
    #Create the necessary subscriptions
    notify_aqi_api = API_NOTIFY_URI + 'index/aqi'
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_aqi_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_aqi_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, notify_aqi_api)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed_airquality(service_name, date_observed):
    method_name = 'execute_air_quality_observed_airquality_random'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    id_aqi = config.sensor_info["011"]["id"]
    aqi_name = config.sensor_info["011"]["name"]
    aqi_description = config.sensor_info["011"]["description"]
    general_latitude = config.sensor_info["011"]["latitude"]
    general_longitude = config.sensor_info["011"]["longitude"]
    list_sub_parameters_elastic = config.aqo_aqi_elastic_subs
    list_sub_parameters_api = config.aqo_aqi_api_subs

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQuaityObserved
    air_quality_observed_benidorm = classes.AirQualityObservedGeneralAQI(id_aqi, region_name, country_info, aqi_name, aqi_description, general_latitude, general_longitude)
    
    #Generate random values for pm10, pm25
    data_pm10 = 0
    data_pm25 = 0

    air_quality_agents = ['pm10', 'pm25']
    air_quality_values = [data_pm10, data_pm25]

    #Generate dictionaries for the request (could be a for)
    dict_air_quality_observed = air_quality_observed_benidorm.__dict__

    #Format new parameter values to python class
    dict_data_model_air_quality_observed = format_data.format_air_quality_observed_airquality_sensor(dict_air_quality_observed, string_date_observed, air_quality_agents, air_quality_values)
    
    list_dicts = [dict_data_model_air_quality_observed]
    #print(dict_air_quality_observed_benidorm)
    #Publish payloads
    #Create the necessary subscriptions
    notify_aqi_api = API_NOTIFY_URI + 'index/aqi'
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_aqi_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_aqi_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, notify_aqi_api)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed_airquality_local(service_name, date_observed):
    method_name = 'execute_air_quality_observed_airquality_random'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    id_aqi = config.sensor_info["011"]["id"]
    aqi_name = config.sensor_info["011"]["name"]
    aqi_description = config.sensor_info["011"]["description"]
    general_latitude = config.sensor_info["011"]["latitude"]
    general_longitude = config.sensor_info["011"]["longitude"]
    list_sub_parameters_elastic = config.aqo_aqi_elastic_subs
    list_sub_parameters_api = config.aqo_aqi_api_subs

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQuaityObserved
    air_quality_observed_benidorm = classes.AirQualityObservedGeneralAQI(id_aqi, region_name, country_info, aqi_name, aqi_description, general_latitude, general_longitude)
    
    #Generate random values for pm10, pm25
    data_pm10 = 0
    data_pm25 = 0

    air_quality_agents = ['pm10', 'pm25']
    air_quality_values = [data_pm10, data_pm25]

    #Generate dictionaries for the request (could be a for)
    dict_air_quality_observed = air_quality_observed_benidorm.__dict__

    #Format new parameter values to python class
    dict_data_model_air_quality_observed = format_data.format_air_quality_observed_airquality_sensor(dict_air_quality_observed, string_date_observed, air_quality_agents, air_quality_values)

    list_dicts = [dict_data_model_air_quality_observed]
    #print(dict_air_quality_observed_benidorm)
    #Publish payloads
    #Create the necessary subscriptions
    notify_aqi_api = API_NOTIFY_URI + 'index/aqi'
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_aqi_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_aqi_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, notify_aqi_api)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)