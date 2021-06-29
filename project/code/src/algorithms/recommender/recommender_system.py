import algorithms.recommender.grades as grades

#This class contains the needed parameters to calculate the recommender system
class RecommendationSystem():
    def __init__(self, temperature, water_temperature, state_of_sky, wind_speed, occupancy, aqi, use_preference, preference_number):
        self.temperature = temperature
        self.surfaceTemperature = water_temperature
        self.weatherType = state_of_sky
        self.windSpeed = wind_speed
        self.peopleOccupancy = occupancy
        self.airQualityIndex = aqi
        self.usePreference = use_preference
        self.preferenceNumber = preference_number
        self.recommendation_result = 0.0
    
    #This method calculate the recommendation value for the beach
    def grade_beach_recommendation(self):
        temperature_grade = grades.grade_temperature_beach(self.temperature)
        water_temperature_grade = grades.grade_water_temperature(self.surfaceTemperature)
        state_of_sky_grade = grades.grade_state_of_sky(self.weatherType)
        wind_speed_grade = grades.grade_wind_beach(self.windSpeed)
        occupancy_grade = grades.grade_occupancy(self.peopleOccupancy)
        aqi_grade = grades.grade_air_quality(self.airQualityIndex)
        
        final_grade = 0.35 * temperature_grade + 0.1 * water_temperature_grade + 0.2 * state_of_sky_grade + 0.15 * wind_speed_grade + 0.1 * aqi_grade + 0.1 * occupancy_grade
        add_value = 0.0
                
        if self.usePreference == 1:
            if isinstance(self.preferenceNumber, int):
                if self.preferenceNumber == 1:
                    add_value=1.0
                elif self.preferenceNumber == 2:
                    add_value=0.0
                elif self.preferenceNumber == 3:
                    add_value=-1.0
                else:
                    add_value=0.0
            else:
                exception_message = "The user is not well configured. The user has enabled the use of preference, but they are not properly configured: '{0}' -> '{1}'".format(self.preferenceNumber, type(self.preferenceNumber))
                raise Exception(exception_message)
                
        final_grade = final_grade + add_value
        
        if final_grade < 0:
            final_grade = 0.0
        elif final_grade > 10:
            final_grade = 10.0

        self.recommendation_result = float("{:.2f}".format(final_grade)) 

    #This method calculate the recommendation value for the bike
    def grade_bike_recommendation(self):
        temperature_grade = grades.grade_temperature(self.temperature)
        state_of_sky_grade = grades.grade_state_of_sky(self.weatherType)
        wind_speed_grade = grades.grade_wind(self.windSpeed)
        occupancy_grade = grades.grade_occupancy(self.peopleOccupancy)
        aqi_grade = grades.grade_air_quality(self.airQualityIndex)
        final_grade = 0.45 * temperature_grade + 0.2 * state_of_sky_grade + 0.15 * wind_speed_grade + 0.1 * aqi_grade + 0.1 * occupancy_grade
        add_value = 0.0
        
        if self.usePreference == 1:
            if isinstance(self.preferenceNumber, int):
                if self.preferenceNumber == 1:
                    add_value=1.0
                elif self.preferenceNumber == 2:
                    add_value=0.0
                elif self.preferenceNumber == 3:
                    add_value=-1.0
                else:
                    add_value=0.0
            else:
                exception_message = "The user is not well configured. The user has enabled the use of preference, but they are not properly configured: '{0}' -> '{1}'".format(self.preferenceNumber, type(self.preferenceNumber))
                raise Exception(exception_message)
                
        final_grade = final_grade + add_value

        if final_grade < 0:
            final_grade = 0.0
        elif final_grade > 10:
            final_grade = 10.0

        self.recommendation_result = float("{:.2f}".format(final_grade))
       
    #This method calculate the recommendation value for the walk
    def grade_walk_recommendation(self):
        temperature_grade = grades.grade_temperature(self.temperature)
        state_of_sky_grade = grades.grade_state_of_sky(self.weatherType)
        wind_speed_grade = grades.grade_wind(self.windSpeed)
        aqi_grade = grades.grade_air_quality(self.airQualityIndex)
        final_grade = 0.45 * temperature_grade + 0.2 * state_of_sky_grade + 0.25 * wind_speed_grade + 0.1 * aqi_grade
        add_value = 0.0
        
        if self.usePreference == 1:
            if isinstance(self.preferenceNumber, int):
                if self.preferenceNumber == 1:
                    add_value=1.0
                elif self.preferenceNumber == 2:
                    add_value=0.0
                elif self.preferenceNumber == 3:
                    add_value=-1.0
                else:
                    add_value=0.0
            else:
                exception_message = "The user is not well configured. The user has enabled the use of preference, but they are not properly configured: '{0}' -> '{1}'".format(self.preferenceNumber, type(self.preferenceNumber))
                raise Exception(exception_message)
        
        final_grade = final_grade + add_value

        if final_grade < 0:
            final_grade = 0.0
        elif final_grade > 10:
            final_grade = 10.0

        self.recommendation_result = float("{:.2f}".format(final_grade))
        
