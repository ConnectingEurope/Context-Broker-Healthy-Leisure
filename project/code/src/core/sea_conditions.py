import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.aemet_requests as aemet_request
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
list_sub_parameters_elastic= config.sc_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Sea in the CB
def execute_sea_conditions(service_name, device_id):
    method_name = 'execute_sea_conditions'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_sc_aemet = config.sensor_info[device_id]["id"]
    id_aemet_beach = config.sensor_info[device_id]["idAEMET"]
    beach_name = config.sensor_info[device_id]["name"]
    general_latitude = config.sensor_info[device_id]["latitude"]
    general_longitude = config.sensor_info[device_id]["longitude"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request information to AEMET for the sea conditions
    json_aemet_sea_conditions_beach = aemet_request.request_beach_info(id_aemet_beach)
    received_datetime_aemet = generate.convert_datetime_aemet(json_aemet_sea_conditions_beach["elaborado"])
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(region_name, beach_name.replace(' ', '-').replace(',', '-'), id_sc_aemet))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME FOR BEACH {0}, NO PUBLISH".format(beach_name))
    else:
        #Create class: SeaConditions with all constant parameters
        sea_conditions_beach = classes.SeaConditionsGeneral(id_sc_aemet, beach_name, region_name, country_info, general_latitude, general_longitude)
        #Generate dictionary for the request
        dict_sea_conditions_beach = sea_conditions_beach.__dict__
        #Format new parameter values to python class
        dict_data_model_sea_beach = format_data.format_sea_conditions(dict_sea_conditions_beach, json_aemet_sea_conditions_beach)
        
        list_dicts = [dict_data_model_sea_beach]

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

# Functions that create/update the information of Sea in the CB
def execute_sea_conditions_local(service_name, device_id):
    method_name = 'execute_sea_conditions_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_sc_aemet = config.sensor_info[device_id]["id"]
    id_aemet_beach = config.sensor_info[device_id]["idAEMET"]
    beach_name = config.sensor_info[device_id]["name"]
    general_latitude = config.sensor_info[device_id]["latitude"]
    general_longitude = config.sensor_info[device_id]["longitude"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request information to AEMET for the sea conditions
    json_aemet_sea_conditions_beach = aemet_request.request_beach_info(id_aemet_beach)
    received_datetime_aemet = generate.convert_datetime_aemet(json_aemet_sea_conditions_beach["elaborado"])
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(region_name, beach_name.replace(' ', '-').replace(',', '-'), id_sc_aemet))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME FOR BEACH {0}, NO PUBLISH".format(beach_name))
    else:
        #Create class: SeaConditions with all constant parameters
        sea_conditions_beach = classes.SeaConditionsGeneral(id_sc_aemet, beach_name, region_name, country_info, general_latitude, general_longitude)
        #Generate dictionary for the request
        dict_sea_conditions_beach = sea_conditions_beach.__dict__
        #Format new parameter values to python class
        dict_data_model_sea_beach = format_data.format_sea_conditions(dict_sea_conditions_beach, json_aemet_sea_conditions_beach)
        
        list_dicts = [dict_data_model_sea_beach]

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

def execute_sea_random_conditions(service_name, date_observed, device_id):
    method_name = 'execute_sea_random_conditions'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_sc_aemet = config.sensor_info[device_id]["id"]
    beach_name = config.sensor_info[device_id]["name"]
    general_latitude = config.sensor_info[device_id]["latitude"]
    general_longitude = config.sensor_info[device_id]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #RANDOM FOR HISTORICAL DATA
    #Fake request information to AEMET for the sea conditions
    wave_level_beach = generate.generate_wave_level(310)
    sea_temperature_beach = generate.generate_sea_temperature_random(date_observed)

    #Create class: sea_conditions with all constant parameters
    sea_conditions_beach = classes.SeaConditionsGeneral(id_sc_aemet, beach_name, region_name, country_info, general_latitude, general_longitude)
    
    #Generate dictionary for the request
    dict_sea_conditions_beach = sea_conditions_beach.__dict__

    #Format aemet information to data model
    dict_data_model_sea_beach = format_data.format_random_sea_conditions(dict_sea_conditions_beach, string_date_observed, wave_level_beach, sea_temperature_beach)
    
    list_dicts = [dict_data_model_sea_beach]
    
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