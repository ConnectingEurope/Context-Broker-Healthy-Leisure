#Class with config files of the project
class Config:
	def __init__(self):
		#CONTAINER NAMES
		self.context_broker_uri='http://fiware-orion-ld-container:1026/v2/entities/'
		self.context_broker_uri_ld='http://fiware-orion-ld-container:1026/ngsi-ld/v1/entities/'
		self.context_broker_types='http://fiware-orion-ld-container:1026/ngsi-ld/v1/types/'
		self.context_broker_uri_ld_local='http://localhost:1026/ngsi-ld/v1/entities/'
		self.subscription_uri='http://fiware-orion-ld-container:1026/v2/subscriptions/'
		self.subscription_uri_ld='http://fiware-orion-ld-container:1026/ngsi-ld/v1/subscriptions/'
		self.subscription_uri_ld_local='http://localhost:1026/ngsi-ld/v1/subscriptions/'
		self.api_notify_uri = "http://flask-server-container:5000/"
		self.cygnus_notify_uri_elastic = 'http://fiware-cygnus:5058/notify'
		self.cygnus_notify_uri_mongo = 'http://fiware-cygnus:5051/notify'
		self.nifi_notify_uri = 'http://nifi-container:8889/elastic'
		#GENERAL INFO
		self.region = 'Benidorm'
		self.country = 'ES'
		#SERVICE NAMES
		self.weather_observed_service = "weatherobservedaemet"
		self.wo_aemet_subs = ["dateObserved", "name", "location", "dataProvider", "source",  "description", "temperature", "feelsLikesTemperature", "relativeHumidity", "windSpeed", "windDirection", "weatherType"]
		self.walking_service = "walkingroutes"
		self.w_occ_subs = ["name", "routeType", "location", "description", "source", "dateObserved", "dataProvider", "predictiveRouteOccupancy", "url", "difficulty", "distance", "positiveSlope", "negativeSlope", "maxHeight", "minHeight", "routeTime"]
		self.w_no_occ_subs = ["name", "routeType", "location", "description", "source", "dateObserved", "dataProvider", "url", "difficulty", "distance", "positiveSlope", "negativeSlope", "maxHeight", "minHeight", "routeTime"]
		self.sea_service = "seaconditions"
		self.sc_subs= ["name", "source", "dataProvider", "location", "description","dateObserved","waveLevel","surfaceTemperature"]
		self.bikelane_service = "bikelaneconditions"
		self.bl_subs = ["dateObserved", "dataProvider", "laneOccupancy", "name", "location", "description", "source", "laneWidth", "laneLength"]
		self.beach_service = "beachconditions"
		self.beach_subs = ["dateObserved","dataProvider","occupationRate","peopleOccupancy", "name", "source", "location", "description"]
		self.aqo_service = "airqualityobserved"
		self.aqo_general_subs = ["name", "dataProvider", "source", "location", "description", "address", "dateObserved", "temperature", "relativeHumidity", "co2", "noiseLevel", "atmosphericPressure", "tvoc", "windSpeed"]
		self.aqo_aqi_service = "airqualityobservedairquality"
		self.aqo_aqi_elastic_subs = ["name", "dataProvider", "source", "location", "description", "address", "dateObserved", "airQualityIndex", "airQualityLevel", "pm10", "pm25"]
		self.aqo_aqi_api_subs = ["pm10", "pm25"]
		#MYSQL
		self.mysql_host='db-mysql-container'
		self.mysql_host_local='localhost'
		self.mysql_user='ubuntu'
		self.mysql_pw='cat123'
		self.mysql_db='nereo'
		self.walking_location_column='ST_AsText(location)'
		self.walking_routes_table = "routes_data"
		self.walking_routes_column_names = ["id", "route_name", "ST_AsText(location)", "route_type", "distance", "difficulty", "positive_slope", "negative_slope", "max_height",  "min_height", "route_time", "url"]
		self.users_table = "users"
		self.users_column_names = ["id","username","email","name","password","beach_position","bikelane_position","walking_route_position","preferences"]
		self.weather_icons_table = "weather_icons"
		self.mysql_important_fields={"mysql": ["preferences", "beach_position", "bikelane_position", "walking_route_position"],
							"class": ["usePreference", "preference_beach", "preference_bike", "preference_walk"]
							}
		#OPEN DATA
		self.aemet_api_key='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcm5hdS5pbmZhbnRlLnBpbm9zQGV2ZXJpcy5jb20iLCJqdGkiOiJlNDAwMmU2Zi1mNzVmLTQ2OTktYjI2Ni05MzQyMWQ0YzhkNTYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxMjg3NTEyOSwidXNlcklkIjoiZTQwMDJlNmYtZjc1Zi00Njk5LWIyNjYtOTM0MjFkNGM4ZDU2Iiwicm9sZSI6IiJ9.dEfRiUjHBcAPeksh0m_hPJn5t0R_8KZ1un230RSKTHE'
		self.aqicn_api_key='be256a00fc6b11f2313061e5a8b755501a21808a'
		self.aqicn_base_uri='https://api.waqi.info'
		self.aemet_wf_base_uri='https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/'
		self.aemet_beachinfo_base_uri='https://opendata.aemet.es/opendata/api/prediccion/especifica/playa/'
		self.aemet_city_weather_prediction_daily_base_uri='https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/'
		self.id_aemet_playa_levante='0303102'
		self.id_aemet_playa_poniente='0303104'
		self.id_aemet_benidorm='03031'
		self.hour_to_publish_walking = 12
		#RULE ENGINE
		self.mysql_alert_table='rules'
		self.mysql_alert_attribute_column = 'attribute_name'
		self.mysql_alert_columns = 'id, service_name, entity_type, attribute_name, operator, threshold, value_category, value_subcategory, value_severity, subscription_id, recurrence_seconds'
		#MODBUS CONNECtOR
		self.modbus_ip_server = '77.211.21.23'
		self.modbus_port_server = 502
		self.list_sensors_modbus = ["012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026"]
		#SENSORS
		self.sensor_type = {
			"-":"AM107",
			"-":"EM500-CO2",
			"-":"EM500-SMTC"
		}
		self.sensor_info = {
			"001": {"id":"WO001", "serviceName":self.weather_observed_service, "name":self.region, "description":"This pointer indicates the values from the open data portal measured in {0}.".format(self.region), "latitude":38.5410566, "longitude":-0.1224937}, #AEMET
			"002": {"id":1, "serviceName":self.walking_service, "id_provider": "WR001"},#Walking route 1
			"003": {"id":2, "serviceName":self.walking_service, "id_provider": "WR002"}, #Walking route 2
			"004": {"id":3, "serviceName":self.walking_service, "id_provider": "WR003"}, #Walking route 3
			"005": {"id":"SC001", "idAEMET":self.id_aemet_playa_levante, "serviceName":self.sea_service, "name":"Playa Levante", "nameEdited":"Playa-Levante", "latitude":38.533286, "longitude":-0.117494}, #Sea conditions playa levante
			"006": {"id":"SC002", "idAEMET":self.id_aemet_playa_poniente, "serviceName":self.sea_service, "name":"Playa Poniente", "nameEdited":"Playa-Poniente", "latitude":38.533058, "longitude":-0.151294}, #Sea conditions playa poniente
			"007": {"id":"BL001", "serviceName":self.bikelane_service, "name":"Av. de la Comunitat Valenciana, 120", "nameEdited":"Av.-de-la-Comunitat-Valenciana--120", "latitude":38.5461478, "longitude":-0.1170691, "length": 15.0, "width":3.0}, #Bike lane 1
			"008": {"id":"BL002", "serviceName":self.bikelane_service, "name":"Av. del Mediterraneo, 52", "nameEdited":"Av.-del-Mediterraneo--52", "latitude":38.536150, "longitude":-0.113632, "length": 15.0, "width":3.0}, # Bike lane 2
			"009": {"id":"BL003", "serviceName":self.bikelane_service, "name":"Av. de Europa, 25", "nameEdited":"Av.-de-Europa--25", "latitude":38.542676, "longitude":-0.120221, "length": 15.0, "width":3.0}, # Bike lane 3
			"010": {"id":"B001", "serviceName":self.beach_service, "name": "Playa Levante", "nameEdited": "Playa-Levante", "latitude":38.5350157, "longitude":-0.1171857}, #Beach playa levante
			"011": {"id":"AQO001", "serviceName":self.aqo_aqi_service, "name": "Playa Levante", "nameEdited": "Playa-Levante", "description":"This pointer indicated the information of the sensors in the beach.", "latitude":38.535736, "longitude":-0.120485}, #Beach playa levante
			#Modbus puente sensor 1 sonometro
			"012": {"id":"AQO002", "serviceName":self.aqo_service, "name": "Puente", "description":"This pointer indicates the information of the noise sensor.", "latitude":38.537575, "longitude":-0.127967, 
				"modbus": {
					"noiseLevel":1000
				}
			}, 
			#Modbus puente sensor 1
			"013": {"id":"AQO003", "serviceName":self.aqo_service, "name": "Puente", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.537139, "longitude":-0.126989, 
				"modbus": {
					"temperature":1001,
					"relativeHumidity":1002,
					"co2": 1003,
					"atmosphericPressure": 1004,
					"tvoc":1009
				}
			},
			#Modbus puente sensor 2
			"014": {"id":"AQO004", "serviceName":self.aqo_service, "name": "Puente", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.536775, "longitude":-0.126731,
				"modbus": {
					"temperature":1005,
					"relativeHumidity":1006,
					"co2": 1007,
					"atmosphericPressure": 1008,
					"tvoc":1010
				}
			}, 
			#Modbus esperanto sensor 1 wind
			"015": {"id":"AQO005", "serviceName":self.aqo_service, "name": "Esperanto", "description":"This pointer indicates the information of the wind sensor.", "latitude":38.537081, "longitude":-0.125139,
				"modbus": {
					"windSpeed": 1019
				}
			}, 
			#Modbus esperanto sensor 1 wind
			"016": {"id":"AQO006", "serviceName":self.aqo_service, "name": "Esperanto", "description":"This pointer indicates the information of the wind sensor.", "latitude":38.537081, "longitude":-0.125139,
				"modbus": {
					"windSpeed": 1020
				}
			}, 
			#Modbus esperanto sensor 1
			"017": {"id":"AQO007", "serviceName":self.aqo_service, "name": "Esperanto", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.537311, "longitude":-0.125675,
				"modbus": {
					"temperature":1011,
					"relativeHumidity":1012,
					"co2": 1013,
					"atmosphericPressure": 1014,
					"tvoc":1021
				}
			}, 
			#Modbus esperanto sensor 2
			"018": {"id":"AQO008", "serviceName":self.aqo_service, "name": "Esperanto", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.537106, "longitude":-0.125639,
				"modbus": {
					"temperature":1015,
					"relativeHumidity":1016,
					"co2": 1017,
					"atmosphericPressure": 1018,
					"tvoc":1022
				}
			},
			#Modbus Orts Llorca sensor sonometro
			"019": {"id":"AQO009", "serviceName":self.aqo_service, "name": "Orts Llorca", "description":"This pointer indicates the information of the noise sensor.", "latitude":38.537017, "longitude":-0.123594,
				"modbus": {
					"noiseLevel":1023
				}
			}, 
			#Modbus Orts Llorca sensor
			"020": {"id":"AQO010", "serviceName":self.aqo_service, "name": "Orts Llorca", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.537206, "longitude":-0.123469,
				"modbus": {
					"temperature":1024,
					"relativeHumidity":1025,
					"co2": 1026,
					"atmosphericPressure": 1027,
					"tvoc":1028
				}
			}, 
			#Modbus Emilio Romero sensor 1 wind
			"021": {"id":"AQO011", "serviceName":self.aqo_service, "name": "Emilio Romero", "description":"This pointer indicates the information of the wind sensor.", "latitude":38.536886, "longitude":-0.121842,
				"modbus": {
					"windSpeed": 1037
				}
			}, 
			#Modbus Emilio Romero sensor 1 wind
			"022": {"id":"AQO012", "serviceName":self.aqo_service, "name": "Emilio Romero", "description":"This pointer indicates the information of the wind sensor.", "latitude":38.536886, "longitude":-0.121842,
				"modbus": {
					"windSpeed": 1038
				}
			}, 
			#Modbus Emilio Romero sensor 1
			"023": {"id":"AQO013", "serviceName":self.aqo_service, "name": "Emilio Romero", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.536881, "longitude":-0.120608,
				"modbus": {
					"temperature":1029,
					"relativeHumidity":1030,
					"co2": 1031,
					"atmosphericPressure": 1032,
					"tvoc":1039
				}
			},
			#Modbus Emilio Romero sensor 2 
			"024": {"id":"AQO014", "serviceName":self.aqo_service, "name": "Emilio Romero", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.537119, "longitude":-0.121717,
				"modbus": {
					"temperature":1033,
					"relativeHumidity":1034,
					"co2": 1035,
					"atmosphericPressure": 1036,
					"tvoc":1040
				}
			}, 
			#Modbus C/Argentina sensor sonometro
			"025": {"id":"AQO015", "serviceName":self.aqo_service, "name": "C/ Argentina", "description":"This pointer indicates the information of the noise sensor.", "latitude":38.538611, "longitude":-0.147786,
				"modbus": {
					"noiseLevel":1041
				}
			},
			#Modbus C/Argentina sensor
			"026": {"id":"AQO016", "serviceName":self.aqo_service, "name": "C/ Argentina", "description":"This pointer indicates the information of the environment sensors.", "latitude":38.538611, "longitude":-0.147786,
				"modbus": {
					"temperature":1042,
					"relativeHumidity":1043,
					"co2": 1044,
					"atmosphericPressure": 1045,
					"tvoc":1046
				}
			} 
		}
		#API
		self.link_context_reference = '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
		self.aemet_environment_id = "urn:ngsi-ld:WeatherObserved:{0}:{1}".format(self.region, self.sensor_info["001"]["id"])
		self.reccomender_info ={"ids": [
									"urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(self.region, self.sensor_info["013"]["id"]), 
									"urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(self.region, self.sensor_info["005"]["nameEdited"], self.sensor_info["005"]["id"]),
									"urn:ngsi-ld:WeatherObserved:{0}:{1}".format(self.region, self.sensor_info["001"]["id"]),
									"urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(self.region, self.sensor_info["015"]["id"]),
									"urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(self.region, self.sensor_info["011"]["id"])
								],
								"fields": [
									["temperature"],
									["surfaceTemperature"], 
									["weatherType"],
									["windSpeed"], 
									["airQualityIndex"]
								],
								"services": [
									self.sensor_info["013"]["serviceName"], 
									self.sensor_info["005"]["serviceName"], 
									self.sensor_info["001"]["serviceName"], 
									self.sensor_info["015"]["serviceName"],
									self.sensor_info["011"]["serviceName"]
								]
		}
		self.reccomender_occupancy={"ids": [
				"urn:ngsi-ld:Beach:{0}:{1}:{2}".format(self.region, self.sensor_info["010"]["nameEdited"], self.sensor_info["010"]["id"]), 
				"urn:ngsi-ld:BikeLanes:{0}:{1}:{2}".format(self.region, self.sensor_info["007"]["nameEdited"], self.sensor_info["007"]["id"]),
				"urn:ngsi-ld:WakingRoutes:{0}:Ruta-Bancos-Benidorm-Te-Espera:{1}".format(self.region, self.sensor_info["002"]["id_provider"])
			],
			"fields": [
				["peopleOccupancy"],
				["laneOccupancy"],
				["predictiveRouteOccupancy"]
			],
			"services": [
				self.sensor_info["010"]["serviceName"], 
				self.sensor_info["007"]["serviceName"], 
				self.sensor_info["002"]["serviceName"]
			]
		}
		self.ids_playa_levante={"beach":"urn:ngsi-ld:Beach:{0}:{1}:{2}".format(self.region, self.sensor_info["010"]["nameEdited"], self.sensor_info["010"]["id"]),
								"seaconditions":"urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(self.region, self.sensor_info["005"]["nameEdited"], self.sensor_info["005"]["id"]),
								"environment_temp": "urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(self.region, self.sensor_info["013"]["id"]),
								"environment_aemet": self.aemet_environment_id,
								"environment_aqi": "urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(self.region, self.sensor_info["011"]["id"])
								}
		self.ids_playa_poniente={"beach":"",
								"seaconditions":"",
								"environment_temp": "",
								"environment_aemet": "",
								"environment_aqi": "",
								}
		'''self.ids_playa_poniente={"beach":"",
								"seaconditions":"urn:ngsi-ld:SeaConditions:Benidorm:Playa-Poniente:S002",
								"environment_temp": "urn:ngsi-ld:AirQualityObserved:Benidorm:AQO004",
								"environment_aemet": self.aemet_environment_id,
								"environment_aqi": "",
								}'''
		self.max_occupancy={"beach": 100,
							"bike": 20,
							"walk": 10
							}
		self.indexes = {"aqi": ["pm25","pm10"],
				"fire-forest": [""]
				}
		self.bikelane_ids ={"mediterraneo":"urn:ngsi-ld:BikeLanes:{0}:{1}:{2}".format(self.region, self.sensor_info["007"]["nameEdited"], self.sensor_info["007"]["id"]),
							"comunitat":"urn:ngsi-ld:BikeLanes:{0}:{1}:{2}".format(self.region, self.sensor_info["008"]["nameEdited"], self.sensor_info["008"]["id"]),
							"europa":"urn:ngsi-ld:BikeLanes:{0}:{1}:{2}".format(self.region, self.sensor_info["009"]["nameEdited"], self.sensor_info["009"]["id"])
							}
		self.entity_types = {
						'bikelaneconditions':'BikeLanes',
						'beachconditions':'Beach', 
						'beachpredictions':'Beach', 
						'seaconditions':'SeaConditions', 
						'walkingroutes':'WakingRoutes',
						'airqualityobserved': 'AirQualityObserved',
						'airqualityobservedairquality': 'AirQualityObserved',
						'weatherobservedaemet':'WeatherObserved',
						'alerts':'Alert'
						}