import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import predictive_models.models as pred_mod
import config.config as cnf

config = cnf.Config()

NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.bl_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Bike Lanes in the CB
def execute_bikelane_conditions(service_name, date_observed, bike_lane_id, bike_lane_count):
    method_name = 'execute_bikelane_conditions'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    id_bl = config.sensor_info[bike_lane_id]["id"]
    bike_lane_name = config.sensor_info[bike_lane_id]["name"]
    general_latitude = config.sensor_info[bike_lane_id]["latitude"]
    general_longitude = config.sensor_info[bike_lane_id]["longitude"]
    lane_width = config.sensor_info[bike_lane_id]["width"]
    lane_length = config.sensor_info[bike_lane_id]["length"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: bike_lane
    bike_lane_conditions_class = classes.BikeLanesGeneral(id_bl, bike_lane_name, region_name, country_info, general_latitude, general_longitude, lane_width, lane_length)
    
    #Generate dictionaries for the request (could be a for)
    dict_bike_lane_dict = bike_lane_conditions_class.__dict__

    #Format new parameter values to python class
    dict_data_model_bike_lane = format_data.format_bike_lane(dict_bike_lane_dict, bike_lane_count, string_date_observed)
    
    list_dicts = [dict_data_model_bike_lane]
    
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

# Functions that create/update the information of Bike Lanes in the CB
def execute_bikelane_conditions_local(service_name, date_observed, bike_lane_id, bike_lane_count):
    method_name = 'execute_bikelane_conditions_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    id_bl = config.sensor_info[bike_lane_id]["id"]
    bike_lane_name = config.sensor_info[bike_lane_id]["name"]
    general_latitude = config.sensor_info[bike_lane_id]["latitude"]
    general_longitude = config.sensor_info[bike_lane_id]["longitude"]
    lane_width = config.sensor_info[bike_lane_id]["width"]
    lane_length = config.sensor_info[bike_lane_id]["length"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: bike_lane
    bike_lane_conditions_class = classes.BikeLanesGeneral(id_bl, bike_lane_name, region_name, country_info, general_latitude, general_longitude, lane_width, lane_length)
    
    #Generate dictionaries for the request (could be a for)
    dict_bike_lane_dict = bike_lane_conditions_class.__dict__

    #Format new parameter values to python class
    dict_data_model_bike_lane = format_data.format_bike_lane(dict_bike_lane_dict, bike_lane_count, string_date_observed)
    
    list_dicts = [dict_data_model_bike_lane]
    
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