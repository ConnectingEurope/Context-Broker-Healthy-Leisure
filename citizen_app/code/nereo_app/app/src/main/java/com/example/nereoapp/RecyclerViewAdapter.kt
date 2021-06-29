package com.example.nereoapp

import android.view.*

import androidx.recyclerview.widget.RecyclerView
import kotlinx.android.synthetic.main.item_list.view.*
import kotlin.collections.ArrayList

class RecyclerViewAdapter(private var data: ArrayList<String>): RecyclerView.Adapter<RecyclerViewAdapter.Holder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return Holder(layoutInflater.inflate(R.layout.item_list, parent, false))
    }

    override fun getItemCount(): Int = data.size

    override fun onBindViewHolder(holder: Holder, position: Int) {
        holder.render(data[position])
    }

    class Holder(val view: View) : RecyclerView.ViewHolder(view) {
        fun render(data: String) {
            view.btnSelection.text = data
        }
    }
}