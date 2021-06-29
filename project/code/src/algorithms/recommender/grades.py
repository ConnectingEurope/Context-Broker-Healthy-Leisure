#This methods returns different grades depeding on analyzed parameter
def grade_wind_beach(wind_speed):
    if wind_speed < 15:
        return 10
    else:
        return downwardQuadraticFunction(0.2, wind_speed, 15, 10)
        
def grade_wind(wind_speed):
    if wind_speed < 30:
        return 10
    else:
        return downwardQuadraticFunction(0.2, wind_speed, 30, 10)
        
def grade_water_temperature(water_temperature):
    return downwardQuadraticFunction(0.1, water_temperature, 22, 10 )
        
def grade_temperature_beach(temperature):
    if temperature >= 23:
        return downwardQuadraticFunction(0.07, temperature, 23, 10)
    else:
        return downwardQuadraticFunction(0.2, temperature,23, 10)

def grade_temperature(temperature):
    return downwardQuadraticFunction(0.1, temperature, 22.5, 10)
        
def grade_air_quality(aqi):
	grade = 0
	
	if aqi == 1:
		grade = 10
	elif aqi == 2:
		grade = 5
	elif aqi == 3:
		grade = 0
	elif aqi == 4:
		grade = -4
	elif aqi == 5:
		grade = -8
	elif aqi == 6:
		grade = -10
		
	return grade    
        
def grade_state_of_sky(state_of_sky):
    grade = 0
	
    if state_of_sky == 'despejado':
        grade = 10
    elif state_of_sky == 'nubes altas': 
        grade = 9
    elif state_of_sky == 'poco nuboso':
        grade = 8
    elif state_of_sky == 'intervalo nuboso':
        grade = 7
    elif state_of_sky == 'nuboso':
        grade = 4
    elif state_of_sky == 'muy nuboso':
        grade = 2
    else:
        grade = 0
        
    return grade
        
def grade_occupancy(occupancy):
    if occupancy < 55:
        return  10
    else:
        return downwardQuadraticFunction(0.01, occupancy, 55, 10)


def downwardQuadraticFunction(a, value, vertex, max_grade):
    return -(a*(value-vertex)**2)+max_grade