import utils.generate_information as generate

# Function that parse the data requested from AEMET to the data model class structure
# AEMET beach conditions is updated twice a day -> service executed every 2 hours
def format_sea_conditions(object_sea_conditions, dict_item):
	object_sea_conditions["source"] = {"type": "Property", "value": dict_item["origen"]["web"]}
	object_sea_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": generate.convert_datetime_aemet(dict_item["elaborado"])}}
	object_sea_conditions["waveLevel"] = {"type": "Property", "value": generate.generate_wave_level(dict_item["prediccion"]["dia"][0]["oleaje"]["f1"])}
	object_sea_conditions["surfaceTemperature"] = {"type": "Property", "value": dict_item["prediccion"]["dia"][0]["tAgua"]["valor1"]}
		
	return object_sea_conditions

def format_random_sea_conditions(object_sea_conditions, date_observed, wave_level, sea_temperature):
	object_sea_conditions["source"] = {"type": "Property", "value": "http://www.aemet.es"}
	object_sea_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": date_observed}}
	object_sea_conditions["waveLevel"] = {"type": "Property", "value": wave_level}
	object_sea_conditions["surfaceTemperature"] = {"type": "Property", "value": sea_temperature}
		
	return object_sea_conditions

# Function that parse the data from the beach predictive module to the data model class structure
# Beach sensor updated every minute -> servicec executed every 5 minutes
def format_beach(object_beach_conditions, beach_occupancy, date_observed):
	object_beach_conditions["peopleOccupancy"] = {"type": "Property", "value": beach_occupancy}
	object_beach_conditions["occupationRate"] = {"type": "Property", "value": generate.generate_beach_occupation_rate(beach_occupancy)} 
	object_beach_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": date_observed}}
	
	return object_beach_conditions

# Function that parse the data from the bike lane module to the data model class structure
# Bike lane sensors updated every minute -> service executed every 5 minutes
def format_bike_lane(object_bike_lane_conditions, lane_occupancy, date_observed):	
	object_bike_lane_conditions["laneOccupancy"] = {"type": "Property", "value": lane_occupancy}
	object_bike_lane_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": date_observed}}
	
	return object_bike_lane_conditions

# Function that parse the data requested from AEMET to the data model class structure
#AEMET environment conditions is updated 4 times a day or more often for some parameters like temperature or humidity -> service executed every 2 hours
def format_weather_observed_aemet(object_weather_observed_conditions, dict_item):
	object_weather_observed_conditions["source"] = {"type": "Property", "value": dict_item["origen"]["web"]}
	object_weather_observed_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": generate.convert_datetime_aemet(dict_item["elaborado"])}}
	object_weather_observed_conditions["temperature"] = {"type": "Property", "value": dict_item["prediccion"]["dia"][0]["temperatura"]["dato"][1]["value"]}
	object_weather_observed_conditions["feelsLikesTemperature"] = {"type": "Property", "value": dict_item["prediccion"]["dia"][0]["sensTermica"]["dato"][1]["value"]}
	object_weather_observed_conditions["relativeHumidity"] = {"type": "Property", "value": dict_item["prediccion"]["dia"][0]["humedadRelativa"]["dato"][1]["value"]}
	period_wind_speed, wind_speed = generate.find_aemet_prediction_data(dict_item["prediccion"]["dia"][0]["viento"], "periodo", "direccion", "velocidad")
	object_weather_observed_conditions["windSpeed"] = {"type": "Property", "value": wind_speed}
	period_wind_direction, wind_direction = generate.find_aemet_prediction_data(dict_item["prediccion"]["dia"][0]["viento"], "periodo", "direccion", "direccion")
	object_weather_observed_conditions["windDirection"] = {"type": "Property", "value": generate.generate_wind_direction(wind_direction)}
	period_stake_of_the_sky, state_of_the_sky = generate.find_aemet_prediction_data(dict_item["prediccion"]["dia"][0]["estadoCielo"], "periodo", "value", "value")
	object_weather_observed_conditions["weatherType"] = {"type": "Property", "value": generate.convert_AEMET_skystate(state_of_the_sky)}
	
	return object_weather_observed_conditions

def format_random_weather_observed_aemet(object_weather_observed_conditions, AEMET_random_data):
	object_weather_observed_conditions["source"] = {"type": "Property", "value": "http://www.aemet.es"}
	object_weather_observed_conditions["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": AEMET_random_data[0]}}
	object_weather_observed_conditions["temperature"] = {"type": "Property", "value": AEMET_random_data[1]}
	object_weather_observed_conditions["feelsLikesTemperature"] = {"type": "Property", "value": AEMET_random_data[2]}
	object_weather_observed_conditions["relativeHumidity"] = {"type": "Property", "value": AEMET_random_data[3]}
	object_weather_observed_conditions["windSpeed"] = {"type": "Property", "value": AEMET_random_data[4]}
	object_weather_observed_conditions["windDirection"] = {"type": "Property", "value": AEMET_random_data[5]}
	object_weather_observed_conditions["weatherType"] = {"type": "Property", "value": AEMET_random_data[6]}
	
	return object_weather_observed_conditions

