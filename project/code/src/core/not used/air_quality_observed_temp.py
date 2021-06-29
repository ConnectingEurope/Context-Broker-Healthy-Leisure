import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
CB_URI_LD = config.context_broker_uri_ld_local
SUB_URI_LD = config.subscription_uri_ld_local
NIFI_NOTIFY_URI = config.nifi_notify_uri

list_sub_parameters_elastic = ["name", "dataProvider", "source", "location", "description", "dateObserved", "temperature", "relativeHumidity"]
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

#GENERAL INFORMATION
city_name_benidorm = 'Benidorm'
beach_name_levante = 'Playa Levante'
beach_name_poniente = 'Playa Poniente'
country_info_benidorm = 'ES'
id_sensor_1 = 'AQO002'
sensor_1_latitude=38.535736
sensor_1_longitude=-0.120485
id_sensor_2 = 'AQO003'
sensor_2_latitude=38.534707
sensor_2_longitude=-0.111991
id_sensor_3 = 'AQO004'
sensor_3_latitude=38.533180
sensor_3_longitude=-0.156709
id_sensor_4 = 'AQO005'
sensor_4_latitude=38.529622
sensor_4_longitude=-0.160957

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed_temp(service_name, date_observed):
    method_name = 'execute_air_quality_observed_temp'
    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Create classes: AirQualityobserved
    air_quality_observed_benidorm_1 = classes.AirQualityObserved(id_sensor_1, beach_name_levante, city_name_benidorm, country_info_benidorm, sensor_1_latitude, sensor_1_longitude)
    air_quality_observed_benidorm_2 = classes.AirQualityObserved(id_sensor_2, beach_name_levante, city_name_benidorm, country_info_benidorm, sensor_2_latitude, sensor_2_longitude)
    air_quality_observed_benidorm_3 = classes.AirQualityObserved(id_sensor_3, beach_name_poniente, city_name_benidorm, country_info_benidorm, sensor_3_latitude, sensor_3_longitude)
    air_quality_observed_benidorm_4 = classes.AirQualityObserved(id_sensor_4, beach_name_poniente, city_name_benidorm, country_info_benidorm, sensor_4_latitude, sensor_4_longitude)

    #Generate random values of temperature and humidity
    temperature_1 = generate.generate_temperature_random(date_observed)
    humidity_1 = generate.generate_humidity_random(date_observed)
    temperature_2 = generate.generate_temperature_random(date_observed)
    humidity_2 = generate.generate_humidity_random(date_observed)
    temperature_3 = generate.generate_temperature_random(date_observed)
    humidity_3 = generate.generate_humidity_random(date_observed)
    temperature_4 = generate.generate_temperature_random(date_observed)
    humidity_4 = generate.generate_humidity_random(date_observed)
    
    sensor_data_1 = [temperature_1, humidity_1, string_date_observed]
    sensor_data_2 = [temperature_2, humidity_2, string_date_observed]
    sensor_data_3 = [temperature_3, humidity_3, string_date_observed]
    sensor_data_4 = [temperature_4, humidity_4, string_date_observed]
    
    #Format new parameter values to python class
    json_data_model_air_quality_observed_benidorm_1 = format_data.format_air_quality_observed_temperature_humidity_sensor(air_quality_observed_benidorm_1, id_sensor_1, sensor_data_1)
    json_data_model_air_quality_observed_benidorm_2 = format_data.format_air_quality_observed_temperature_humidity_sensor(air_quality_observed_benidorm_2, id_sensor_2, sensor_data_2)
    json_data_model_air_quality_observed_benidorm_3 = format_data.format_air_quality_observed_temperature_humidity_sensor(air_quality_observed_benidorm_3, id_sensor_3, sensor_data_3)
    json_data_model_air_quality_observed_benidorm_4 = format_data.format_air_quality_observed_temperature_humidity_sensor(air_quality_observed_benidorm_4, id_sensor_4, sensor_data_4)
    
    #Generate dictionaries for the request (could be a for)
    dict_air_quality_observed_benidorm_1 = json_data_model_air_quality_observed_benidorm_1.__dict__
    dict_air_quality_observed_benidorm_2 = json_data_model_air_quality_observed_benidorm_2.__dict__
    dict_air_quality_observed_benidorm_3 = json_data_model_air_quality_observed_benidorm_3.__dict__
    dict_air_quality_observed_benidorm_4 = json_data_model_air_quality_observed_benidorm_4.__dict__

    list_dicts = [dict_air_quality_observed_benidorm_1, dict_air_quality_observed_benidorm_2, dict_air_quality_observed_benidorm_3, dict_air_quality_observed_benidorm_4]
    
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
