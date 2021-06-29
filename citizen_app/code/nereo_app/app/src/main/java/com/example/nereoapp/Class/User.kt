package com.example.nereoapp.Class

import android.provider.ContactsContract

class User {
    private var id : String = ""
    private var username : String = ""
    private var password : String = ""
    private var email : String = ""
    private var Name : String = ""

    fun User(){}
    fun setUser(useraname : String, password : String, email : String, Name : String){
        this.username = useraname
        this.password = password
        this.email = email
        this.Name = Name
    }
    fun setId(id : String){this.id = id}
    fun getId() : String{return id}
    fun getUsername() : String{return username}
    fun getPassword() : String{return password}
    fun getEmail() : String{return email}
    fun getName() : String{return Name}
}