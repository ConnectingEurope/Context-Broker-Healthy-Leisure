package com.example.nereoapp.Class

import org.osmdroid.util.GeoPoint

class Bike {
    private var id : String = ""
    private var population : Int = 0

    fun Bike(){}

    fun setBike(id : String, population : Int){
        this.id = id
        this.population = population
    }
    fun getId(): String {return id}
    fun getPopulation() : Int {return population}
}