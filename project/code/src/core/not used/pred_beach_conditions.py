import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import predictive_models.models as pred_mod
import config.config as cnf

config = cnf.Config()
CB_URI_LD = config.context_broker_uri_ld_local
SUB_URI_LD = config.subscription_uri_ld_local
NIFI_NOTIFY_URI = config.nifi_notify_uri

list_sub_parameters_elastic = ["dateObserved","dataProvider","occupationRate","predictivePeopleOccupancy", "name", "source", "location", "description"]
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

#INFORMATION BEACH CONDITIONS
id_sensor_beach_levante = 'B001'
id_sensor_beach_poniente = 'P001'
beach_name_levante = 'Playa Levante'
beach_name_poniente = 'Playa Poniente'
city_name_benidorm = 'Benidorm'
country_info_benidorm = 'ES'
beach_levante_latitude=38.534996
beach_levante_longitude=-0.114694
beach_poniente_latitude=38.5311908
beach_poniente_longitude=-0.1591542

# Functions that create/update the information of Beach in the CB
def execute_beach_conditions_pred(service_name, date_observed):
    method_name = 'execute_beach_conditions_pred'
    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: beachPred
    beach_conditions_levante = classes.PredcitionBeach(id_sensor_beach_levante, beach_name_levante, city_name_benidorm, country_info_benidorm, beach_levante_latitude, beach_levante_longitude)
    #beach_conditions_poniente = classes.PredcitionBeach(id_sensor_beach_poniente, beach_name_poniente, city_name_benidorm, country_info_benidorm, beach_poniente_latitude, beach_poniente_longitude)
    
    #Get beach occupancy predictive model
    beach_occupancy_0 = pred_mod.predictive_model_beach_occupancy(date_observed)
    #beach_occupancy_1 = pred_mod.predictive_model_beach_occupancy(date_observed)

    #Format new parameter values to python class
    json_data_model_beach_levante = format_data.format_beach_prediction(beach_conditions_levante, beach_occupancy_0, string_date_observed)
    #json_data_model_beach_poniente = format_data.format_beach_prediction(beach_conditions_poniente, beach_occupancy_1, string_date_observed)
    
    #Generate dictionaries for the request (could be a for)
    dict_beach_conditions_levante = json_data_model_beach_levante.__dict__
    #dict_beach_conditions_poniente = json_data_model_beach_poniente.__dict__

    #list_dicts = [dict_beach_conditions_levante, dict_beach_conditions_poniente]
    list_dicts = [dict_beach_conditions_levante]
    
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
