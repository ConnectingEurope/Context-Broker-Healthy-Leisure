package com.example.nereoapp.Fragments

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Adapter
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.nereoapp.MainMenu
import com.example.nereoapp.R
import com.example.nereoapp.RecyclerViewAdapter
import kotlinx.android.synthetic.main.fragment_profile.view.*
import java.util.*
import kotlin.collections.ArrayList

class ProfileFragment : Fragment() {
    val data = ArrayList<String>()
    lateinit var prefs : SharedPreferences
    lateinit var prefseditor: SharedPreferences.Editor

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val v : View = inflater.inflate(R.layout.fragment_profile, container, false)
        prefs = context?.getSharedPreferences("preferences", Context.MODE_PRIVATE)!!
        prefseditor = prefs.edit()
        data.add("BEACH")
        data.add("BIKE ROUTES")
        data.add("WALKING ROUTES")
        initRecycler(v)
        // Inflate the layout for this fragment
        return v
    }
    fun initRecycler(v : View){
        v.recyclerView.layoutManager = LinearLayoutManager(this.context)
        val adapter = RecyclerViewAdapter(data)
        v.recyclerView.adapter = adapter
        val itemtTouchHelper = ItemTouchHelper(simpleCallback)
        itemtTouchHelper.attachToRecyclerView(v.recyclerView)
    }
    val simpleCallback = object : ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN or ItemTouchHelper.START or ItemTouchHelper.END, 0){
        override fun onMove(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder, target: RecyclerView.ViewHolder): Boolean {
            val fromPosition : Int = viewHolder.adapterPosition
            val toPosition : Int = target.adapterPosition
            Collections.swap(data, fromPosition, toPosition)
            recyclerView.adapter?.notifyItemMoved(fromPosition, toPosition)
            for (i in 0 until data.size){
                when(data[i]){
                    "BEACH" -> prefseditor?.putInt("beach", i)
                    "BIKE ROUTES" -> prefseditor?.putInt("bikelane", i)
                    "WALKING ROUTES" -> prefseditor?.putInt("street", i)
                }
            }
            return false
        }
        override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
            TODO("Not yet implemented")
        }
    }
}