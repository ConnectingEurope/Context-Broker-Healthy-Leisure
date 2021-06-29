package com.example.nereoapp

import android.app.AlarmManager
import android.app.AlertDialog
import android.app.PendingIntent
import android.content.Context
import android.content.DialogInterface
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.viewpager.widget.ViewPager
import com.example.nereoapp.Adapter.PagerViewAdapter
import com.example.nereoapp.Fragments.HomeFragment
import okhttp3.*
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.jar.Manifest
import kotlin.system.exitProcess

class MainMenu : AppCompatActivity() {
    private lateinit var mViewPager: ViewPager
    private lateinit var btnHome: ImageButton
    private lateinit var btnBeach: ImageButton
    private lateinit var btnBike: ImageButton
    private lateinit var btnStreet: ImageButton
    private lateinit var btnLogOut : ImageButton
    private lateinit var mPagerAdapter: PagerViewAdapter
    private lateinit var LayoutMenu : LinearLayout
    private lateinit var LayoutProfile : LinearLayout
    private lateinit var LayoutOmit : LinearLayout
    private lateinit var btnLast : Button
    private lateinit var btnOmit : Button
    private lateinit var btnSave : Button
    var client = OkHttpClient()
    var id : String = "3"
    var nick : String = "admin"

    @RequiresApi(Build.VERSION_CODES.M)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main_menu)
        val prefs = this.getSharedPreferences("preferences", Context.MODE_PRIVATE)
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.WRITE_EXTERNAL_STORAGE), 0)
        }
        
        // init views
        id = intent.getStringExtra("id").toString()
        nick = intent.getStringExtra("nick").toString()
        mViewPager = findViewById(R.id.mViewPager)
        LayoutMenu = findViewById(R.id.Menu)
        LayoutProfile = findViewById(R.id.ProfileMenu)
        LayoutOmit = findViewById(R.id.Omit)
        //Buttons
        btnHome = findViewById(R.id.btnHome)
        btnBeach = findViewById(R.id.btnBeach)
        btnBike = findViewById(R.id.btnBike)
        btnStreet = findViewById(R.id.btnStreet)
        btnLogOut = findViewById(R.id.btnLogOut)

        btnLast = findViewById(R.id.last)
        btnOmit = findViewById(R.id.omit)
        btnSave = findViewById(R.id.save)

        mPagerAdapter = PagerViewAdapter(supportFragmentManager)
        mViewPager.adapter = mPagerAdapter
        mViewPager.offscreenPageLimit = 5

        HomeFragment()
        //add page change listener
        btnHome.setOnClickListener{
            mViewPager.currentItem = 0
        }
        btnBeach.setOnClickListener {
            mViewPager.currentItem = 1
        }
        btnBike.setOnClickListener {
            mViewPager.currentItem = 2
        }
        btnStreet.setOnClickListener {
            mViewPager.currentItem = 3
        }
        btnLogOut.setOnClickListener{

            val builder = AlertDialog.Builder(this)
                .setTitle("LOG OUT CONFIRMATION")
                .setMessage("ARE YOU SURE YOU WANT TO LOG OUT?")
                .setPositiveButton("YES"){ dialog, which ->
                    val cache : File = applicationContext.cacheDir
                    val appDir : File = File(cache.parent)
                    if(appDir.exists()){
                        val children : Array<String> = appDir.list()
                        for(s : String in children){
                            if(!s.equals("lib")){
                                File(appDir, s).deleteRecursively()
                            }
                        }
                    }
                    val intent = Intent(this, MainActivity::class.java)
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    this.startActivity(intent)
                    finish()
                    Runtime.getRuntime().exit(0)
                }
                .setNegativeButton("NO"){dialog, which ->
                    dialog.dismiss()
                }
            val dialog : AlertDialog = builder.create()
            dialog.show()
        }


        btnLast.setOnClickListener {
            LayoutMenu.visibility = View.VISIBLE
            LayoutProfile.visibility = View.GONE
            LayoutOmit.visibility = View.GONE
            fetchJson("http://localhost:5000/preferences/$id?omit=false")
            mViewPager.currentItem = 0
        }
        btnOmit.setOnClickListener {
            LayoutMenu.visibility = View.VISIBLE
            LayoutProfile.visibility = View.GONE
            LayoutOmit.visibility = View.GONE
            fetchJson("http://localhost:5000/preferences/$id?omit=true")
            mViewPager.currentItem = 0

        }
        btnSave.setOnClickListener {
            Toast.makeText(this, "PREFERENCES SAVED CORRECTLY", Toast.LENGTH_SHORT).show()
            LayoutMenu.visibility = View.VISIBLE
            LayoutProfile.visibility = View.GONE
            LayoutOmit.visibility = View.GONE
            PostRequest(prefs.getInt("beach", 0), prefs.getInt("bikelane", 1),prefs.getInt("street", 2),id)
            mViewPager.currentItem = 0
        }
        mViewPager.addOnPageChangeListener(object : ViewPager.OnPageChangeListener{


            override fun onPageScrollStateChanged(state: Int) {

            }

            override fun onPageScrolled(
                    position: Int,
                    positionOffset: Float,
                    positionOffsetPixels: Int
            ) {

            }

            override fun onPageSelected(position: Int) {
                changingTabs(position)
            }
        })

        // default tab
        mViewPager.currentItem = 4
        if(mViewPager.currentItem == 4){
            LayoutMenu.visibility = View.INVISIBLE
        }
    }
    private fun changingTabs(position: Int){
        if(position == 0){
            activateHome()
        }
        if(position == 1){
            activateBeach()
        }
        if(position == 2){
            activateBike()
        }
        if(position == 3){
            activateStreet()
        }
    }
    private fun activateHome(){
        btnHome.setImageResource(R.drawable.ic_home_green)
        btnBeach.setImageResource(R.drawable.ic_action_beach)
        btnBike.setImageResource(R.drawable.ic_action_bike)
        btnStreet.setImageResource(R.drawable.ic_action_street)
    }
    private fun activateBeach(){
        btnHome.setImageResource(R.drawable.ic_home_black)
        btnBeach.setImageResource(R.drawable.ic_action_beach_green)
        btnBike.setImageResource(R.drawable.ic_action_bike)
        btnStreet.setImageResource(R.drawable.ic_action_street)
    }
    private fun activateBike(){
        btnHome.setImageResource(R.drawable.ic_home_black)
        btnBeach.setImageResource(R.drawable.ic_action_beach)
        btnBike.setImageResource(R.drawable.ic_action_bike_green)
        btnStreet.setImageResource(R.drawable.ic_action_street)
    }
    private fun activateStreet(){
        btnHome.setImageResource(R.drawable.ic_home_black)
        btnBeach.setImageResource(R.drawable.ic_action_beach)
        btnBike.setImageResource(R.drawable.ic_action_bike)
        btnStreet.setImageResource(R.drawable.ic_action_street_green)
    }
    internal fun changePage(position: Int){
        mViewPager.currentItem = position
    }
    
    private fun PostRequest(beach_position: Int, bikelane_position: Int, walking_route_position: Int, id: String) {
        var JSON: MediaType? = MediaType.parse("application/json; charset=utf-8")
        //Check we are in login part
        var formBody = JSONObject()
                .put("beach_position", beach_position)
                .put("bikelane_position", bikelane_position)
                .put("walking_route_position", walking_route_position)
        var body = RequestBody.create(JSON, formBody.toString())
        var request = Request.Builder()
                .url("http://ypur_api_url/preferences/$id")
                .post(body)
                .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Toast.makeText(applicationContext, e.toString(), Toast.LENGTH_SHORT)
            }
            override fun onResponse(call: Call, response: Response) {
            }
        })
    }
    fun fetchJson(url: String) {
        val request = Request.Builder().url(url).build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                /*Handler(Looper.getMainLooper()).post {
                    run {
                        Toast.makeText(applicationContext, e.toString(), Toast.LENGTH_SHORT).show()
                    }
                }*/
            }
            override fun onResponse(call: Call, response: Response) {
            }
        })
    }

    override fun onBackPressed() {
        changePage(0)
    }
}