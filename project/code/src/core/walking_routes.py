import core.nereo_classes_ld as classes
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import predictive_models.models as pred_mod
import connectors.mysql_connector as mysql
import config.config as cnf

config = cnf.Config()
MYSQL_DT = config.walking_routes_table
NIFI_NOTIFY_URI = config.nifi_notify_uri
region_name = config.region
country_info = config.country
WALKING_ROUTES_COLUMN_NAMES = config.walking_routes_column_names
WALKING_ROUTES_LOCATION_COLUMN = config.walking_location_column

# Functions that create/update the information of Bike Lanes in the CB
def execute_walking_routes(service_name, date_observed):
    method_name = 'execute_walking_routes'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    list_sub_parameters_elastic = config.w_occ_subs
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'

    id_route_1 = config.sensor_info["002"]["id"]
    id_route_2 = config.sensor_info["003"]["id"]
    id_route_3 = config.sensor_info["004"]["id"]

    id_provider_1 = config.sensor_info["002"]["id_provider"]
    id_provider_2 = config.sensor_info["003"]["id_provider"]
    id_provider_3 = config.sensor_info["004"]["id_provider"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }

    query_walking_routes_column_name = ''

    for column_name in WALKING_ROUTES_COLUMN_NAMES:
        query_walking_routes_column_name = query_walking_routes_column_name + column_name + ','
        
    query_walking_routes_column_name = query_walking_routes_column_name[:-1]

    #Retrive info data base
    db_connector = mysql.connect()
    result_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_1))
    result_location_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_1))

    result_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_2))
    result_location_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_2))
    
    result_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_3))
    result_location_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_3))
    
    #Format location LineString
    location_1 = format_data.parse_multipoint_mysql(result_location_mysql_route_1)
    location_2 = format_data.parse_multipoint_mysql(result_location_mysql_route_2)
    location_3 = format_data.parse_multipoint_mysql(result_location_mysql_route_3)

    #Create classes: walking_routes
    route_1_class = classes.WalkingRoutesGeneral(id_provider_1, result_mysql_route_1[0][1], result_mysql_route_1[0][2], region_name, country_info, location_1)
    route_2_class = classes.WalkingRoutesGeneral(id_provider_2, result_mysql_route_2[0][1], result_mysql_route_2[0][2], region_name, country_info, location_2)
    route_3_class = classes.WalkingRoutesGeneral(id_provider_3, result_mysql_route_3[0][1], result_mysql_route_3[0][2], region_name, country_info, location_3)
    
    #Generate dictionaries for the request (could be a for)
    dict_route_1 = route_1_class.__dict__
    dict_route_2 = route_2_class.__dict__
    dict_route_3 = route_3_class.__dict__

    #Predictive model
    walking_route_1_occupancy = 0
    walking_route_2_occupancy = 0
    #walking_route_3_occupancy = pred_mod.predictive_model_route_occupancy()
    walking_route_3_occupancy = 0

    #Format new parameter values to python class
    dict_data_model_route_1 = format_data.format_walking_routes(dict_route_1, result_mysql_route_1[0], walking_route_1_occupancy, string_date_observed)
    dict_data_model_route_2 = format_data.format_walking_routes(dict_route_2, result_mysql_route_2[0], walking_route_2_occupancy, string_date_observed)
    dict_data_model_route_3 = format_data.format_walking_routes(dict_route_3, result_mysql_route_3[0], walking_route_3_occupancy, string_date_observed)
    
    list_dicts = [dict_data_model_route_1, dict_data_model_route_2, dict_data_model_route_3]
    
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
def execute_walking_routes_no_occupancy(service_name, date_observed):
    method_name = 'execute_walking_routes_no_occupancy'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld

    list_sub_parameters_elastic = config.w_no_occ_subs
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'

    id_route_1 = config.sensor_info["002"]["id"]
    id_route_2 = config.sensor_info["003"]["id"]
    id_route_3 = config.sensor_info["004"]["id"]

    id_provider_1 = config.sensor_info["002"]["id_provider"]
    id_provider_2 = config.sensor_info["003"]["id_provider"]
    id_provider_3 = config.sensor_info["004"]["id_provider"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }

    query_walking_routes_column_name = ''

    for column_name in WALKING_ROUTES_COLUMN_NAMES:
        query_walking_routes_column_name = query_walking_routes_column_name + column_name + ','
        
    query_walking_routes_column_name = query_walking_routes_column_name[:-1]

    #Retrive info data base
    db_connector = mysql.connect()
    result_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_1))
    result_location_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_1))

    result_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_2))
    result_location_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_2))
    
    result_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_3))
    result_location_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_3))
    
    #Format location LineString
    location_1 = format_data.parse_multipoint_mysql(result_location_mysql_route_1)
    location_2 = format_data.parse_multipoint_mysql(result_location_mysql_route_2)
    location_3 = format_data.parse_multipoint_mysql(result_location_mysql_route_3)
    
    #Create classes: walking_routes
    route_1_class = classes.WalkingRoutesGeneral(id_provider_1, result_mysql_route_1[0][1], result_mysql_route_1[0][2], region_name, country_info, location_1)
    route_2_class = classes.WalkingRoutesGeneral(id_provider_2, result_mysql_route_2[0][1], result_mysql_route_2[0][2], region_name, country_info, location_2)
    route_3_class = classes.WalkingRoutesGeneral(id_provider_3, result_mysql_route_3[0][1], result_mysql_route_3[0][2], region_name, country_info, location_3)

    #Generate dictionaries for the request (could be a for)
    dict_route_1 = route_1_class.__dict__
    dict_route_2 = route_2_class.__dict__
    dict_route_3 = route_3_class.__dict__

    #Format new parameter values to python class
    dict_data_model_route_1 = format_data.format_walking_routes(dict_route_1, result_mysql_route_1[0], 0, string_date_observed)
    dict_data_model_route_2 = format_data.format_walking_routes(dict_route_2, result_mysql_route_2[0], 0, string_date_observed)
    dict_data_model_route_3 = format_data.format_walking_routes(dict_route_3, result_mysql_route_3[0], 0, string_date_observed)
    
    list_dicts = [dict_data_model_route_1, dict_data_model_route_2, dict_data_model_route_3]
    
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
def execute_walking_routes_no_occupancy_local(service_name, date_observed):
    method_name = 'execute_walking_routes_no_occupancy_local'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local

    list_sub_parameters_elastic = config.w_no_occ_subs
    list_sub_parameters_api = []
    notify_elastic = True
    notify_api = False
    sub_description_elastic = 'Notify Elastic of'
    sub_description_api = 'Notify API of'

    id_route_1 = config.sensor_info["002"]["id"]
    id_route_2 = config.sensor_info["003"]["id"]
    id_route_3 = config.sensor_info["004"]["id"]

    id_provider_1 = config.sensor_info["002"]["id_provider"]
    id_provider_2 = config.sensor_info["003"]["id_provider"]
    id_provider_3 = config.sensor_info["004"]["id_provider"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }

    query_walking_routes_column_name = ''

    for column_name in WALKING_ROUTES_COLUMN_NAMES:
        query_walking_routes_column_name = query_walking_routes_column_name + column_name + ','
        
    query_walking_routes_column_name = query_walking_routes_column_name[:-1]

    #Retrive info data base
    db_connector = mysql.connect_local()
    result_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_1))
    result_location_mysql_route_1 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_1))

    result_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_2))
    result_location_mysql_route_2 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_2))
    
    result_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(query_walking_routes_column_name, MYSQL_DT, id_route_3))
    result_location_mysql_route_3 = mysql.select_query(db_connector, 'SELECT {0} FROM {1} WHERE id={2}'.format(WALKING_ROUTES_LOCATION_COLUMN, MYSQL_DT, id_route_3))
    
    #Format location LineString
    location_1 = format_data.parse_multipoint_mysql(result_location_mysql_route_1)
    location_2 = format_data.parse_multipoint_mysql(result_location_mysql_route_2)
    location_3 = format_data.parse_multipoint_mysql(result_location_mysql_route_3)
    
    #Create classes: walking_routes
    route_1_class = classes.WalkingRoutesGeneral(id_provider_1, result_mysql_route_1[0][1], result_mysql_route_1[0][2], region_name, country_info, location_1)
    route_2_class = classes.WalkingRoutesGeneral(id_provider_2, result_mysql_route_2[0][1], result_mysql_route_2[0][2], region_name, country_info, location_2)
    route_3_class = classes.WalkingRoutesGeneral(id_provider_3, result_mysql_route_3[0][1], result_mysql_route_3[0][2], region_name, country_info, location_3)

    #Generate dictionaries for the request (could be a for)
    dict_route_1 = route_1_class.__dict__
    dict_route_2 = route_2_class.__dict__
    dict_route_3 = route_3_class.__dict__

    #Format new parameter values to python class
    dict_data_model_route_1 = format_data.format_walking_routes(dict_route_1, result_mysql_route_1[0], 0, string_date_observed)
    dict_data_model_route_2 = format_data.format_walking_routes(dict_route_2, result_mysql_route_2[0], 0, string_date_observed)
    dict_data_model_route_3 = format_data.format_walking_routes(dict_route_3, result_mysql_route_3[0], 0, string_date_observed)
   
    list_dicts = [dict_data_model_route_1, dict_data_model_route_2, dict_data_model_route_3]
    
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