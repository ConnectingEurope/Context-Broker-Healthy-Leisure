from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import requests

import config.config as cnf
config = cnf.Config()

import data_formatter.data_formatter as formatter
import connectors.mysql_connector as mysql
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import algorithms.aqi.air_quality_index as aqi
import core.nereo_classes_ld as classes
import utils.generate_information as generate
import rule_engine.rule_engine as rule_engine 

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

#ORION
CB_URI_LD = config.context_broker_uri_ld
CB_TYPES = config.context_broker_types
SUB_URI_LD = config.subscription_uri_ld
NIFI_NOTIFY_URI = config.nifi_notify_uri

#WALKING ROUTES
WALKING_ROUTES_TABLE = config.walking_routes_table
WALKING_ROUTES_COLUMN_NAMES = config.walking_routes_column_names

#RULE ENGINE
DATABASE = config.mysql_db
RULE_TABLE = config.mysql_alert_table
ENTITY_TYPES = config.entity_types

#This API method check the health of the API
class Health(Resource):
    def get(self):
        return {"Status":"OK"}, 200

#This API method returns the information for the beach screen in mobile APP
class Beach(Resource):
    def get(self, id):
        try:
            ctx_ids = formatter.get_beach_ids(id)
            response = formatter.beach_response(CB_URI_LD, ctx_ids)
            return response, 200
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            print(response)
            return response, 500

#This API method returns the information for the bike lanes screen in mobile APP
class BikeLane(Resource):
    def get(self, id=None):
        try:
            ctx_id = formatter.get_bikelanes_ids(id)
            response = formatter.bikelane_response(CB_URI_LD, ctx_id)
            return response, 200
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            print(response)
            return response, 500

#This API method returns the information for the walking routes screen in mobile APP
class WalkingRoute(Resource):
	def get(self, route_id=None):
		try:
			query_walking_routes_column_name = ''

			for column_name in WALKING_ROUTES_COLUMN_NAMES:
				query_walking_routes_column_name = query_walking_routes_column_name + column_name + ','

			query_walking_routes_column_name = query_walking_routes_column_name[:-1]
			
			if route_id is not None:
				query= "SELECT {0} FROM {1} WHERE id={2}".format(query_walking_routes_column_name, WALKING_ROUTES_TABLE,route_id)
			else:
				query = "SELECT {0} FROM {1}".format(query_walking_routes_column_name, WALKING_ROUTES_TABLE)

			print(query)   
			db_connector = mysql.connect()
			list_mysql_response = mysql.select_query(db_connector, query)
			response = formatter.format_mysql_walking_routes(list_mysql_response, WALKING_ROUTES_COLUMN_NAMES)    
			return response, 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

#This API method returns the information for the main screen in mobile APP
class SkyState(Resource):
    def get(self):
        try:
            response = formatter.sky_status_response(CB_URI_LD)
            return response, 200
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            print(response)
            return response, 500
            
#This API method returns the information of the user to login/register in mobile APP	
class User(Resource):
    def post(self):
        try:
            post_json_received = request.get_json()

            if post_json_received["register"]:
                response, code = formatter.register_user(post_json_received)
            else:
                response, code = formatter.login_user(post_json_received)
            print(response)
            return response, code
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            print(response)
            return response, 500
			
class WebUser(Resource):
	def post(self):
		try:
			post_json_received = request.get_json()
			if post_json_received['register']:
				response, code = formatter.register_web_user(post_json_received)
			else:
				response, code = formatter.login_web_user(post_json_received)
			return response, code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500		
	def delete(self,id):
		try:
			# post_json_received = request.get_json()
			response, code = formatter.delete_web_user(id)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500
	def put(self):
		try:
			post_json_received = request.get_json()
			response, code = formatter.update_web_user(post_json_received)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

#This API method updated the information of the preferenced of a user in mobile APP
class Preferences(Resource):
    def post(self, id):
        try:
            post_json_received = request.get_json()
            response, code = formatter.update_preferences(post_json_received, id)
            print(response)
            return response, code
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            print(response)
            return response, 500
    def get(self, id):
        try:
            omit = request.args.get('omit')
            response = ''
            if omit:
                response, code = formatter.disable_preferences(id)
            else:
                response, code = formatter.enable_preferences(id)
            print(response)
            return response, code
        except Exception as ex:
            response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
            return response, 500

#This method receive the notifications from orion to calculate different algorithms
class PublishIndex(Resource):
	def post(self, id):
		try:
			print("Received post of {0}".format(id))
			print("HEADERS: {0}".format(request.headers))
			print("SERVICE: {0}".format(request.headers["fiware-service"]))
			post_json_received = request.get_json()
			receied_dict_data = post_json_received["data"][0]
			print(post_json_received)
			
			if id == "aqi":
				service_name = request.headers["fiware-service"]
				headers={'fiware-service': service_name,
					'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
				}
			
				list_fields = formatter.get_index_fields(id)
				list_agents = []
				list_values = []
				
				# Calculate AQI
				for field in list_fields:
					list_agents.append(field)
					list_values.append(receied_dict_data[field]["value"])

				critic_air_quality_agent = aqi.calculate_AQI(list_agents, list_values)

				# Format AQI values
				aqi_json_update = formatter.parse_aqi_data(critic_air_quality_agent.rangeValue, critic_air_quality_agent.rangeLevel)
				print(aqi_json_update)
				# Update orion information
				response = orion.update_specific_data(CB_URI_LD, receied_dict_data["id"], headers, aqi_json_update)
				print(200)
				return 200
			elif id == "fire-forest":
				# Get POST data as json & read it as a DataFrame
				return 200
			else:
				response = {"Message": "Something went wrong. No found id: {0}".format(id)}, 404
				print(response)
				return response
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

