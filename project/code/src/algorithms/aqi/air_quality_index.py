import math as math
import operator

ranges_o3 = [50, 100, 130, 240, 380]
ranges_no2 = [40, 90, 120, 230, 340]
ranges_pm25 = [10, 20, 25, 50, 75]
ranges_pm10 = [20, 40, 50, 100, 150]
ranges_so2 = [100, 200, 350, 500, 750]

#AQI class with the needed values
class AQI:
	def __init__(self, agent, agent_ranges, agent_value):
		self.agent = agent
		self.agentRanges = agent_ranges
		self.value = agent_value
		self.rangeValue = 0
		self.rangeLevel = ''
		self.nextRange = 0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#This method reference the different ranges of AQI
def aqi_range(aqi_range):
    switcher = {
        1: 'very good',
        2: 'good',
        3: 'medium',
        4: 'poor',
        5: 'very poor',
    	6: 'extremely poor'
    }
    return switcher.get(aqi_range, 'invalid range')
   
#This method returns the ranges of AQI depeing on the agent
def get_agent_ranges(agent):
	switcher = {
		'o3': ranges_o3,
		'no2': ranges_no2,
		'pm25': ranges_pm25,
		'pm10': ranges_pm10,
		'so2': ranges_so2
    }
	return switcher.get(agent, 'invalid agent')

#This method calculates the current range of an agent of he AQI
def calculate_aqi_range(value_agent, ranges):
	if value_agent >= ranges[4]:
		range_aqi = 6
		next_range = value_agent-ranges[4]
	elif value_agent >= ranges[3]:
		range_aqi = 5
		next_range = ((value_agent-ranges[3])*100)/(ranges[4]-ranges[3])      
	elif value_agent >= ranges[2]:
		range_aqi = 4
		next_range = ((value_agent-ranges[2])*100)/(ranges[3]-ranges[2])
	elif value_agent >= ranges[1]:
		range_aqi = 3
		next_range = ((value_agent-ranges[1])*100)/(ranges[3]-ranges[2])  
	elif value_agent >= ranges[0]:
		range_aqi = 2
		next_range = ((value_agent-ranges[0])*100)/(ranges[2]-ranges[1])  
	else:
		range_aqi = 1
		next_range = (value_agent*100)/(ranges[1]-ranges[0])  
		
	return range_aqi, next_range

#THis method sort the list of the AQI agents depending on the range calculated
def sort_aqi_values(list_aqi_data):
    list_aqi_data.sort(key = operator.attrgetter('nextRange'), reverse = True)
    list_aqi_data.sort(key = operator.attrgetter('rangeValue'), reverse = True)
    return list_aqi_data

#This method calculates the value of the AQI depending on the list of the agents
def calculate_AQI(list_agents, list_agents_values):
	agents_ranges = []
	for agent in list_agents:
		agents_ranges.append(get_agent_ranges(agent))
	
	list_aqi_agents = []
	for i in range(0, len(list_agents)):
		agent = AQI(list_agents[i], agents_ranges[i], list_agents_values[i])
		agent.rangeValue, agent.nextRange = calculate_aqi_range(agent.value, agent.agentRanges)
		agent.rangeLevel = aqi_range(agent.rangeValue)
		list_aqi_agents.append(agent)
	
	sorted_aqi_values = sort_aqi_values(list_aqi_agents)
	
	return sorted_aqi_values[0]

#MAIN TEST
if __name__ == "__main__":
	value_o3 = 245
	value_no2 = 245
	value_pm25 = 15
	value_pm10 = 56
	value_so2 = 1000
	
	agents = ['o3', 'no2', 'pm25', 'pm10', 'so2']
	values = [value_o3, value_no2, value_pm25, value_pm10, value_so2]
	
	aqi = calculate_AQI(agents, values)
	#print(aqi)	
