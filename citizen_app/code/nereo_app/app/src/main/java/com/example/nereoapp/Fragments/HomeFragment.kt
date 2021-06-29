package com.example.nereoapp.Fragments

import android.content.Context
import android.content.SharedPreferences
import android.content.res.ColorStateList
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Base64
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.nereoapp.Class.Home
import com.example.nereoapp.Class.Recommendations
import com.example.nereoapp.MainActivity
import com.example.nereoapp.MainMenu
import com.example.nereoapp.R
import kotlinx.android.synthetic.main.fragment_home.view.*
import kotlinx.android.synthetic.main.fragment_street.view.*
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.math.BigDecimal
import java.math.RoundingMode
import kotlin.math.round
import kotlin.math.roundToInt

class HomeFragment : Fragment() {
    val client = OkHttpClient()
    private var home = Home()
    var recommendations : Recommendations = Recommendations()
    var first : String = ""
    var perc : Double = 0.0
    var segunda : String = ""
    var percSec : Double = 0.0
    var tercera: String = ""
    var percTer : Double = 0.0
    lateinit var v : View

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        v = inflater.inflate(R.layout.fragment_home, container, false)

        // Inflate the layout for this fragment
        return v
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val sharedPreferences = context?.getSharedPreferences("preferences", Context.MODE_PRIVATE)
        var editor : SharedPreferences.Editor? = sharedPreferences?.edit()
        editor?.putString("surroundnull", "nonull")
        v.hello.text = "GOOD MORNING "+(activity as MainMenu).nick+"!"
        var urlHome= "http://your_api_url" //Copy here the API URL
        var urlRecommendations = "http://your_api_url/recommender/"+(activity as MainMenu).id
        fetchJson(urlHome, v)
        if (editor != null && sharedPreferences != null){
            getRecommendations(urlRecommendations, editor, sharedPreferences, v)
        }
    }
    fun fetchJson(url : String, v : View){
        val request = Request.Builder().url(url).build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.i("fail", "Error")
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonobj = JSONObject(body)
                home.setHome(jsonobj.getString("descriptiveSkyState").toUpperCase(), jsonobj.getInt("temperature"), jsonobj.getInt("relativeHumidity"), jsonobj.getString("icon"))

                val imageBytes = Base64.decode(home.getIcono(), Base64.DEFAULT)
                val decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                Handler(Looper.getMainLooper()).post {
                    run {
                        v.timeImage.setImageBitmap(decodedImage)
                        v.state.text = home.getEstado()
                        v.temperature.text = ("${home.getTemperatura()} ºC")
                    }
                }
            }
        })
    }
    fun getRecommendations(url : String, editor : SharedPreferences.Editor, sharedPreferences : SharedPreferences, v : View){
        val request = Request.Builder().url(url).build()
        Log.i("urlreq", url)
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.i("fail", "Error")
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonobj = JSONObject(body)
                editor.putLong("beach_recommender_result", (jsonobj.getDouble("beach_recommender_result")*100).toLong())
                editor.putLong("bike_recommender_result", (jsonobj.getDouble("bike_recommender_result")*100).toLong())
                editor.putLong("walk_recommender_result", (jsonobj.getDouble("walk_recommender_result")*100).toLong())
                Log.i("walk_recommender_result", jsonobj.getDouble("walk_recommender_result").toString())
                editor.commit()
                if (sharedPreferences != null) {
                    recommendations.setRecommendations(sharedPreferences.getLong("beach_recommender_result", 1).toDouble()/100, sharedPreferences.getLong("bike_recommender_result", 1).toDouble()/100, sharedPreferences.getLong("walk_recommender_result", 1).toDouble()/100)
                }

                if (recommendations.getBeach_perc()>recommendations.getBike_perc() && recommendations.getBeach_perc()>recommendations.getStreet_perc()){
                    first = "BEACH"
                    perc = recommendations.getBeach_perc()*10
                    if (recommendations.getBike_perc()>recommendations.getStreet_perc()){
                        segunda = "BIKE ROUTES"
                        percSec = recommendations.getBike_perc()*10
                        tercera = "WALKING ROUTES"
                        percTer = recommendations.getStreet_perc()*10
                    }else{
                        segunda = "WALKING ROUTES"
                        percSec = recommendations.getStreet_perc()*10
                        tercera = "BIKE ROUTES"
                        percTer = recommendations.getBike_perc()*10
                    }
                }else if (recommendations.getBike_perc()>recommendations.getBeach_perc() && recommendations.getBike_perc()>recommendations.getStreet_perc()){
                    first = "BIKE ROUTES"
                    perc = recommendations.getBike_perc()*10
                    if (recommendations.getBeach_perc()>recommendations.getStreet_perc()){
                        segunda = "BEACH"
                        percSec = recommendations.getBeach_perc()*10
                        tercera = "WALKING ROUTES"
                        percTer = recommendations.getStreet_perc()*10
                    }else{
                        segunda = "WALKING ROUTES"
                        percSec = recommendations.getStreet_perc()*10
                        tercera = "BEACH"
                        percTer = recommendations.getBeach_perc()*10
                    }
                }else{
                    first = "WALKING ROUTES"
                    perc = recommendations.getStreet_perc()*10
                    if (recommendations.getBeach_perc()>recommendations.getBike_perc()){
                        segunda = "BEACH"
                        percSec = recommendations.getBeach_perc()*10
                        tercera = "BIKE ROUTES"
                        percTer = recommendations.getBike_perc()*10
                    }else{
                        segunda = "BIKE ROUTES"
                        percSec = recommendations.getBike_perc()*10
                        tercera = "BEACH"
                        percTer = recommendations.getBeach_perc()*10
                    }
                }

                v.firstSelection.text = first
                v.firstPerc.text = round(perc, 2).toString()+"%"
                v.firstBar.progress = round(perc, 2).toInt()

                v.secondSelection.text = segunda
                v.secondPerc.text = round(percSec, 2).toString()+"%"
                v.secondBar.progress = round(percSec, 2).toInt()

                v.thirdSelection.text = tercera
                v.thirdPerc.text = round(percTer, 2).toString()+"%"
                v.thirdBar.progress = round(percTer, 2).toInt()

                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
                    if(perc >70.0){
                        v.firstBar.progressTintList = ColorStateList.valueOf(Color.GREEN)
                    }
                    if(perc > 50.0 && perc < 70.0){
                        v.firstBar.progressTintList = ColorStateList.valueOf(Color.YELLOW)
                    }
                    if(perc < 50.0){
                        v.firstBar.progressTintList = ColorStateList.valueOf(Color.RED)
                    }

                    if(percSec >70.0){
                        v.secondBar.progressTintList = ColorStateList.valueOf(Color.GREEN)
                    }
                    if(percSec > 50.0 && percSec < 70.0){
                        v.secondBar.progressTintList = ColorStateList.valueOf(Color.YELLOW)
                    }
                    if(percSec < 50.0){
                        v.secondBar.progressTintList = ColorStateList.valueOf(Color.RED)
                    }
                    if(percTer >70.0){
                        v.thirdBar.progressTintList = ColorStateList.valueOf(Color.GREEN)
                    }
                    if(percTer > 50.0 && percTer < 70.0){
                        v.thirdBar.progressTintList = ColorStateList.valueOf(Color.YELLOW)
                    }
                    if(percTer < 50.0){
                        v.thirdBar.progressTintList = ColorStateList.valueOf(Color.RED)
                    }
                }

                v.firstCardView.setOnClickListener{
                    when(first){
                        "BEACH" -> (activity as MainMenu).changePage(1)
                        "BIKE ROUTES" -> (activity as MainMenu).changePage(2)
                        "WALKING ROUTES" -> (activity as MainMenu).changePage(3)
                    }
                }
                v.secondCardView.setOnClickListener{
                    when(segunda){
                        "BEACH" -> (activity as MainMenu).changePage(1)
                        "BIKE ROUTES" -> (activity as MainMenu).changePage(2)
                        "WALKING ROUTES" -> (activity as MainMenu).changePage(3)
                    }
                }
                v.thirdCardView.setOnClickListener {
                    when(tercera){
                        "BEACH" -> (activity as MainMenu).changePage(1)
                        "BIKE ROUTES" -> (activity as MainMenu).changePage(2)
                        "WALKING ROUTES" -> (activity as MainMenu).changePage(3)
                    }
                }
            }
        })
    }

    private fun round(perc: Double, i: Int): Double {
        var bd : BigDecimal = BigDecimal.valueOf(perc)
        bd = bd.setScale(i, RoundingMode.HALF_UP)
        return bd.toDouble()
    }
}