#This method returns the result of the recommender system
class Recommender(Resource):	   
	def get(self,id):
		try:
			print("GET Recommender")
			# Retrive information of the receieved user id in mySQL DB
			dict_mysql_data = formatter.get_user_info_mysql(id)
			
			# Collect orion information to execute recommender (no occupancy)
			dict_recommender_info = {}
			dict_recommender_info = formatter.get_recommender_general_info(CB_URI_LD, dict_recommender_info)
			print(dict_recommender_info)
			
			# Collect orion information to execute recommender (occupancy)
			dict_recommender_info = formatter.get_recommender_occupancy_info(CB_URI_LD, dict_recommender_info)
			print(dict_recommender_info)
			
			# Parse mysql column name to data model fields
			list_mysql_fields, list_class_fields = formatter.get_mysql_fields()
			print(list_mysql_fields)
			print(list_class_fields)

			for i in range(len(list_mysql_fields)):
				dict_recommender_info[list_class_fields[i]] = dict_mysql_data[list_mysql_fields[i]]
			
			# Execute recommender
			beach_recommendation, bike_recommendation, walk_recommendation = formatter.execute_recommender(dict_recommender_info)
			print(dict_recommender_info)

			# POST orion statics
			try:
				service_name = 'recommenderstats'
				headers = {
					'fiware-service': service_name,
					'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
				}
				sub_description_elastic = 'Notify Elastic of'
				sub_description_api = 'Notify API of'
				notify_elastic = True
				notify_api = False
				list_sub_parameters_elastic = ["description", "dateObserved", "usePreferences", "userId", "firstPreference", "secondPreference", "thirdPreference", "beachRecommendationResult", "bikeRecommendationResult", "walkRecommendationResult"]

				recommender_class = classes.Recommendation(id)
				string_datetime_now, date_datetime_now = generate.datetime_time_tz()

				if dict_recommender_info["usePreference"] == 1:
					list_preferences = formatter.format_preference_order(dict_recommender_info["preference_beach"], dict_recommender_info["preference_bike"], dict_recommender_info["preference_walk"])
					json_data_model_recommender = format_data.format_recommender_json(recommender_class, string_datetime_now, dict_recommender_info["usePreference"], list_preferences[0], list_preferences[1], list_preferences[2], beach_recommendation.recommendation_result, bike_recommendation.recommendation_result, walk_recommendation.recommendation_result)
				else:
					json_data_model_recommender = format_data.format_recommender_json(recommender_class, string_datetime_now, dict_recommender_info["usePreference"], "", "", "", beach_recommendation.recommendation_result, bike_recommendation.recommendation_result, walk_recommendation.recommendation_result)

				dict_recommender_json = json_data_model_recommender.__dict__
				list_dicts = [dict_recommender_json]
				
				subscription_type = list_dicts[0]["type"]
				subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
				subscription_json_api = ''
    
				response = orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
				print(response.status_code)
				print(response.content)
			except Exception as ex:
				response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
				print(response)
				
			# RETURN FORMAT
			print(beach_recommendation.recommendation_result, bike_recommendation.recommendation_result, walk_recommendation.recommendation_result)

			response = formatter.format_recommender_response(id, beach_recommendation.recommendation_result, bike_recommendation.recommendation_result, walk_recommendation.recommendation_result)
			print(response)
			return response, 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

#This method received the notification of all dat from orion and it executes the rule engine
class Notifications(Resource):
	def post(self):
		try:
			#Get data from request received
			post_json_received  = request.get_json()
			service_name = request.headers["fiware-service"]
			dict_data = post_json_received["data"][0]
    
			#process received data
			list_attributes = formatter.parse_received_data_rule_engine()
			list_data_rule_engine = formatter.data_to_rule_engine(service_name, dict_data, list_attributes)
			
			#Load the rules in mysql
			list_rules = rule_engine.load_rules()
			
			#For every rule to be analyzed is processed into rule engine
			for data_rule in list_data_rule_engine:
				print(data_rule)
				rule_engine.evaluate_rules(service_name, list_rules, data_rule)
            
			return {"Status":"OK"}, 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

