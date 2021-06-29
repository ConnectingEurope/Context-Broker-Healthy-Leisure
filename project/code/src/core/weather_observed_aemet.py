import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.aemet_requests as aemet_request
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
ID_AEMET_CITY_BENIDORM = config.id_aemet_benidorm
NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.wo_aemet_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_weather_observed_aemet(service_name):
    module_name = 'execute_weather_observed_aemet'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_wo = config.sensor_info["001"]["id"]
    name_value = config.sensor_info["001"]["name"]
    value_description = config.sensor_info["001"]["description"]
    general_latitude = config.sensor_info["001"]["latitude"]
    general_longitude = config.sensor_info["001"]["longitude"]
    
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request information to AEMET
    json_aemet_weather_observed_benidorm = aemet_request.request_weather_info(ID_AEMET_CITY_BENIDORM)
    received_datetime_aemet = generate.convert_datetime_aemet(json_aemet_weather_observed_benidorm["elaborado"])
    orion_datetime_payload = ''
    
    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:WeatherObserved:{0}:{1}".format(region_name, id_wo))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Create classes: WeatherObserved
        weather_observed_benidorm = classes.WeatherObservedGeneral(id_wo, region_name, country_info, name_value, value_description, general_latitude, general_longitude)
        
        #Generate dictionaries for the request (could be a for)
        dict_weather_observed_benidorm = weather_observed_benidorm.__dict__

        #Format new parameter values to python class
        dict_data_model_weather_observed_benidorm = format_data.format_weather_observed_aemet(dict_weather_observed_benidorm, json_aemet_weather_observed_benidorm)
        
        list_dicts = [dict_data_model_weather_observed_benidorm]
        
        #Publish payloads
        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ""
                                            
        try:
            orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        except Exception as ex:
            error_text = "Exception in {0}: {1}".format(method_name, ex)
            print(error_text)
    
# Functions that create/update the information of Environment in the CB
def execute_weather_observed_aemet_local(service_name):
    module_name = 'execute_weather_observed_aemet_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_wo = config.sensor_info["001"]["id"]
    name_value = config.sensor_info["001"]["name"]
    value_description = config.sensor_info["001"]["description"]
    general_latitude = config.sensor_info["001"]["latitude"]
    general_longitude = config.sensor_info["001"]["longitude"]
    
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request information to AEMET
    json_aemet_weather_observed_benidorm = aemet_request.request_weather_info(ID_AEMET_CITY_BENIDORM)
    received_datetime_aemet = generate.convert_datetime_aemet(json_aemet_weather_observed_benidorm["elaborado"])
    orion_datetime_payload = ''
    
    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:WeatherObserved:{0}:{1}".format(region_name, id_wo))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Create classes: WeatherObserved
        weather_observed_benidorm = classes.WeatherObservedGeneral(id_wo, region_name, country_info, name_value, value_description, general_latitude, general_longitude)
        
        #Generate dictionaries for the request (could be a for)
        dict_weather_observed_benidorm = weather_observed_benidorm.__dict__

        #Format new parameter values to python class
        dict_data_model_weather_observed_benidorm = format_data.format_weather_observed_aemet(dict_weather_observed_benidorm, json_aemet_weather_observed_benidorm)
        
        list_dicts = [dict_data_model_weather_observed_benidorm]
        
        #Publish payloads
        #Create the necessary subscriptions
        subscription_type = list_dicts[0]["type"]
        subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
        subscription_json_api = ""
                                            
        try:
            orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
        except Exception as ex:
            error_text = "Exception in {0}: {1}".format(method_name, ex)
            print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_random_weather_observed_aemet_random(service_name, date_observed):
    method_name = 'execute_random_weather_observed_aemet_random'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_wo = config.sensor_info["001"]["id"]
    name_value = config.sensor_info["001"]["name"]
    value_description = config.sensor_info["001"]["description"]
    general_latitude = config.sensor_info["001"]["latitude"]
    general_longitude = config.sensor_info["001"]["longitude"]
    
    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }

    #Create classes: WeatherObserved
    weather_observed_benidorm = classes.WeatherObservedGeneral(id_wo, region_name, country_info, name_value, value_description, general_latitude, general_longitude)

    #Generate random values
    temperature = generate.generate_temperature_random(date_observed)
    feel_like_temperature = generate.generate_temperature_random(date_observed)
    relative_humidity = generate.generate_humidity_random(date_observed)
    wind_speed = generate.generate_wind_speed_random(date_observed)
    wind_direction = generate.generate_wind_dir_random()
    weather_type = generate.generate_weather_type_random()

    AEMET_random_data = [string_date_observed, temperature, feel_like_temperature, relative_humidity, wind_speed, wind_direction, weather_type]

    #Generate dictionaries for the request (could be a for)
    dict_weather_observed_benidorm = weather_observed_benidorm.__dict__

    #Format new parameter values to python class
    dict_data_model_weather_observed_benidorm = format_data.format_random_weather_observed_aemet(dict_weather_observed_benidorm, AEMET_random_data)
    
    list_dicts = [dict_data_model_weather_observed_benidorm]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ""
                                         
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)
        
