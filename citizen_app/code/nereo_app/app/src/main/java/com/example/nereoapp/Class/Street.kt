package com.example.nereoapp.Class

import org.osmdroid.util.GeoPoint

class Street {
    private var id : Int = 0
    private var route_name : String = ""
    private var dificulty : String = ""
    private var distance : Double = 0.0
    private var slope : Double = 0.0
    private var height : Double = 0.0
    private var locations : ArrayList<GeoPoint> = ArrayList()

    fun Street(){}
    fun setStreet(id: Int, route_name: String, dificulty: String, distance: Double, slope: Double, height: Double, locations : ArrayList<GeoPoint>){
        this.id = id
        this.route_name = route_name
        this.dificulty = dificulty
        this.distance = distance
        this.slope = slope
        this.height = height
        this.locations = locations
    }
    fun getId() : Int{return id}
    fun getRouteName() : String{return route_name}
    fun getDificulty() : String {return dificulty}
    fun getDistance() : Double {return distance}
    fun getSlope() : Double {return slope}
    fun getHeight() : Double {return height}
    fun getLocations() : ArrayList<GeoPoint> {return locations}
}