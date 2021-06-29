import requests
import json
import base64
import os

import config.config as cnf
config = cnf.Config()

import connectors.mysql_connector as mysql
import connectors.format_data as format
import connectors.orion_connector_ld as orion
import algorithms.recommender.recommender_system as rec

#API METHOD MOBILE APP
LINK_CONTEXT_REFERENCE = config.link_context_reference
ENVIRONMENT_AEMET_ID = config.aemet_environment_id
WO_AEMET_SERVICE = config.weather_observed_service
AQO_TEMP_SERVICE = config.aqo_service
AQO_AQI_SERVICE = config.aqo_aqi_service
BEACH_SERVICE = config.beach_service
BIKE_SERVICE = config.bikelane_service
SEA_SERVICE = config.sea_service

#RECOMMENDER CONSTANTS
RECOMMENDER_INFO = config.reccomender_info
RECOMMENDER_OCCUPANCY = config.reccomender_occupancy
MYSQL_FIELDS = config.mysql_important_fields
MAX_BEACH = config.max_occupancy['beach']
MAX_BIKE = config.max_occupancy['bike']
MAX_WALK = config.max_occupancy['walk']
USERS_TABLE = config.users_table
USERS_COLUMN_NAMES = config.users_column_names
WALK_ROUTES_LOCATION_COLUMN_NAME = config.walking_location_column

#RULE ENGINE CONSTANTS
RULE_ATTRIBUTE_COLUMN = config.mysql_alert_attribute_column
RULE_ENGINE_TABLE = config.mysql_alert_table
NOTYFY_API_URI = config.api_notify_uri+"notifications"

#This method retrive the orion service ids depnding on the requested beach id
def get_beach_ids(id):
    if id == "playa-levante":
        selected_id = config.ids_playa_levante
    elif id == "playa-poniente":
        selected_id = config.ids_playa_poniente
    else:
        exception_message = "Beach id doesn't exist '{0}'".format(id)
        raise Exception(exception_message)

    return selected_id

