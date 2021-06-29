package com.example.nereoapp.Class

class Beach {
    private var population : Int = 0
    private var occupationRate : String = ""
    private var temperatura : Int = 0
    private var waves : Int = 0
    private var water_temperature : Int = 0
    private var humidity : Int = 0
    private var wind_speed : Int = 0
    private var wind_direction : Int = 0
    private var airQuality : Int = 0
    private var airIndex : String = ""
    private var lat : Double = 0.0
    private var lng : Double = 0.1


    fun Beach(){}

    fun setBeach(population: Int, occupationRate: String, lat : Double, lng : Double, waves: Int, temperatura: Int, water_temperature: Int, humidity: Int, wind_speed: Int, wind_direction: Int, airQuality: Int, airIndex : String){
        this.population = population
        this.lat = lat
        this.lng = lng
        this.occupationRate = occupationRate
        this.temperatura = temperatura
        this.waves = waves
        this.water_temperature = water_temperature
        this.humidity = humidity
        this.wind_speed = wind_speed
        this.wind_direction = wind_direction
        this.airQuality = airQuality
        this.airIndex = airIndex
    }
    fun getPopulation(): Int {return population}
    fun getLat() : Double {return lat}
    fun getLng() : Double {return lng}
    fun getTemperatura(): Int {return temperatura}
    fun getWaves(): Int {return waves}
    fun getWater_temperature(): Int {return water_temperature}
    fun getHumidity(): Int {return humidity}
    fun getWind_Speed(): Int {return wind_speed}
    fun getWind_direction(): Int {return wind_direction}
    fun getAirQuality(): Int {return airQuality}
    fun getAirIndex() : String {return airIndex}

}