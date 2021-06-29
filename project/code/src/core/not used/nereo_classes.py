from datetime import datetime

# All classes are defined using the data models

#All changing information is from AEMET
class SeaConditions:
	def __init__(self, id_sea_conditions, beach_name, city_name, country_name, latitude, longitude):
		self.id='SeaConditions-{0}-{1}-{2}'.format(city_name, beach_name.replace(' ', '-').replace(',', '-'), id_sea_conditions)
		self.type='SeaConditions'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(beach_name)
		self.description='State of the sea in {0} - {1}'.format(beach_name, city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider='{0}'.format(id_sea_conditions)
		self.source=''
		self.waveLevel=0
		self.surfaceTemperature=0.0
		self.waveHeight=0.0
		self.wavePeriod=0.0
		self.pH=0.0
		self.salinity=0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
#All changing information is from predictive model/sensors
class Beach():
	def __init__(self, id_beach, beach_name, city_name, country_name, latitude, longitude):
		self.id='Beach-{0}-{1}-{2}'.format(city_name, beach_name.replace(' ', '-').replace(',', '-'), id_beach)
		self.type='Beach'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(beach_name)
		self.description='Beach information: {0} - {1}'.format(beach_name, city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider='{0}'.format(id_beach)
		self.source=''
		self.occupationRate=''
		self.peopleOccupancy=0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
class PredcitionBeach():
	def __init__(self, id_beach, beach_name, city_name, country_name, latitude, longitude):
		self.id='Beach-{0}-{1}-pred-{2}'.format(city_name, beach_name.replace(' ', '-').replace(',', '-'), id_beach)
		self.type='Beach'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(beach_name)
		self.description='Prediction beach information: {0} - {1}'.format(beach_name, city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider='{0}'.format(id_beach)
		self.source='Predictive-Model-Beach-Occupancy-{0}'.format(datetime.now().strftime("%d%m%Y"))
		self.occupationRate=''
		self.predictivePeopleOccupancy=0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
#All changing information is from sensors
class BikeLanes():
	def __init__(self, id_lane_sensor, street_address, city_name, country_name, latitude, longitude, lane_width, lane_length):
		self.id='BikeLanes-{0}-{1}-{2}'.format(city_name, street_address.replace(' ', '-').replace(',', '-'), id_lane_sensor)
		self.type='BikeLanes'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(street_address, city_name)
		self.description='Bike lane information: {0} - {1}'.format(street_address, city_name)
		self.address={'streetAddress': street_address,'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider='{0}'.format(id_lane_sensor)
		self.source=''
		self.laneOccupancy=0
		self.laneWidth=lane_width
		self.laneLength=lane_length
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
class WalkingRoutes():
	def __init__(self, id_walking_route, route_name, route_type, city_name, country_name, latitude, longitude):
		self.id='WakingRoutes-{0}-{1}-{2}'.format(city_name, route_name.replace(' ', '-').replace(',', '-'), id_walking_route)
		self.type='WakingRoutes'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(route_name)
		self.routeType='{0}'.format(route_type)
		self.description='Walking route information: {0} - {1}'.format(route_name, city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider=''
		self.source='Wikiloc'
		self.predictiveRouteOccupancy=0
		self.url=''
		self.difficulty=''
		self.distance=0.0
		self.positiveSlope=0.0
		self.negativeSlope=0.0
		self.maxHeight=0.0
		self.minHeight=0.0
		self.routeTime=0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
#All changing information is from AEMET/sensors	
class WeatherObserved():
	def __init__(self, id_env_cond, city_name, country_name, latitude, longitude):
		self.id='WeatherObserved-{0}-{1}'.format(city_name, id_env_cond)
		self.type='WeatherObserved'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(city_name)
		self.description='Weather observed in {0}'.format(city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider=''
		self.source=''
		self.atmosphericPressure=0.0
		self.temperature=0.0
		self.feelsLikesTemperature=0.0
		self.relativeHumidity=0.0
		self.illuminance=0.0
		self.windSpeed=0.0
		self.windDirection=0.0
		self.weatherType=''
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
#All changing information is from AEMET/sensors	
class AirQualityObserved():
	def __init__(self, id_env_cond, beach_name, city_name, country_name, latitude, longitude):
		self.id='AirQualityObserved-{0}-{1}'.format(city_name, id_env_cond)
		self.type='AirQualityObserved'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0}'.format(beach_name)
		self.description='Air quality observed in {0}, {1}'.format(beach_name, city_name)
		self.address={'addressCountry':country_name, 'addressLocality':city_name}
		self.dataProvider=''
		self.source=''
		self.airQualityIndex=0
		self.airQualityLevel=''
		self.no2=0.0
		self.o3=0.0
		self.so2=0.0
		self.pm10=0.0
		self.pm25=0.0
		self.relativeHumidity=0.0
		self.temperature=0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
class Anomaly():
	def __init__(self):
		self.id=''
		self.type='Anomaly'
		self.detectedBy=''
		self.anomalousProperty=''
		self.dateDetected=''
		self.thresholdBreach=[]
		self.dataProvider=''
		self.source=''
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
class Recommendation():
	def __init__(self, user_id):
		self.id='Recommendation-{0}'.format(user_id)
		self.userId=user_id
		self.type='Recommendation'
		self.description='Result of the recommender'
		self.usePreferences=1
		self.dateObserved = ''
		self.firstPreference = ''
		self.secondPreference = ''
		self.thirdPreference = ''
		self.beachRecommendationResult = 0.0
		self.bikeRecommendationResult = 0.0
		self.walkRecommendationResult = 0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