#This method parse the information of the beach API method to be sent back
def beach_response(cb_uri, ctx_ids):
    response = {}
    
    if ctx_ids["beach"] != '':
        response_get = requests.get(cb_uri + ctx_ids["beach"], headers={'fiware-service': BEACH_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
        
        if response_get.status_code >= 200 and response_get.status_code <300:
            response_beach = response_get.json()
            response["peopleOccupancy"] = response_beach['peopleOccupancy']['value']
            response["occupationRate"] = response_beach['occupationRate']['value']
            response["location"]= response_beach["location"]["value"]["coordinates"]
        else:
            exception_message = 'No data in {0} - ID: {1}'.format(BEACH_SERVICE, ctx_ids["beach"])
            raise Exception(exception_message)
    else:
        response["peopleOccupancy"] = -1
        response["occupationRate"] = ''
        response["location"]= []
    
    if ctx_ids["seaconditions"] != '':
        response_get = requests.get(cb_uri + ctx_ids["seaconditions"], headers={'fiware-service': SEA_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})

        if response_get.status_code >= 200 and response_get.status_code <300:
            response_sea = response_get.json()
            response["waveLevel"] = response_sea['waveLevel']['value']
            response["surfaceTemperature"] = response_sea['surfaceTemperature']['value']  
        else:
            exception_message = 'No data in {0} - ID: {1}'.format(SEA_SERVICE, ctx_ids["seaconditions"])
            raise Exception(exception_message)   
    else:
        response["waveLevel"] = -1
        response["surfaceTemperature"] = -1
    
    if ctx_ids["environment_temp"] != '':
        response_get = requests.get(cb_uri + ctx_ids["environment_temp"], headers={'fiware-service': AQO_TEMP_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})

        if response_get.status_code >= 200 and response_get.status_code <300:
            response_envtemp = response_get.json()
            response["temperature"] = response_envtemp['temperature']['value']
            response["relativeHumidity"] = response_envtemp['relativeHumidity']['value']
        else:
            exception_message = 'No data in {0} - ID: {1}'.format(AQO_TEMP_SERVICE, ctx_ids["environment_temp"])
            raise Exception(exception_message)			
    else:
        response["temperature"] = -1
        response["relativeHumidity"] = -1
                
    if ctx_ids["environment_aemet"] != '':
        response_get = requests.get(cb_uri + ctx_ids["environment_aemet"], headers={'fiware-service': WO_AEMET_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})

        if response_get.status_code >= 200 and response_get.status_code <300:
            response_envaemet = response_get.json()
            response["windSpeed"] = response_envaemet['windSpeed']['value']
            response["windDirection"] = response_envaemet['windDirection']['value']
        else:
            exception_message = 'No data in {0} - ID: {1}'.format(WO_AEMET_SERVICE, ctx_ids["environment_aemet"])
            raise Exception(exception_message)			
    else:
        response["windSpeed"] = -1
        response["windDirection"] = -1
        
    if ctx_ids["environment_aqi"] != '':
        response_get = requests.get(cb_uri + ctx_ids["environment_aqi"], headers={'fiware-service': AQO_AQI_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})

        if response_get.status_code >= 200 and response_get.status_code <300:
            response_envaqi = response_get.json()
            response["aqiValue"] = response_envaqi['airQualityIndex']['value']
            response["aqiIndex"] = response_envaqi['airQualityLevel']['value']
        else:
            exception_message = 'No data in {0} - ID: {1}'.format(AQO_AQI_SERVICE, ctx_ids["environment_aqi"])
            raise Exception(exception_message)			
    else:
        response["aqiValue"] = -1
        response["aqiIndex"] = ''
        
    return response

#This method retrive the orion service ids depnding on the requested bike id
def get_bikelanes_ids(id):
    if id == "mediterraneo":
        selected_id = str(config.bikelane_ids["mediterraneo"])
    elif id == "comunitat":
        selected_id = str(config.bikelane_ids["comunitat"])
    elif id == "europa":
        selected_id = str(config.bikelane_ids["europa"])
    elif id is None:
        selected_id = config.bikelane_ids
    else:
        exception_message = "Bike lane id doesn't exist '{0}'".format(id)
        raise Exception(exception_message)
        
    return selected_id

#This method parse the information of the bike API method to be sent back
def bikelane_response(cb_uri, ctx_id):
	response = []
	
	if not isinstance(ctx_id, str):
		if ctx_id["mediterraneo"] != '':
			response_get = requests.get(cb_uri + ctx_id["mediterraneo"], headers={'fiware-service': BIKE_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
			
			if response_get.status_code >= 200 and response_get.status_code <300:
				response_lane = response_get.json()
				response.append({"id": ctx_id["mediterraneo"], "laneOccupancy": response_lane['laneOccupancy']['value']})
			else:
				exception_message = 'No data in {0} - ID: {1}'.format(BIKE_SERVICE, ctx_id["mediterraneo"])
				raise Exception(exception_message)	
		else:
			response.append({"id": ctx_id["mediterraneo"], "laneOccupancy": -1})
		
		if ctx_id["comunitat"] != '':
			response_get = requests.get(cb_uri + ctx_id["comunitat"], headers={'fiware-service': BIKE_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
			
			if response_get.status_code >= 200 and response_get.status_code <300:
				response_lane = response_get.json()
				response.append({"id": ctx_id["comunitat"], "laneOccupancy": response_lane['laneOccupancy']['value']})
			else:
				exception_message = 'No data in {0} - ID: {1}'.format(BIKE_SERVICE, ctx_id["comunitat"])
				raise Exception(exception_message)	
		else:
			response.append({"id": ctx_id["comunitat"], "laneOccupancy": -1})
		
		if ctx_id["europa"] != '':
			response_get = requests.get(cb_uri + ctx_id["europa"], headers={'fiware-service': BIKE_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
			
			if response_get.status_code >= 200 and response_get.status_code <300:
				response_lane = response_get.json()
				response.append({"id": ctx_id["europa"], "laneOccupancy": response_lane['laneOccupancy']['value']})
			else:
				exception_message = 'No data in {0} - ID: {1}'.format(BIKE_SERVICE, ctx_id["europa"])
				raise Exception(exception_message)	
		else:
			response.append({"id": ctx_id["europa"], "laneOccupancy": -1})
	else:
		response_get = requests.get(cb_uri + ctx_id, headers={'fiware-service': BIKE_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
		
		if response_get.status_code >= 200 and response_get.status_code <300:
			response_lane = response_get.json()
			response.append({"id": ctx_id, "laneOccupancy": response_lane['laneOccupancy']['value']})
		else:
			exception_message = 'No data in {0} - ID: {1}'.format(BIKE_SERVICE, ctx_id)
			raise Exception(exception_message)	
			
	return response

#This method parse the information of mysql to be sent back in the walking routes API method
def format_mysql_walking_routes(list_mysql_response, mysql_column_names):
	list_response = []
	
	for element in list_mysql_response:
		response = {}
		for i in range(len(element)):
			#print(mysql_column_names[i])
			#print(WALK_ROUTES_LOCATION_COLUMN_NAME)
			if mysql_column_names[i] == WALK_ROUTES_LOCATION_COLUMN_NAME:
				#print("INSIDE")
				list_location = format.format_location_linestring(element[i])
				response["location"] = list_location
				#print(response["location"])
			else:
				response[mysql_column_names[i]] = element[i]
				#print(response[mysql_column_names[i]])
			#print("OUTSITE")

		list_response.append(response)

	print(list_response)
	return list_response

#This method parse the response for the API method of the state of the sky
def sky_status_response(cb_uri):
	response_orion = requests.get(cb_uri + ENVIRONMENT_AEMET_ID, headers={'fiware-service': WO_AEMET_SERVICE, 'Link': LINK_CONTEXT_REFERENCE})
    
	if response_orion.status_code >= 200 and response_orion.status_code <300:
		response_orion_aemet = response_orion.json()
		
		db_connector = mysql.connect()
		query="SELECT * FROM weather_icons WHERE sky_state='{0}'".format(response_orion_aemet["weatherType"]["value"])
		sky_state_icon_info = mysql.select_query(db_connector, query)

		if len(sky_state_icon_info) == 0:
			exception_message = 'No image for the sky_state = {0}'.format(response_orion_aemet["weatherType"]["value"])
			raise Exception(exception_message)
		else:
			response = {
			"descriptiveSkyState": response_orion_aemet["weatherType"]["value"],
			"temperature": response_orion_aemet["temperature"]["value"],
			"relativeHumidity": response_orion_aemet["relativeHumidity"]["value"],
			"icon": get_base64_encoded_image(sky_state_icon_info[0][3])
			}

		return response
	else:
		exception_message = 'No data in {0} - ID: {1}'.format(WO_AEMET_SERVICE, ENVIRONMENT_AEMET_ID)
		raise Exception(exception_message)	

#This method returns the value of the image in base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

#This method check the log in parameters
def login_user(user_data):
    db_connector = mysql.connect()
    query="SELECT * FROM users where email='{0}' and password='{1}'".format(user_data['email'], user_data['password'])
    user_info = mysql.select_query(db_connector, query)
    
    if len(user_info) == 0:
        exception_message = "Incorrect user or password"
        raise Exception(exception_message)
    else:
        response = {
            "id"                    : user_info[0][0],
            "username"              : user_info[0][1],
            "email"                 : user_info[0][2],
            "name"                  : user_info[0][3],
            "beach_position"        : user_info[0][5],
            "bikelane_position"     : user_info[0][6],    
            "walikng_route_position": user_info[0][7],
        }
        
    return response, 200

#This method registers a user to the mysql
def register_user(user_data):
    db_connector = mysql.connect()
    query="INSERT INTO users(username, email, name, password) VALUES('{0}','{1}','{2}','{3}')".format(user_data['username'],user_data['email'],user_data['name'], user_data['password'])
    user_info, code = mysql.insert_query(db_connector, query)

    if not isinstance(user_info, int):
        exception_message = "Missing fields. Fill all the required fields."
        raise Exception(exception_message)
    else:
        response = {
            "id" : user_info
        }

    return response, code

#This method updated the preferences in the db
def update_preferences(user_data, id):
    db_connector = mysql.connect()
    query="UPDATE users SET beach_position={0},bikelane_position={1},walking_route_position={2},preferences=1 WHERE id={3}".format(user_data["beach_position"],user_data["bikelane_position"],user_data["walking_route_position"], id)
    update_info, code = mysql.update_query(db_connector, query)
    
    return update_info, code

#This method enable the preferences for later use in the recommender algorithm
def enable_preferences(id):
    db_connector = mysql.connect()
    query="UPDATE users SET preferences=1 WHERE id={0}".format(id)
    response, code = mysql.update_query(db_connector, query)
    
    return response, code

#This method disable the preferences for later use in the recommender algorithm
def disable_preferences(id):
    db_connector = mysql.connect()
    query="UPDATE users SET preferences=0 WHERE id={0}".format(id)
    response, code = mysql.update_query(db_connector, query)
    
    return response, code

### WEB USERS METHODS ###
#This method check the log in parameters
def login_web_user(user_data):
    db_connector = mysql.connect()
    query="SELECT * FROM web_users where email='{0}' and password='{1}'".format(user_data['email'], user_data['password'])
    user_info = mysql.select_query(db_connector, query)
    
    if len(user_info) == 0:
        exception_message = "Incorrect user or password"
        raise Exception(exception_message)
    else:
        response = {
            "id"                    : user_info[0][0],
            "username"              : user_info[0][1],
            "email"                 : user_info[0][2],
            "name"                  : user_info[0][4],
        }
        
    return response, 200

#This method registers a user to the mysql
def register_web_user(user_data):
    db_connector = mysql.connect()
    query="INSERT INTO web_users(username, email, password, name) VALUES('{0}','{1}','{2}','{3}')".format(user_data['username'],user_data['email'], user_data['password'],user_data['name'])
    user_info, code = mysql.insert_query(db_connector, query)

    if not isinstance(user_info, int):
        exception_message = "Missing fields. Fill all the required fields."
        raise Exception(exception_message)
    else:
        response = {
            "id" : user_info
        }

    return response, code
def update_web_user(user_data):
    db_connector = mysql.connect()
    query="UPDATE web_users SET name='{0}' WHERE id={1}".format(user_data['name'],user_data['id'])
    code = mysql.update_query(db_connector, query)

    if code != 200:
        exception_message = "Could not update. Check updated fields."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully updated."
        }
    return response,code
def delete_web_user(id):
    db_connector = mysql.connect()
    query="DELETE FROM web_users WHERE id={0}".format(id)
    code = mysql.delete_query(db_connector, query)

    if code != 200:
        exception_message = "Could not delete the user."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully deleted."
        }
    return response,code
#This method retrive the orion service ids depnding on the requested published index id
def get_index_fields(id):
    if id == "aqi":
        selected_fields = config.indexes["aqi"]
    elif id == "fire-forest":
        selected_fields = config.indexes["fire-forest"]
    else:
        exception_message = "Index id doesn't exist '{0}'".format(id)
        raise Exception(exception_message)
        
    return selected_fields

#this method created the json to update the AQI values
def parse_aqi_data(aqi_index, aqi_level):
	aqi_json_update = {
	"airQualityIndex": {"type": "Property", "value": aqi_index},
	"airQualityLevel": {"type": "Property", "value": aqi_level}
	}
	
	return aqi_json_update

#This method retrive the information of a user in db
def get_user_info_mysql(id):
	select_query = "SELECT * FROM {0} WHERE id={1}".format(USERS_TABLE, id)
	db_connector = mysql.connect()
	list_mysql_response = mysql.select_query(db_connector, select_query)
	dict_mysql_data = format_mysql_users(list_mysql_response[0], USERS_COLUMN_NAMES)
	
	return dict_mysql_data

#This method created a dictionary using the column names and the values of a response of mysql
def format_mysql_users(tuple_mysql_response, mysql_column_names):
	dict_users = {}

	for i in range(len(tuple_mysql_response)):
		dict_users[mysql_column_names[i]] = tuple_mysql_response[i]
			
	return dict_users

#This method retrive the information of CB fo the recommender algorithm
def get_recommender_general_info(cb_uri, dict_recommender_info):
	recommender_ids = RECOMMENDER_INFO["ids"]
	recommender_fields = RECOMMENDER_INFO["fields"]
	recommender_services = RECOMMENDER_INFO["services"]
	
	for i in range(len(recommender_ids)):
		get_headers = {'fiware-service': recommender_services[i], 'Link': LINK_CONTEXT_REFERENCE}
		get_url = cb_uri + recommender_ids[i]
		response_orion = requests.get(get_url, headers=get_headers)
		
		if response_orion.status_code >= 200 and response_orion.status_code <300:
			response_orion_general_info = response_orion.json()
			for field in recommender_fields[i]:
				dict_recommender_info[field] = response_orion_general_info[field]["value"]
		else:
			exception_message = 'No data in {0} - ID: {1}'.format(recommender_services[i], recommender_ids[i])
			raise Exception(exception_message)	
					
	return dict_recommender_info

#This method retrive the information of CB fo the recommender algorithm
def get_recommender_occupancy_info(cb_uri, dict_recommender_info):
	recommender_ids = RECOMMENDER_OCCUPANCY["ids"]
	recommender_fields = RECOMMENDER_OCCUPANCY["fields"]
	recommender_services = RECOMMENDER_OCCUPANCY["services"]
	
	for i in range(len(recommender_ids)):
		get_headers = {'fiware-service': recommender_services[i], 'Link': LINK_CONTEXT_REFERENCE}
		response_orion = requests.get(cb_uri + recommender_ids[i], headers=get_headers)
		
		if response_orion.status_code >= 200 and response_orion.status_code <300:
			response_orion_occupancy = response_orion.json()
			for field in recommender_fields[i]:
				value_percentage_occupancy = parse_occupancy_percentage(field, response_orion_occupancy[field]["value"])
				dict_recommender_info[field] = value_percentage_occupancy
		else:
			exception_message = 'No data in {0} - ID: {1}'.format(recommender_services[i], recommender_ids[i])
			raise Exception(exception_message)
							
	return dict_recommender_info

#THis method parse the occupancy and created a % of it
def parse_occupancy_percentage(field, field_value):
	if field == 'peopleOccupancy':
		field_percentage = field_value/MAX_BEACH*100
	elif field == 'laneOccupancy':
		field_percentage = field_value/MAX_BIKE*100
	elif field == 'predictiveRouteOccupancy':
		field_percentage = field_value/MAX_WALK*100
	else:
		field_percentage = 0
		
	if field_percentage > 100:
		field_percentage = 100
	elif field_percentage < 0:
		field_percentage = 0
	else:
		field_percentage = field_percentage
		
	return field_percentage

#This method retrive the name of the fields of mysql and data model (class)
def get_mysql_fields():
	mysql_fields = MYSQL_FIELDS["mysql"]
	class_fields = MYSQL_FIELDS["class"]
	
	return mysql_fields, class_fields

#This method executed the recommender
def execute_recommender(dict_recommender_info):
	# Execute beach recomendation system
	beach_recommendation = rec.RecommendationSystem(dict_recommender_info["temperature"], dict_recommender_info["surfaceTemperature"], dict_recommender_info["weatherType"], dict_recommender_info["windSpeed"], dict_recommender_info["peopleOccupancy"], dict_recommender_info["airQualityIndex"], dict_recommender_info["usePreference"], dict_recommender_info["preference_beach"])
	beach_recommendation.grade_beach_recommendation()
	# Execute bike recomendation system	
	bike_recommendation = rec.RecommendationSystem(dict_recommender_info["temperature"], dict_recommender_info["surfaceTemperature"], dict_recommender_info["weatherType"], dict_recommender_info["windSpeed"], dict_recommender_info["laneOccupancy"], dict_recommender_info["airQualityIndex"], dict_recommender_info["usePreference"], dict_recommender_info["preference_bike"])
	bike_recommendation.grade_bike_recommendation()
	# Execute walking recomendation system
	walk_recommendation = rec.RecommendationSystem(dict_recommender_info["temperature"], dict_recommender_info["surfaceTemperature"], dict_recommender_info["weatherType"], dict_recommender_info["windSpeed"], dict_recommender_info["predictiveRouteOccupancy"], dict_recommender_info["airQualityIndex"], dict_recommender_info["usePreference"], dict_recommender_info["preference_walk"])
	walk_recommendation.grade_walk_recommendation()
	
	return beach_recommendation, bike_recommendation, walk_recommendation

#This method creates a list ordere by the number of preference
def format_preference_order(number_preference_beach, number_preference_bike, number_preference_walk):
	list_preferences = list(range(3))
	list_preferences[number_preference_beach] = 'beach'
	list_preferences[number_preference_bike] = 'bike'
	list_preferences[number_preference_walk] = 'walk'
	
	return list_preferences
	
#This method format the payload response for the recommender API method
def format_recommender_response(id_user, beach_result, bike_result, walk_result):
	response = {}
	response["id"] = id_user
	response["beach_recommender_result"] = beach_result
	response["bike_recommender_result"] = bike_result
	response["walk_recommender_result"] = walk_result
		
	return response

#This method parse the rule engine dat received from the post
def parse_received_data_rule_engine():
	#Select of the fields of the current rules
	mysql_connector = mysql.connect()
	query = "SELECT {0} FROM {1}".format(RULE_ATTRIBUTE_COLUMN, RULE_ENGINE_TABLE)        
	mysql_result = mysql.select_query(mysql_connector, query)
	
	list_attributes = []
	
	#If there are eisting rules, we add to the list the name of the values to be checked.
	if len(mysql_result) > 0:
		for (attribute,) in mysql_result:
			list_attributes.append(str(attribute))
			
	return list_attributes

#This method creates a dictionary for every rule depending on the received fields.
def data_to_rule_engine(service, dict_data, list_attributes):
	list_data_rules = []
	for attribute in list_attributes:
		if attribute in dict_data:
			data = {"service": service,
					"attribute": attribute,
					"dateObserved": dict_data["dateObserved"],
					"value": dict_data[attribute]["value"],
					"dataProvider" : dict_data["dataProvider"]
					}
			list_data_rules.append(data)
               
	return list_data_rules

#This method transforms a list of tuples with a sigle value [ (value1, ), (value2,), ...] to a list [value1, value2, ...]
def single_value_tuple_list_to_list(tuple_list):
    return [item for t in tuple_list for item in t]

#This method creates a json to be sent to the front end 
def create_rule_json( query_result, column_list ):
    json_result = []
    
    for q in query_result:
        row = {}
        for i in range(len(column_list)):
            row[column_list[i]] = q[i]
        
        json_result.append(row)

    return json_result

#This method extracts the values of a json to create a tuple
def get_rule_values_from_json( json ):
	list_temp = [ json["rule_name"], json["service_name"], json["entity_type"], json["attribute_name"],
	json["operator"], json["threshold"], json["value_category"],json["value_subcategory"], json["value_severity"],
	json["subscription_id"], json["recurrence_seconds"] ]
	tuple_res = []
	for value in list_temp:
		if value == "":
			exception_message = "A rule value is empty"
			raise Exception(exception_message) 
		tuple_res.append(value)
	return tuple(tuple_res)

    
#This method creates the string set for an update query for rules
def get_columns_string_for_update( column_tuple ):
    update_set = ""
    aux_tuple = column_tuple[1:]
    for field in aux_tuple:
        if field[0] == "recurrence_seconds" or field[0] == "threshold":
            update_set = update_set + str(field[0])+'=%s,'
        else:
            update_set = update_set + str(field[0])+'="%s",'
    update_set = update_set.rstrip(',')
    return update_set

#This method creates a subscription json
def create_subscription_json( rule_dic ):
	sub_description_alert = "Notify API of {0} {1} {2}".format(rule_dic["attribute_name"], rule_dic["operator"], rule_dic["threshold"])
	list_sub_parameters = ["dateObserved", "dataProvider", rule_dic["attribute_name"]]
	if int(rule_dic["recurrence_seconds"]) != 0:
		print("SECONDS " + NOTYFY_API_URI)
		subs_json = orion.create_json_subscription_alert_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI, int(rule_dic["recurrence_seconds"]) )
	else:
		print("NO SECONDS" + NOTYFY_API_URI)
		subs_json = orion.create_json_subscription_no_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI)
	
	return subs_json
