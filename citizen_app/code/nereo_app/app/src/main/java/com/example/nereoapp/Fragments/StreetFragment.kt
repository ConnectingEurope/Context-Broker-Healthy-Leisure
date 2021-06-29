package com.example.nereoapp.Fragments

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.preference.PreferenceManager
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import com.example.nereoapp.BuildConfig
import com.example.nereoapp.Class.Street
import com.example.nereoapp.R
import kotlinx.android.synthetic.main.fragment_street.view.*
import kotlinx.android.synthetic.main.fragment_street.view.openmapview
import okhttp3.*
import org.json.JSONArray
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapController
import org.osmdroid.views.overlay.Polyline
import java.io.IOException

class StreetFragment : Fragment() {
    val street = Street()
    val client = OkHttpClient()
    var geopoints : ArrayList<GeoPoint> = ArrayList<GeoPoint>()
    var line : Polyline = Polyline()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        super.onCreate(savedInstanceState)
        val v: View = inflater.inflate(R.layout.fragment_street, container, false)
        Configuration.getInstance().load(context, PreferenceManager.getDefaultSharedPreferences(context))
        Configuration.getInstance().userAgentValue = BuildConfig.APPLICATION_ID
        var myMapController: MapController = v.openmapview.controller as MapController
        v.openmapview.setMultiTouchControls(true)
        v.openmapview.setTileSource(TileSourceFactory.MAPNIK)
        v.openmapview.setBuiltInZoomControls(true)
        myMapController.setZoom(15)

        val lista = resources.getStringArray(R.array.rutas)
        val adaptador = activity?.let { ArrayAdapter(it, android.R.layout.simple_spinner_item, lista) }
        v.spinner2.adapter = adaptador
        v.spinner2.onItemSelectedListener = object :
                AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                fetchJson((position+1).toString(), v, myMapController)
            }
            override fun onNothingSelected(parent: AdapterView<*>?) {
            }
        }

        // Inflate the layout for this fragment
        return v
    }
    fun fetchJson(position: String, v: View, myMapController: MapController){
        val request = Request.Builder().url("http://your_api_url/walkingroute/$position").build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.i("failing", "Error")
            }
            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonarr = JSONArray(body)
                val jsonobj = jsonarr.getJSONObject(0)
                val location = ArrayList<JSONArray>()
                val locations = ArrayList<GeoPoint>()

                for (i in 0..jsonobj.getJSONArray("location").length()-1){
                    location.add(jsonobj.getJSONArray("location")[i] as JSONArray)
                    locations.add(GeoPoint(location[i].getDouble(1),location[i].getDouble(0)))
                }
                street.setStreet(jsonobj.getInt("id"), jsonobj.getString("route_name"), jsonobj.getString("difficulty"), jsonobj.getDouble("distance"), jsonobj.getDouble("positive_slope"), jsonobj.getDouble("max_height"), locations)
                v.Distancia.text = street.getDistance().toString()+"m"
                v.Dificultad.text = street.getDificulty().toUpperCase()
                v.PendienteAsc.text = street.getSlope().toString()+ "m"
                v.Altitud.text = street.getHeight().toString()+ "m"
                Handler(Looper.getMainLooper()).post {
                    run {
                        myMapController.setCenter(street.getLocations()[0])
                        geopoints.clear()
                        for(i in 0..street.getLocations().size-1){
                            geopoints.add(street.getLocations()[i])
                        }
                        line.setPoints(geopoints)
                        v.openmapview.overlays.add(line)
                        v.openmapview.invalidate()
                    }
                }
            }
        })
    }
}