class Categories(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT category.value FROM category "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'} 

		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class SubCategories(Resource):
	def get(self, category):
		try:
			mydb = mysql.connect()
			query_cat_id = "SELECT category.id FROM category WHERE category.value = '{0}'".format(category)
			query_cat_result = mysql.select_query(mydb, query_cat_id)
			single_value = query_cat_result[0][0]
			query = "SELECT subcategory.value FROM relational JOIN subcategory ON relational.id_subcategory = subcategory.id WHERE relational.id_category = {0}".format(single_value)
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response, {'Access-Control-Allow-Origin': '*'}

class Severity(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT severity.value FROM severity "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class RuleEngine(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format(DATABASE, RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)
			column_list = formatter.single_value_tuple_list_to_list(column_query)

			rule_query = "SELECT * FROM rules"#.format("rules")
			rule_query_result = mysql.select_query(mydb, rule_query)

			response = formatter.create_rule_json(rule_query_result, column_list)

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def delete(self, id):
		try:
			mydb = mysql.connect()
			service_subs_query = "SELECT service_name, subscription_id FROM {0} WHERE id = {1}".format(RULE_TABLE, id)
			service_subs = mysql.select_query(mydb, service_subs_query)
			query = "DELETE FROM {0} WHERE id = {1}".format(RULE_TABLE,id)
			response = mysql.delete_query(mydb, query)

			delete_header = {
								'fiware-service': service_subs[0][0],
								'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
							}

			orion.request_delete_data(SUB_URI_LD, delete_header, service_subs[0][1])
			#Delete from orion

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def post(self):
		try:
			post_json_received = request.get_json()
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format(DATABASE, RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)

			for rule in post_json_received:
				headers = {
							'fiware-service': rule["service_name"],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}
				response = ""
				bool_update = False
				request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
				if type(request_json) is dict:
					error_message = 'The service does not exists'
					raise Exception(error_message)
				rule["entity_type"] = ENTITY_TYPES[rule["service_name"]]
				if rule["id"] != "":
					try:
						#In case we need to delete subs and service changed
						query_service = "SELECT service_name FROM rules WHERE id = {0}".format(rule["id"])
						service_result = mysql.select_query(mydb, query_service)
						delete_header = {
							'fiware-service': service_result[0][0],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}

						rule_json_values = formatter.get_rule_values_from_json(rule)
						query_set = formatter.get_columns_string_for_update(column_query)
						query_set = query_set % rule_json_values
						query_set = query_set.rstrip(',')
						query = "UPDATE {0} SET {1} WHERE id={2}".format(RULE_TABLE, query_set, rule["id"])
						query_result = mysql.update_query(mydb,query)
						if query_result[0] != 0:
							
							#DELETE SUBS
							orion.request_delete_data(SUB_URI_LD, delete_header, rule["subscription_id"])

							subs_json = formatter.create_subscription_json(rule)

							response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
							bool_update = True
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
				else:
					try:
						#POST TO ORION
						subs_json = formatter.create_subscription_json(rule)
						response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
						
				if response != "" and response.status_code >= 200 and response.status_code < 300:
					subscription_id = ''
					check_subscription_content = orion.check_existing_sub(SUB_URI_LD, headers).json()
					
					if len(check_subscription_content) > 0:
						for i in range(len(check_subscription_content)):
							if subs_json["description"] == check_subscription_content[i]["description"]:
								subscription_id = check_subscription_content[i]["id"]
								break
								
					if subscription_id == '':
						error_message = 'Could not locate the id of the subscription'
						raise Exception(error_message)
					else:
						if bool_update:
							rule["subscription_id"]=subscription_id
							query = "UPDATE {0} SET subscription_id='{1}' WHERE id = {2}".format(RULE_TABLE, subscription_id, rule["id"])					
							response = mysql.update_query(mydb, query)
						else:
							rule["subscription_id"]=subscription_id		
							rule_json_values = formatter.get_rule_values_from_json(rule)
							column_list = []
							for column in column_query:
								column_list.append(column[0])
							column_tuple = tuple(column_list[1:])
							query = "INSERT INTO {0} {1} VALUES %s".format(RULE_TABLE, str(column_tuple).replace("'",""))					
							query = query % str(rule_json_values)
							response = mysql.insert_query(mydb, query)
			return 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class Attributes(Resource):
	def get(self, service):
		try:
			headers = {'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' , 'fiware-service': service}
			request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
			if type(request_json) is dict:
				error_message = 'The service does not exists, could not load attributes'
				raise Exception(error_message)
			else:
				response = request_json[0]["attributeNames"]
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

api.add_resource(Health, "/health")         
api.add_resource(Beach, "/beach/<string:id>")
api.add_resource(BikeLane, "/bikelane","/bikelane/<id>")
api.add_resource(WalkingRoute, "/walkingroute","/walkingroute/<route_id>")
api.add_resource(SkyState, "/skystate")
api.add_resource(User, "/user")
api.add_resource(WebUser, "/web-user")
api.add_resource(Preferences, "/preferences/<id>")
api.add_resource(PublishIndex, "/index/<id>")
api.add_resource(Recommender, "/recommender/<id>")
api.add_resource(Notifications, "/notifications")
api.add_resource(Categories, "/categories")
api.add_resource(SubCategories, "/subcategories/<string:category>")
api.add_resource(Severity, "/severity")
api.add_resource(RuleEngine, "/rule-engine", "/rule-engine/<id>")
api.add_resource(Attributes, "/attributes/<string:service>")

if __name__ == "__main__":
    app.run(debug=True)
