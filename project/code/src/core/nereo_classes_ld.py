from datetime import datetime

# All classes are defined using the data models
#All changing information is from AEMET
class SeaConditions:
	def __init__(self, id_sea_conditions, beach_name, city_name, country_name, latitude, longitude):
		self.id="urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(city_name, beach_name.replace(' ', '-').replace(',', '-'), id_sea_conditions)
		self.type="SeaConditions"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": beach_name}
		self.description={"type": "Property","value": "State of the sea in {0} - {1}".format(beach_name, city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_sea_conditions}
		self.source={"type": "Property", "value": ""}
		self.waveLevel={"type": "Property", "value": 0}
		self.surfaceTemperature={"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class SeaConditionsGeneral:
	def __init__(self, id_sea_conditions, beach_name, city_name, country_name, latitude, longitude):
		self.id="urn:ngsi-ld:SeaConditions:{0}:{1}:{2}".format(city_name, beach_name.replace(' ', '-').replace(',', '-'), id_sea_conditions)
		self.type="SeaConditions"
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": beach_name}
		self.description={"type": "Property","value": "State of the sea in {0} - {1}".format(beach_name, city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_sea_conditions}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from predictive model/sensors
class Beach():
	def __init__(self, id_beach, beach_name, city_name, country_name, latitude, longitude):
		self.id="urn:ngsi-ld:Beach:{0}:{1}:{2}".format(city_name, beach_name.replace(" ","-").replace(",","-"), id_beach)
		self.type="Beach"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": beach_name}
		self.description={"type": "Property","value": "Beach information: {0} - {1}".format(beach_name, city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_beach}
		self.occupationRate={"type": "Property", "value": ""}
		self.peopleOccupancy={"type": "Property", "value": 0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from predictive model/sensors
class BeachGeneral():
	def __init__(self, id_beach, beach_name, city_name, country_name, latitude, longitude):
		self.id="urn:ngsi-ld:Beach:{0}:{1}:{2}".format(city_name, beach_name.replace(" ","-").replace(",","-"), id_beach)
		self.type="Beach"
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": beach_name}
		self.description={"type": "Property","value": "Beach information: {0} - {1}".format(beach_name, city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_beach}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from sensors
class BikeLanes():
	def __init__(self, id_lane_sensor, street_address, city_name, country_name, latitude, longitude, lane_width, lane_length):
		self.id='urn:ngsi-ld:BikeLanes:{0}:{1}:{2}'.format(city_name, street_address.replace(' ', '-').replace(',', '-'), id_lane_sensor)
		self.type='BikeLanes'
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": street_address}
		self.description={"type": "Property","value": "Bike lane information: {0} - {1}".format(street_address, city_name)}
		self.address={"type": "Property","value": {"streetAddress": street_address, "addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_lane_sensor}
		self.source={"type": "Property", "value": ""}
		self.laneOccupancy={"type": "Property", "value": 0}
		self.laneWidth={"type": "Property", "value": lane_width}
		self.laneLength={"type": "Property", "value": lane_length}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class BikeLanesGeneral():
	def __init__(self, id_lane_sensor, street_address, city_name, country_name, latitude, longitude, lane_width, lane_length):
		self.id='urn:ngsi-ld:BikeLanes:{0}:{1}:{2}'.format(city_name, street_address.replace(' ', '-').replace(',', '-'), id_lane_sensor)
		self.type='BikeLanes'
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": street_address}
		self.description={"type": "Property","value": "Bike lane information: {0} - {1}".format(street_address, city_name)}
		self.address={"type": "Property","value": {"streetAddress": street_address, "addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_lane_sensor}
		self.laneWidth={"type": "Property", "value": lane_width}
		self.laneLength={"type": "Property", "value": lane_length}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class WalkingRoutes():
	def __init__(self, id_walking_route, route_name, route_type, city_name, country_name, coordinates_line_string):
		self.id='urn:ngsi-ld:WakingRoutes:{0}:{1}:{2}'.format(city_name, route_name.replace(' ', '-').replace(',', '-'), id_walking_route)
		self.type='WakingRoutes'
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "LineString", "coordinates": coordinates_line_string}}
		self.name={"type": "Property","value": route_name}
		self.description={"type": "Propert","value": "Walking route information: {0} - {1}".format(route_name, city_name)}
		self.routeType={"type": "Property","value": route_type}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": ""}
		self.source={"type": "Property", "value": "Wikiloc"}
		self.predictiveRouteOccupancy={"type": "Property", "value": 0}
		self.url={"type": "Property", "value": ""}
		self.difficulty={"type": "Property", "value": ""}
		self.distance={"type": "Property", "value": 0.0}
		self.positiveSlope={"type": "Property", "value": 0.0}
		self.negativeSlope={"type": "Property", "value": 0.0}
		self.maxHeight={"type": "Property", "value": 0.0}
		self.minHeight={"type": "Property", "value": 0.0}
		self.routeTime={"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class WalkingRoutesGeneral():
	def __init__(self, id_walking_route, route_name, route_type, city_name, country_name, coordinates_line_string):
		self.id='urn:ngsi-ld:WakingRoutes:{0}:{1}:{2}'.format(city_name, route_name.replace(' ', '-').replace(',', '-'), id_walking_route)
		self.type='WakingRoutes'
		self.location={"type": "GeoProperty","value": {"type": "LineString", "coordinates": coordinates_line_string}}
		self.name={"type": "Property","value": route_name}
		self.description={"type": "Property","value": "Walking route information: {0} - {1}".format(route_name, city_name)}
		self.routeType={"type": "Property","value": route_type}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.source={"type": "Property", "value": "Wikiloc"}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from AEMET/sensors	
class WeatherObserved():
	def __init__(self, id_env_cond, city_name, country_name, latitude, longitude):
		self.id='urn:ngsi-ld:WeatherObserved:{0}:{1}'.format(city_name, id_env_cond)
		self.type='WeatherObserved'
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": city_name}
		self.description={"type": "Property","value": "Weather observed in {0}".format(city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_env_cond}
		self.source={"type": "Property", "value": ""}
		self.temperature={"type": "Property", "value": 0.0}
		self.relativeHumidity={"type": "Property", "value": 0.0}
		self.windSpeed={"type": "Property", "value": 0.0}
		self.windDirection={"type": "Property", "value": 0.0}
		self.weatherType={"type": "Property", "value": ""}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class WeatherObservedGeneral():
	def __init__(self, id_env_cond, city_name, country_name, name, description, latitude, longitude):
		self.id='urn:ngsi-ld:WeatherObserved:{0}:{1}'.format(city_name, id_env_cond)
		self.type='WeatherObserved'
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_env_cond}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from AEMET/sensors	
class AirQualityObserved():
	def __init__(self, id_env_cond, beach_name, city_name, country_name, latitude, longitude):
		self.id='urn:ngsi-ld:AirQualityObserved:{0}:{1}'.format(city_name, id_env_cond)
		self.type='AirQualityObserved'
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": beach_name}
		self.description={"type": "Property","value": "Air quality observed in {0}, {1}".format(beach_name, city_name)}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_env_cond}
		self.airQualityIndex={"type": "Property", "value": -1}
		self.airQualityLevel={"type": "Property", "value": ""}
		self.pm10={"type": "Property", "value": 0.0}
		self.pm25={"type": "Property", "value": 0.0}
		self.relativeHumidity={"type": "Property", "value": 0.0}
		self.temperature={"type": "Property", "value": 0.0}
		self.co2={"type": "Property", "value": 0.0}
		self.atmosphericPressure={"type": "Property", "value": 0.0}
		self.tvoc={"type": "Property", "value": 0.0}
		self.noiseLevel={"type": "Property", "value": 0.0}
		self.windSpeed={"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from AEMET/sensors	
class AirQualityObservedGeneral():
	def __init__(self, id_env_cond, city_name, country_name, name, description, latitude, longitude):
		self.id='urn:ngsi-ld:AirQualityObserved:{0}:{1}'.format(city_name, id_env_cond)
		self.type='AirQualityObserved'
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_env_cond}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#All changing information is from AEMET/sensors	
class AirQualityObservedGeneralAQI():
	def __init__(self, id_env_cond, city_name, country_name, name, description, latitude, longitude):
		self.id='urn:ngsi-ld:AirQualityObserved:{0}:{1}'.format(city_name, id_env_cond)
		self.type='AirQualityObserved'
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry": country_name,"addressLocality": city_name,"type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_env_cond}
		self.airQualityIndex={"type": "Property", "value": -1}
		self.airQualityLevel={"type": "Property", "value": ""}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class Recommendation():
	def __init__(self, user_id):
		self.id='urn:ngsi-ld:Recommendation:Benidorm'
		self.type='Recommendation'
		self.dateObserved = {"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.description={"type": "Property","value": "Result of the recommender"}
		self.userId={"type": "Property", "value": user_id}
		self.usePreferences={"type": "Property", "value": 0}
		self.firstPreference = {"type": "Property", "value": ""}
		self.secondPreference = {"type": "Property", "value": ""}
		self.thirdPreference = {"type": "Property", "value": ""}
		self.beachRecommendationResult = {"type": "Property", "value": 0.0}
		self.bikeRecommendationResult = {"type": "Property", "value": 0.0}
		self.walkRecommendationResult = {"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