def find_air_quality_agent_index(agent_to_find, air_quality_agents):
	agent_index = -1
	for i in range(len(air_quality_agents)):
		if agent_to_find == air_quality_agents[i]:
			agent_index = i
			break

	return agent_index

def format_air_quality_observed_general(object_air_quality_observed, string_date_observed, dict_data):
	for key in dict_data:
		object_air_quality_observed[key] = {"type": "Property", "value": dict_data[key]}

	object_air_quality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_air_quality_observed

def format_air_quality_observed_airquality_sensor(object_air_quality_observed, string_date_observed, air_quality_agents, air_quality_values):
	object_air_quality_observed["pm10"]= {"type": "Property", "value": air_quality_values[find_air_quality_agent_index('pm10', air_quality_agents)]}
	object_air_quality_observed["pm25"]= {"type": "Property", "value": air_quality_values[find_air_quality_agent_index('pm25', air_quality_agents)]}
	object_air_quality_observed["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}

	return object_air_quality_observed

def format_air_quality_observed_temperature_humidity_sensor(object_air_quality_observed, id_sensor, sensor_data):
	object_air_quality_observed.temperature = {"type": "Property", "value": sensor_data[0]}
	object_air_quality_observed.relativeHumidity = {"type": "Property", "value": sensor_data[1]}
	object_air_quality_observed.dateObserved = {"type": "Property", "value": { "type": "DateTime", "value": sensor_data[2]}}

	return object_air_quality_observed

def format_walking_routes(object_walking_route, query_result, result_predictive_model, string_date_observed):
	object_walking_route["predictiveRouteOccupancy"]= {"type": "Property", "value": result_predictive_model}
	object_walking_route["dateObserved"] = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}
	object_walking_route["distance"]= {"type": "Property", "value": query_result[3]}
	object_walking_route["difficulty"]= {"type": "Property", "value": query_result[4]}
	object_walking_route["positiveSlope"]= {"type": "Property", "value": query_result[5]}
	object_walking_route["negativeSlope"]= {"type": "Property", "value": query_result[6]}
	object_walking_route["maxHeight"]= {"type": "Property", "value": query_result[7]}
	object_walking_route["minHeight"]= {"type": "Property", "value": query_result[8]}
	object_walking_route["routeTime"]= {"type": "Property", "value": query_result[9]}
	object_walking_route["url"]= {"type": "Property", "value": query_result[10]}

	return object_walking_route

def format_recommender_json(object_recommender, string_date_observed, use_preferences, first, second, third, beach_result, bike_result, walk_result):
	object_recommender.usePreferences= {"type": "Property", "value": use_preferences}
	object_recommender.dateObserved = {"type": "Property", "value": { "type": "DateTime", "value": string_date_observed}}
	object_recommender.firstPreference = {"type": "Property", "value": first}
	object_recommender.secondPreference = {"type": "Property", "value": second}
	object_recommender.thirdPreference = {"type": "Property", "value": third}
	object_recommender.beachRecommendationResult = {"type": "Property", "value": beach_result}
	object_recommender.bikeRecommendationResult = {"type": "Property", "value": bike_result}
	object_recommender.walkRecommendationResult = {"type": "Property", "value": walk_result}
	
	return object_recommender

def parse_multipoint_mysql(string_tuple_location):
	list_coordinates = []

	if len(string_tuple_location) > 0:
		data_multipoint = string_tuple_location[0][0]
		tuple_test = data_multipoint.replace('MULTIPOINT(', '')
		tuple_test = tuple_test[:-1]
		list_tuples = tuple_test.split(',')
		
		for tuple_value in list_tuples:
			edited_value = tuple_value.replace(')', '').replace(' ', ',').replace('(', '')
			split_comma = edited_value.split(',')
			list_elements = []

			for element in split_comma:
				list_elements.append(float(element))
			
			list_coordinates.append(list_elements)
	else:
		list_elements = []
		list_coordinates.append(list_elements)

	#print(list_coordinates)
	return list_coordinates

def format_modbus_data(key_name, key_value):
	calculed_value = ""

	if key_name == "temperature" or key_name == "relativeHumidity" or key_name == "tvoc":
		calculed_value = key_value/10
	elif key_name == "co2" or key_name == "atmosphericPressure" or key_name == "windSpeed":
		calculed_value = key_value
	elif key_name == "noiseLevel":
		calculed_value = key_value*0.01+25
	else:
		calculed_value = ""

	return calculed_value

def format_location_linestring(string_tuple_location):
	list_coordinates = []
	#print(string_tuple_location)
	tuple_test = string_tuple_location.replace('MULTIPOINT(', '')
	tuple_test = tuple_test[:-1]
	#print(tuple_test)
	list_tuples = tuple_test.split(',')

	for tuple_value in list_tuples:
		edited_value = tuple_value.replace(')', '').replace(' ', ',').replace('(', '')
		split_comma = edited_value.split(',')
		list_elements = []

		for element in split_comma:
			list_elements.append(float(element))
		
		list_coordinates.append(list_elements)

	#print(list_coordinates)
	return list_coordinates