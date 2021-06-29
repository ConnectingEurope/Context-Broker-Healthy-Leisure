import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed(service_name, date_observed, device_id, dict_data):
    method_name = 'execute_air_quality_observed'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    id_aqi = config.sensor_info[device_id]["id"]
    aqi_name = config.sensor_info[device_id]["name"]
    aqi_description = config.sensor_info[device_id]["description"]
    general_latitude = config.sensor_info[device_id]["latitude"]
    general_longitude = config.sensor_info[device_id]["longitude"]
    list_sub_parameters_elastic = config.aqo_general_subs

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQuaityObserved
    air_quality_observed_class = classes.AirQualityObservedGeneral(id_aqi, region_name, country_info, aqi_name, aqi_description, general_latitude, general_longitude)
    
    #for key in dict_data:
    #    list_sub_parameters_elastic.append(key)

    #print(list_sub_parameters_elastic)

    #Generate dictionaries for the request
    dict_air_quality_observed = air_quality_observed_class.__dict__

    #Format new parameter values to python class
    dict_data_model_air_quality_observed = format_data.format_air_quality_observed_general(dict_air_quality_observed, string_date_observed, dict_data)
    
    list_dicts = [dict_data_model_air_quality_observed]

    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''

    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed_local(service_name, date_observed, device_id, dict_data):
    method_name = 'execute_air_quality_observed_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    id_aqi = config.sensor_info[device_id]["id"]
    aqi_name = config.sensor_info[device_id]["name"]
    aqi_description = config.sensor_info[device_id]["description"]
    general_latitude = config.sensor_info[device_id]["latitude"]
    general_longitude = config.sensor_info[device_id]["longitude"]
    list_sub_parameters_elastic = config.aqo_general_subs

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQuaityObserved
    air_quality_observed_class = classes.AirQualityObservedGeneral(id_aqi, region_name, country_info, aqi_name, aqi_description, general_latitude, general_longitude)
    
    for key in dict_data:
        list_sub_parameters_elastic.append(key)

    #Generate dictionaries for the request
    dict_air_quality_observed = air_quality_observed_class.__dict__

    #Format new parameter values to python class
    dict_data_model_air_quality_observed = format_data.format_air_quality_observed_general(dict_air_quality_observed, string_date_observed, dict_data)
    
    list_dicts = [dict_data_model_air_quality_observed]

    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_aqi_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''

    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)