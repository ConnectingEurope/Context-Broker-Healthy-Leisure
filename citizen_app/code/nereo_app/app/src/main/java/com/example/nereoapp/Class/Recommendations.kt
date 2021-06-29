package com.example.nereoapp.Class

class Recommendations {
    private var beach_perc : Double = 0.0
    private var bike_perc : Double = 0.0
    private var street_perc : Double = 0.0

    fun Recommendations(){}

    fun setRecommendations(beach_perc : Double, bike_perc : Double, street_perc : Double){
        this.beach_perc = beach_perc
        this.bike_perc = bike_perc
        this.street_perc = street_perc
    }
    fun getBeach_perc() : Double {return beach_perc}
    fun getBike_perc() : Double {return bike_perc}
    fun getStreet_perc() : Double {return street_perc}
}