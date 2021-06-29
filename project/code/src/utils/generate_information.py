import config.config as cnf
import datetime
import pytz
import random

config = cnf.Config()
aemet_wave_low=310
aemet_wave_medium=320
aemet_wave_high=330
first_period = '00-24'
second_period = '12-24'
third_period = '12-18'

# Function that parses the aemet wave level to Douglas scale
def generate_wave_level(aemet_wave_level):
	if aemet_wave_level==aemet_wave_low:
		douglas_wave_level=random.randint(0, 2)
	elif aemet_wave_level==aemet_wave_medium:
		douglas_wave_level=random.randint(3, 6)
	else:
		douglas_wave_level=random.randint(7, 10)
		
	return douglas_wave_level

# FUnction that parses the aemet wind direction to a number
def generate_wind_direction(aemet_wind_direction):
	switcher={
		"N":0,
		"NE":45,
		"E":90,
		"SE":135,
		"S":180,
		"SO":-135,
		"O":-90,
		"NO":-45
		}
	
	return switcher.get(aemet_wind_direction, 0)

# Functions that generates a random value of air quality index
def generate_air_quality_index_random(datetime_hour):
	if(datetime_hour.hour < 7):
		air_quality_index= random.randint(0, 75)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		air_quality_index= random.randint(50, 100)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		air_quality_index= random.randint(50, 150)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		air_quality_index= random.randint(50, 100)	
	else:
		air_quality_index= random.randint(0, 75)
	
	return air_quality_index

# Functions that generates a random value of air quality index for no2 -> 0-229
def generate_random_no2(datetime_hour): 
	if(datetime_hour.hour < 7):
		no2= random.randint(0, 75)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		no2= random.randint(50, 100)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		no2= random.randint(100, 229)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		no2= random.randint(50, 100)	
	else:
		no2= random.randint(0, 75)
	
	return no2

def generate_random_so2(datetime_hour): 
	if(datetime_hour.hour < 7):
		so2= random.randint(0, 75)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		so2= random.randint(50, 100)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		so2= random.randint(100, 229)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		so2= random.randint(50, 100)	
	else:
		so2= random.randint(0, 75)
	
	return so2

# Functions that generates a random value of air quality index for o3 -> 0-239
def generate_random_o3(datetime_hour): 
	if(datetime_hour.hour < 7):
		o3= random.randint(0, 100)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		o3= random.randint(100, 150)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		o3= random.randint(150, 239)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		o3= random.randint(100, 175)	
	else:
		o3= random.randint(0, 50)
	
	return o3

# Functions that generates a random value of air quality index for pm10 -> 0-150+
def generate_random_pm10(datetime_hour): 
	if(datetime_hour.hour < 7):
		pm10= random.randint(0, 10)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		pm10= random.randint(10, 20)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		pm10= random.randint(20, 150)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		pm10= random.randint(20, 40)	
	else:
		pm10= random.randint(0, 20)
	
	return pm10

# Functions that generates a random value of air quality index for pm25 -> 0-75+
def generate_random_pm25(datetime_hour): 
	if(datetime_hour.hour < 7):
		pm25= random.randint(0, 10)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		pm25= random.randint(30, 40)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		pm25= random.randint(20, 75)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		pm25= random.randint(20, 40)	
	else:
		pm25= random.randint(0, 20)
	
	return pm25

def generate_sea_temperature_random(datetime_hour):
	if(datetime_hour.hour < 7):
		sea_temperature= random.randint(12, 14)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		sea_temperature= random.randint(13, 15)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		sea_temperature= random.randint(14, 16)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		sea_temperature= random.randint(13, 15)	
	else:
		sea_temperature= random.randint(12, 15)
	
	return sea_temperature

def generate_temperature_random(datetime_hour):
	if(datetime_hour.hour < 7):
		temperature= random.randint(5, 15)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		temperature= random.randint(20, 30)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		temperature= random.randint(25, 35)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		temperature= random.randint(20, 30)	
	else:
		temperature= random.randint(15, 25)
	
	return temperature

def generate_humidity_random(datetime_hour):
	if(datetime_hour.hour < 7):
		humidity= random.randint(50, 80)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		humidity= random.randint(0, 10)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		humidity= random.randint(0, 15)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		humidity= random.randint(20, 40)	
	else:
		humidity= random.randint(10, 30)
	
	return humidity

def generate_wind_speed_random(datetime_hour):
	if(datetime_hour.hour < 7):
		wind_speed = random.randint(0, 8)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		wind_speed= random.randint(5, 20)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		wind_speed= random.randint(10, 20)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		wind_speed= random.randint(0, 12)	
	else:
		wind_speed= random.randint(0, 20)
	
	return wind_speed

def generate_wind_dir_random():
	wind_direction_list = [0, 45, 90, 135, 180, -135, -90, -45]
	wind_direction = random.choice(wind_direction_list)
	
	return wind_direction

def generate_weather_type_random():
	weather_type_list = ['11', '12', '14', '17', '15', '11', '11', '11']
	weather_type = convert_AEMET_skystate(random.choice(weather_type_list))
	
	return weather_type
	
#Function that assings an air quality index in a descriptive way
def generate_air_quality_index(air_quality_index):
	if air_quality_index <= 50:
		descriptive_air_quality_index = 'good'
	elif air_quality_index > 50 & air_quality_index <= 100:
		descriptive_air_quality_index = 'moderate'
	elif air_quality_index > 100 & air_quality_index <= 150:
		descriptive_air_quality_index = 'unhealthy for sensitive groups'
	elif air_quality_index > 150 & air_quality_index <= 200:
		descriptive_air_quality_index = 'unhealthy'
	elif air_quality_index > 200 & air_quality_index <= 300:
		descriptive_air_quality_index = 'very unhealthy'
	elif air_quality_index > 300:	
		descriptive_air_quality_index = 'hazardous'

	return descriptive_air_quality_index

