package com.example.nereoapp.Fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.preference.PreferenceManager
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.nereoapp.Class.Beach
import com.example.nereoapp.BuildConfig
import com.example.nereoapp.R
import kotlinx.android.synthetic.main.fragment_beach.view.*
import kotlinx.android.synthetic.main.fragment_beach.view.openmapview
import okhttp3.*
import org.json.JSONObject
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapController
import org.osmdroid.views.overlay.Marker
import java.io.IOException

class BeachFragment : Fragment() {
    val client = OkHttpClient()
    var Levante : Beach = Beach()
    var Poniente : Beach = Beach()
    var urllevante = "http://your_api_url" //Copy here the API URL
    var urlPoniente = "http://your_api_url" //Copy here the API URL


    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        val v : View = inflater.inflate(R.layout.fragment_beach, container, false)
        Configuration.getInstance().load(context, PreferenceManager.getDefaultSharedPreferences(context))
        Configuration.getInstance().userAgentValue = BuildConfig.APPLICATION_ID
        var myMapController: MapController = v.openmapview.controller as MapController
        v.openmapview.setMultiTouchControls(true)
        v.openmapview.setTileSource(TileSourceFactory.MAPNIK)
        var startMarker : Marker = Marker(v.openmapview)
        myMapController.setZoom(17)
        v.openmapview.setMultiTouchControls(true)
        val lista = resources.getStringArray(R.array.playas)
        val adaptador = activity?.let { ArrayAdapter(it, android.R.layout.simple_spinner_item, lista) }
        v.beachSpinner.adapter = adaptador

