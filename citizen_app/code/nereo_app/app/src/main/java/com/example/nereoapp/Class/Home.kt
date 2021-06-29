package com.example.nereoapp.Class

class Home {
    private var estado : String = ""
    private var temperatura : Int = 0
    private var humedad : Int = 0
    private var icono : String = ""

    fun Home(){}

    fun setHome(estado : String, temperatura : Int, humedad : Int, icono : String){
        this.estado = estado
        this.temperatura = temperatura
        this.humedad = humedad
        this.icono = icono
    }
    fun getEstado() : String {return estado}
    fun getTemperatura() : Int {return temperatura}
    fun getHumedad() : Int {return humedad}
    fun getIcono() : String {return icono}
}