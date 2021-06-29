package com.example.nereoapp

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.core.content.ContextCompat
import com.example.nereoapp.Class.User
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_main.view.*
import kotlinx.android.synthetic.main.fragment_home.*
import kotlinx.android.synthetic.main.login_layout.*
import kotlinx.android.synthetic.main.login_layout.view.*
import okhttp3.*
import org.json.JSONObject
import java.io.IOException


class MainActivity : AppCompatActivity() {
    var user : User = User()
    var client = OkHttpClient()
    var position = true
    var validador = false


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val sharedPreferencesiterator = this.getSharedPreferences("registered", Context.MODE_PRIVATE)
        var editorIterator : SharedPreferences.Editor = sharedPreferencesiterator.edit()
        val sharedPreference = this.getSharedPreferences("autologin", Context.MODE_PRIVATE)
        var editor: SharedPreferences.Editor = sharedPreference.edit()
        val mail: EditText = findViewById<EditText>(R.id.mail)
        val password: EditText = findViewById<EditText>(R.id.Password)

        //LOGIN
        //Check is registered
        if (sharedPreferencesiterator.getBoolean("isregistered", false)){
            val intent = Intent(this, MainMenu::class.java)
            intent.putExtra("id", sharedPreference.getString("id", "1"))
            intent.putExtra("nick", sharedPreference.getString("username", "admin"))
            startActivity(intent)
            finish()
        }
        //Check isn't registered
        else {
            editorIterator.putBoolean("isregistered", false)
            editorIterator.commit()
            //GET DATA AND SHARE TO API
            val login = findViewById<Button>(R.id.login)
            login?.setOnClickListener {
                //Say we are in login API part
                position = false
                PostRequest(editor, sharedPreference, this, editorIterator, mail, password)
            }

            //REGISTER PAGE
            val register = findViewById<Button>(R.id.register)
            register?.setOnClickListener {
                val loginDialog = LayoutInflater.from(this).inflate(R.layout.login_layout, null)
                val loginBuilder = AlertDialog.Builder(this)
                        .setView(loginDialog)
                        .setTitle("REGISTER PAGE")
                val loginAlertDialog = loginBuilder.show()
                loginDialog.loginBtn.setOnClickListener {
                    position = true
                    if (loginDialog.password.text.toString() != loginDialog.repeatpassword.text.toString()) {
                        loginDialog.username.setText("")
                        loginDialog.email.setText("")
                        loginDialog.password.setText("")
                        loginDialog.repeatpassword.setText("")
                        loginDialog.Name.setText("")
                        Toast.makeText(this, "INCORRECT REPEATED PASSWORD", Toast.LENGTH_SHORT).show()
                    }
                    //If all is okay
                    else {
                        val encryptedpsswd = AESEncryption.encrypt(loginDialog.password.text.toString())
                        if (encryptedpsswd != null) {
                            user.setUser(loginDialog.username.text.toString(), encryptedpsswd, loginDialog.email.text.toString(), loginDialog.Name.text.toString())
                            PostRegister(editor, editorIterator, loginAlertDialog, this, sharedPreference, loginDialog)
                        }
                    }
                }
                loginDialog.cancelBtn.setOnClickListener {
                    loginAlertDialog.cancel()
                    loginAlertDialog.dismiss()
                }
            }
        }
        Log.i("userdata", user.getName())
    }

    private fun PostRequest(editor: SharedPreferences.Editor, sharedPreference: SharedPreferences, context: Context, editorIterator: SharedPreferences.Editor, mail: EditText, password: EditText){
        var JSON: MediaType? = MediaType.parse("application/json; charset=utf-8")
        //Check we are in login part
            var encryptedpsswd = AESEncryption.encrypt(password.text.toString())
            var formBody = JSONObject()
                    .put("email", mail.text)
                    .put("password", encryptedpsswd)
                    .put("register", position)
            var body = RequestBody.create(JSON, formBody.toString())
            Log.i("bodylogin", formBody.toString())
            var request = Request.Builder()
                    .url("http://your_api_url/user")
                    .post(body)
                    .build()
                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        Toast.makeText(context, e.toString(), Toast.LENGTH_SHORT)
                    }
                    override fun onResponse(call: Call, response: Response) {
                        val body = response?.body()?.string()
                        val jsonobj = JSONObject(body)
                        LoginResponse(jsonobj, editor, sharedPreference, context, editorIterator, mail, password)
                    }
                })
    }
    private fun PostRegister(editor : SharedPreferences.Editor, editorIterator: SharedPreferences.Editor, loginAlertDialog: AlertDialog, context : Context, sharedPreference : SharedPreferences, loginDialog: View){
        var JSON: MediaType? = MediaType.parse("application/json; charset=utf-8")
        var formBody = JSONObject()
                .put("username", user.getUsername())
                .put("password", user.getPassword())
                .put("email", user.getEmail())
                .put("name", user.getName())
                .put("register", position)
        var body = RequestBody.create(JSON, formBody.toString())
        var request = Request.Builder()
                .url("http://your_api_url/user")
                .post(body)
                .build()
        client.newCall(request).enqueue(object : Callback{
            override fun onFailure(call: Call, e: IOException) {
                editor.putBoolean("change", false)
            }
            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                val jsonobj = JSONObject(body)
                RegisterResponse(jsonobj, editor, editorIterator, loginAlertDialog, context, sharedPreference, loginDialog)
            }
        })
    }
    private fun checkBody(jsonobj : JSONObject): Boolean {
        if(jsonobj.has("id")){
            return true
        }else if(jsonobj.has("Exception")){
            throw TestException(jsonobj.get("Exception").toString())
        }else{
            throw Exception(jsonobj.toString())
        }
    }
    class TestException(message : String) : Exception(message)

    private fun RegisterResponse(jsonobj : JSONObject, editor : SharedPreferences.Editor, editorIterator: SharedPreferences.Editor, loginAlertDialog: AlertDialog, context : Context, sharedPreference : SharedPreferences, loginDialog: View){
        try {
            checkBody(jsonobj)
            editor.putString("id", jsonobj.getString("id"))
            editor.putString("username", user.getUsername())
            editor.putString("email", user.getEmail())
            editor.putString("name", user.getName())
            editor.putBoolean("change", true)
            editor.commit()
            editorIterator.putBoolean("isregistered", true)
            editorIterator.commit()
            loginAlertDialog.cancel()
            loginAlertDialog.dismiss()
            Handler(Looper.getMainLooper()).post {
                run {
                    Toast.makeText(context, "YOU LOGGED CORRECTLY", Toast.LENGTH_SHORT).show()
                }
            }

            val intent = Intent(context, MainMenu::class.java)
            intent.putExtra("id", sharedPreference.getString("id", "1"))
            intent.putExtra("nick", sharedPreference.getString("username", "admin"))
            startActivity(intent)
        }catch (e : TestException){
            Log.i("loginexception", e.toString())
            loginDialog.username.setText("")
            loginDialog.email.setText("")
            loginDialog.password.setText("")
            loginDialog.repeatpassword.setText("")
            loginDialog.Name.setText("")
            Handler(Looper.getMainLooper()).post {
                run {
                    Toast.makeText(context, e.toString().substringAfterLast(":"), Toast.LENGTH_SHORT).show()
                }
            }


        }catch (e : Exception){
            Log.i("loginexception", e.toString())
            Handler(Looper.getMainLooper()).post {
                run {
                    Toast.makeText(context, e.toString().substringAfterLast(":"), Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
    private fun LoginResponse(jsonobj : JSONObject, editor: SharedPreferences.Editor, sharedPreference: SharedPreferences, context: Context, editorIterator: SharedPreferences.Editor, mail: EditText, password: EditText){
        try{
            checkBody(jsonobj)
            editor.putString("id", jsonobj.getString("id"))
            editor.putString("username", jsonobj.getString("username"))
            editor.putString("email", jsonobj.getString("email"))
            editor.putString("name", jsonobj.getString("name"))
            editor.commit()
            user.setId(jsonobj.getString("id"))
            editorIterator.putBoolean("isregistered", true)
            editorIterator.commit()
            val intent = Intent(context, MainMenu::class.java)
            intent.putExtra("id", sharedPreference.getString("id", "1"))
            intent.putExtra("nick", sharedPreference.getString("username", "admin"))
            startActivity(intent)
        }catch(e : TestException){
            Log.i("loginexception", e.toString())
            mail.setText("")
            password.setText("")
            Handler(Looper.getMainLooper()).post {
                run {
                    Toast.makeText(context, e.toString().substringAfterLast(":"), Toast.LENGTH_SHORT).show()
                }
            }
        }catch(e : Exception){
            Log.i("loginexception", e.toString())
            Handler(Looper.getMainLooper()).post {
                run {
                    Toast.makeText(context, e.toString().substringAfterLast(":"), Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

}