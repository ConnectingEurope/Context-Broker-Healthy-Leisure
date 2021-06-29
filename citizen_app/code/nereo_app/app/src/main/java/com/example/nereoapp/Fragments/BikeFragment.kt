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
import androidx.fragment.app.Fragment
import com.example.nereoapp.BuildConfig
import com.example.nereoapp.Class.Bike
import com.example.nereoapp.R
import kotlinx.android.synthetic.main.fragment_beach.view.*
import kotlinx.android.synthetic.main.fragment_bike.view.*
import kotlinx.android.synthetic.main.fragment_bike.view.ocupation
import kotlinx.android.synthetic.main.fragment_bike.view.openmapview
import okhttp3.*
import org.json.JSONArray
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapController
import org.osmdroid.views.overlay.Marker
import org.osmdroid.views.overlay.Polyline
import java.io.IOException

class BikeFragment : Fragment() {
    val client = OkHttpClient()
    private var Com_Val : Bike = Bike()
    private var Mediterraneo : Bike = Bike()
    private var Europa : Bike = Bike()
    private var urlcom_val : String = "http://your_api_url" //Copy here the API URL
    private var urlmediterraneo : String = "http://your_api_url" //Copy here the API URL
    private var urleuropa : String = "http://your_api_url" //Copy here the API URL

    private var Com_Val_Start = GeoPoint(38.5609, -0.0976)
    private var Com_val_End = GeoPoint(38.5414, -0.1232)
    private var Mediterraneo_Start = GeoPoint(38.5345, -0.1072)
    private var Mediterraneo_Mid = GeoPoint(38.5356, -0.1101)
    private var Mediterraneo_End = GeoPoint(38.5371, -0.1257)
    private var Europa_Start = GeoPoint(38.5818, -0.0703)
    private var Europa_End = GeoPoint(38.5687, -0.0875)
    var geopoints : ArrayList<GeoPoint> = ArrayList<GeoPoint>()
    var line : Polyline = Polyline()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        val v : View = inflater.inflate(R.layout.fragment_bike, container, false)
        Configuration.getInstance().load(context, PreferenceManager.getDefaultSharedPreferences(context))
        Configuration.getInstance().userAgentValue = BuildConfig.APPLICATION_ID
        var myMapController: MapController = v.openmapview.controller as MapController
        v.openmapview.setBuiltInZoomControls(true)
        v.openmapview.setMultiTouchControls(true)
        v.openmapview.setTileSource(TileSourceFactory.MAPNIK)
        myMapController.setZoom(17)

        val lista = resources.getStringArray(R.array.calles)
        val adaptador = activity?.let { ArrayAdapter(it, android.R.layout.simple_spinner_item, lista) }
        v.spinner.adapter = adaptador
        v.spinner.onItemSelectedListener = object:
            AdapterView.OnItemSelectedListener{
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                when(lista[position]) {
                    "Av. Comunitat Valenciana" -> {
                        fetchJson(urlcom_val, 1, v, myMapController)
                    }
                    "Av. del Mediterraneo" -> {
                        fetchJson(urlmediterraneo, 2, v, myMapController)
                    }
                    "Av. Europa" -> {
                        fetchJson(urleuropa, 3, v, myMapController)
                    }
                }
            }
            override fun onNothingSelected(parent: AdapterView<*>?) {
                fetchJson(urlcom_val, 1, v, myMapController)
            }
        }
        return v
    }
    fun fetchJson(url: String, contador: Int, v: View, myMapController: MapController){
        val request = Request.Builder().url(url).build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.i("fail", "Error")
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonarr = JSONArray(body)
                val jsonobj = jsonarr.getJSONObject(0)
                if (contador == 1){
                    Com_Val.setBike(jsonobj.getString("id"), jsonobj.getInt("laneOccupancy"))
                    if (Com_Val.getPopulation()<0) {
                        v.populationBike.text = "NO DATA AVAIABLE"
                    }else{
                        if (Com_Val.getPopulation()<30){
                            v.ocupation.setBackgroundResource(R.drawable.circle_green)
                        }else if (Com_Val.getPopulation() in 30..69){
                            v.ocupation.setBackgroundResource(R.drawable.circle_yellow)
                        }else{
                            v.ocupation.setBackgroundResource(R.drawable.circle_red)
                        }
                        v.populationBike.text= Com_Val.getPopulation().toString()+" / 2000"
                        Handler(Looper.getMainLooper()).post {
                            run {
                                myMapController.setCenter(Com_Val_Start)
                                geopoints.clear()
                                geopoints.add(Com_Val_Start)
                                geopoints.add(Com_val_End)
                                line.setPoints(geopoints)
                                v.openmapview.overlays.add(line)
                                v.openmapview.invalidate()
                            }
                        }
                    }
                }
                if (contador == 2){
                    Mediterraneo.setBike(jsonobj.getString("id"), jsonobj.getInt("laneOccupancy"))
                    if (Mediterraneo.getPopulation()<0) {
                        v.populationBike.text = "NO DATA AVAIABLE"
                    }else{
                        if (Mediterraneo.getPopulation()<30){
                            v.ocupation.setBackgroundResource(R.drawable.circle_green)
                        }else if (Mediterraneo.getPopulation() in 30..69){
                            v.ocupation.setBackgroundResource(R.drawable.circle_yellow)
                        }else{
                            v.ocupation.setBackgroundResource(R.drawable.circle_red)
                        }
                        v.populationBike.text= Mediterraneo.getPopulation().toString()+" / 2000"
                        Handler(Looper.getMainLooper()).post {
                            run {
                                myMapController.setCenter(Mediterraneo_Start)
                                geopoints.clear()
                                geopoints.add(Mediterraneo_Start)
                                geopoints.add(Mediterraneo_Mid)
                                geopoints.add(Mediterraneo_End)
                                line.setPoints(geopoints)
                                v.openmapview.overlays.add(line)
                            }
                        }
                    }
                }else if (contador == 3){
                    Europa.setBike(jsonobj.getString("id"), jsonobj.getInt("laneOccupancy"))
                    if (Europa.getPopulation()<0) {
                        v.populationBike.text = "NO DATA AVAIABLE"
                    }else{
                        if (Europa.getPopulation()<30){
                            v.ocupation.setBackgroundResource(R.drawable.circle_green)
                        }else if (Europa.getPopulation() in 30..69){
                            v.ocupation.setBackgroundResource(R.drawable.circle_yellow)
                        }else{
                            v.ocupation.setBackgroundResource(R.drawable.circle_red)
                        }
                        v.populationBike.text= Europa.getPopulation().toString()+" / 2000"
                        Handler(Looper.getMainLooper()).post {
                            run {
                                myMapController.setCenter(Europa_Start)
                                geopoints.clear()
                                geopoints.add(Europa_Start)
                                geopoints.add(Europa_End)
                                line.setPoints(geopoints)
                                v.openmapview.invalidate()
                            }
                        }
                    }
                }
            }

        })
    }
}