        //Set data to text views
        v.beachSpinner.onItemSelectedListener = object:
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>?,
                view: View?,
                position: Int,
                id: Long
            ) {
                when (lista[position]) {
                    "PLAYA DE LEVANTE" ->{
                        fetchJson(urllevante, 1, v, myMapController, startMarker)
                    }
                    "PLAYA DE PONIENTE" ->{
                        fetchJson(urlPoniente, 2, v, myMapController, startMarker)
                    }
                }
            }
            override fun onNothingSelected(parent: AdapterView<*>?) {
                TODO("Not yet implemented")
            }
        }
        // Inflate the layout for this fragment
        return v
    }
    fun fetchJson(url: String, contador: Int, v: View, myMapController: MapController, startMarker: Marker){
        val request = Request.Builder().url(url).build()
        client.newCall(request).enqueue(object : Callback{
            override fun onFailure(call: Call, e: IOException) {
                Log.i("fail", "Error")
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonobj = JSONObject(body)
                if (contador == 1){
                    if(jsonobj.getJSONArray("location").length() == 0){
                        Levante.setBeach(jsonobj.getInt("peopleOccupancy"), jsonobj.getString("occupationRate"), 0.0, 0.0, jsonobj.getInt("waveLevel"), jsonobj.getInt("surfaceTemperature"), jsonobj.getInt("temperature"), jsonobj.getInt("relativeHumidity"), jsonobj.getInt("windSpeed"), jsonobj.getInt("windDirection"), jsonobj.getInt("aqiValue"), jsonobj.getString("aqiIndex"))
                    }else {
                        Levante.setBeach(jsonobj.getInt("peopleOccupancy"), jsonobj.getString("occupationRate"), jsonobj.getJSONArray("location").getDouble(1), jsonobj.getJSONArray("location").getDouble(0), jsonobj.getInt("waveLevel"), jsonobj.getInt("surfaceTemperature"), jsonobj.getInt("temperature"), jsonobj.getInt("relativeHumidity"), jsonobj.getInt("windSpeed"), jsonobj.getInt("windDirection"), jsonobj.getInt("aqiValue"), jsonobj.getString("aqiIndex"))
                    }
                    if(Levante.getPopulation()<0){
                        v.population.text = "NO DATA"
                        v.temperatureBeach.text ="NO DATA"
                        v.wavesBeach.text = "NO DATA"
                        v.waterTempBeach.text = "NO DATA"
                        v.humidityBeach.text = "NO DATA"
                        v.windBeach.text = "NO DATA"
                        v.airQBeach.text = "NO DATA"
                    }else{
                        if (Levante.getPopulation()<30){
                            v.ocupation.setBackgroundResource(R.drawable.circle_green)
                        }else if (Levante.getPopulation() in 30..69){
                            v.ocupation.setBackgroundResource(R.drawable.circle_yellow)
                        }else{
                            v.ocupation.setBackgroundResource(R.drawable.circle_red)
                        }
                        v.population.text = Levante.getPopulation().toString()+" / 2000"
                        v.temperatureBeach.text = Levante.getWater_temperature().toString()+"ºC"
                        v.wavesBeach.text = "Degree"+Levante.getWaves().toString()
                        v.waterTempBeach.text = Levante.getTemperatura().toString()+"ºC"
                        v.humidityBeach.text = Levante.getHumidity().toString()+"%"
                        v.windBeach.text = Levante.getWind_direction().toString()+"/"+Levante.getWind_Speed().toString()+"km/h"
                        v.airQBeach.text = Levante.getAirQuality().toString()+"/"+Levante.getAirIndex()
                        Handler(Looper.getMainLooper()).post {
                            run {
                                myMapController.setCenter(GeoPoint(Levante.getLat(), Levante.getLng()))
                                startMarker.position = GeoPoint(Levante.getLat(), Levante.getLng())
                                startMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
                                v.openmapview.overlays.add(startMarker)
                            }
                        }
                    }
                }
                if (contador == 2){
                    if(jsonobj.getJSONArray("location").length() == 0){
                        Poniente.setBeach(jsonobj.getInt("peopleOccupancy"), jsonobj.getString("occupationRate"),0.0, 0.0, jsonobj.getInt("waveLevel"), jsonobj.getInt("surfaceTemperature"), jsonobj.getInt("temperature"), jsonobj.getInt("relativeHumidity"), jsonobj.getInt("windSpeed"), jsonobj.getInt("windDirection"), jsonobj.getInt("aqiValue"), jsonobj.getString("aqiIndex"))
                    }else {
                        Poniente.setBeach(jsonobj.getInt("peopleOccupancy"), jsonobj.getString("occupationRate"), jsonobj.getJSONArray("location").getDouble(0), jsonobj.getJSONArray("location").getDouble(1), jsonobj.getInt("waveLevel"), jsonobj.getInt("surfaceTemperature"), jsonobj.getInt("temperature"), jsonobj.getInt("relativeHumidity"), jsonobj.getInt("windSpeed"), jsonobj.getInt("windDirection"), jsonobj.getInt("aqiValue"), jsonobj.getString("aqiIndex"))
                    }
                        if(Poniente.getPopulation()<0){
                            v.population.text = "NO DATA"
                            v.temperatureBeach.text ="NO DATA"
                            v.wavesBeach.text = "NO DATA"
                            v.waterTempBeach.text = "NO DATA"
                            v.humidityBeach.text = "NO DATA"
                            v.windBeach.text = "NO DATA"
                            v.airQBeach.text = "NO DATA"
                    }else{
                        if (Poniente.getPopulation()<30){
                            v.ocupation.setBackgroundResource(R.drawable.circle_green)
                        }else if (Poniente.getPopulation() in 30..69){
                            v.ocupation.setBackgroundResource(R.drawable.circle_yellow)
                        }else{
                            v.ocupation.setBackgroundResource(R.drawable.circle_red)
                        }
                        v.population.text = Poniente.getPopulation().toString()+" / 2000"
                            v.temperatureBeach.text = Poniente.getWater_temperature().toString()+"ºC"
                            v.wavesBeach.text = "Degree"+Poniente.getWaves().toString()
                            v.waterTempBeach.text = Poniente.getTemperatura().toString()+"ºC"
                            v.humidityBeach.text = Poniente.getHumidity().toString()+"%"
                            v.windBeach.text = Poniente.getWind_direction().toString()+"/"+Poniente.getWind_Speed().toString()+"m/s"
                            v.airQBeach.text = Poniente.getAirQuality().toString()+"/"+Poniente.getAirIndex()
                            Handler(Looper.getMainLooper()).post {
                                run {
                                    myMapController.setCenter(GeoPoint(Poniente.getLat(), Poniente.getLng()))
                                    startMarker.position = GeoPoint(Poniente.getLat(), Poniente.getLng())
                                    startMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
                                    v.openmapview.overlays.add(startMarker)
                                }
                            }
                    }
                }
            }
        })
    }
}