# Function that parses the beach occupacy number to string scale
def generate_beach_occupation_rate(beach_occupation_number):
	if beach_occupation_number == 0:
		occupation_rate='none'
	elif beach_occupation_number > 0 and beach_occupation_number <= 10:
		occupation_rate='low'
	elif beach_occupation_number > 10 and beach_occupation_number <= 50:
		occupation_rate='medium'
	else:
		occupation_rate='high'
		
	return occupation_rate

# Function that converts the datetime of AEMET to ISO 8601
def convert_datetime_aemet(string_datetime):
	datetime_spain = pytz.timezone("Europe/Madrid")
	AEMET_datetime = datetime.datetime.strptime(string_datetime, '%Y-%m-%dT%H:%M:%S')
	AEMET_datetime_tz = pytz.timezone('Europe/Madrid').localize(AEMET_datetime)
	AEMET_datetime_iso = AEMET_datetime_tz.isoformat()

	return AEMET_datetime_iso

# Functions that generates a datetime from now to ISO 8601
def datetime_time_tz():
	datetime_spain = pytz.timezone("Europe/Madrid")
	datetime_now = datetime.datetime.now(datetime_spain)
	datetime_now_no_micro = datetime_now.replace(microsecond=0)
	string_now_tz = datetime_now_no_micro.isoformat()
	
	return string_now_tz, datetime_now_no_micro

# Function that converts the number of state of the sky from AEMET to a descriptive state of the sky
def convert_AEMET_skystate(sky_state_number):
	switcher={
		"11":"despejado",
		"11n":"despejado noche",
		"12":"poco nuboso",
		"12n":"poco nuboso noche",
		"13":"intervalos nubosos",
		"13n":"intervalos nubosos noche",
		"14":"nuboso",
		"14n":"nuboso noche",
		"15":"muy nuboso",
		"15n":"muy nuboso noche",
		"16":"cubierto",
		"16n":"cubierto noche",
		"17":"nubes altas",
		"17n":"nubes altas noche",
		"23":"intervalos nubosos con lluvia",
		"23n":"intervalos nubosos con lluvia noche",
		"24":"nuboso con lluvia",
		"24n":"nuboso con lluvia noche",
		"25":"muy nuboso con lluvia",
		"25n":"muy nuboso con lluvia noche",
		"26":"cubierto con lluvia",
		"26n":"cubierto con lluvia noche",
		"33":"intervalos nubosos con nieve",
		"33n":"intervalos nubosos con nieve noche",
		"34":"nuboso con nieve",
		"34n":"nuboso con nieve noche",
		"35":"muy nuboso con nieve",
		"35n":"muy nuboso con nieve noche",
		"36":"cubierto con nieve",
		"36n":"cubierto con nieve noche",
		"43":"intervalos nubosos con lluvia escasa",
		"43n":"intervalos nubosos con lluvia escasa noche",
		"44":"nuboso con lluvia escasa",
		"44n":"nuboso con lluvia escasa noche",
		"45":"muy nuboso con lluvia escasa",
		"45n":"muy nuboso con lluvia escasa noche",
		"46":"cubierto con lluvia escasa",
		"46n":"cubierto con lluvia escasa noche",
		"51":"intervalos nubosos con tormenta",
		"51n":"intervalos nubosos con tormenta noche",
		"52":"nuboso con tormenta",
		"52n":"nuboso con tormenta noche",
		"53":"muy nuboso con tormenta",
		"53n":"muy nuboso con tormenta noche",
		"54":"cubierto con tormenta",
		"54n":"cubierto con tormenta noche",
		"61":"intervalos nubosos con tormenta y lluvia escasa",
		"61n":"intervalos nubosos con tormenta y lluvia escasa noche",
		"62":"nuboso con tormenta y lluvia escasa",
		"62n":"nuboso con tormenta y lluvia escasa noche",
		"63":"muy nuboso con tormenta y lluvia escasa",
		"63n":"muy nuboso con tormenta y lluvia escasa noche",
		"64":"cubierto con tormenta y lluvia escasa",
		"64n":"cubierto con tormenta y lluvia escasa noche",
		"71":"intervalos nubosos con nieve escasa",
		"71n":"intervalos nubosos con nieve escasa noche",
		"72":"nuboso con nieve escasa",
		"72n":"nuboso con nieve escasa noche",
		"73":"muy nuboso con nieve escasa",
		"73n":"muy nuboso con nieve escasa noche",
		"74":"cubierto con nieve escasa",
		"74n":"cubierto con nieve escasa noche",
		"81":"niebla",
		"82":"bruma",
		"83":"calima",
		}

	return switcher.get(sky_state_number, "despejado")

# Functions that ensures the data from some AEMET aparameters, it checks if the parameter is not empty
def find_aemet_prediction_data(array_aemet, period_parameter, check_parameter, save_parameter):
	period_used = ""
	prediction_value = ""
	
	for aemet_element in array_aemet:
		if aemet_element[period_parameter] == first_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(first_period, aemet_element[check_parameter]))
			else:
				period_used = first_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(first_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
		elif aemet_element[period_parameter] == second_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(second_period, aemet_element[check_parameter]))
			else:
				period_used = second_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(second_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
			
		elif aemet_element[period_parameter] == third_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(third_period, aemet_element[check_parameter]))
			else:
				period_used = third_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(third_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
	
	return period_used, prediction_value
