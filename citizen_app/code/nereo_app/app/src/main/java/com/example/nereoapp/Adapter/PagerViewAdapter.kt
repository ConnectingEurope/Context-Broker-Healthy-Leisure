package com.example.nereoapp.Adapter

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentPagerAdapter
import com.example.nereoapp.Fragments.*
import com.example.nereoapp.Fragments.HomeFragment
import com.example.nereoapp.Fragments.ProfileFragment

internal class PagerViewAdapter(fm:FragmentManager?):
        FragmentPagerAdapter(fm!!){
    override fun getItem(position: Int): Fragment {

        return when(position){
            0 -> {
                HomeFragment()
            }
            1 -> {
                BeachFragment()
            }
            2 -> {
                BikeFragment()
            }
            3 -> {
                StreetFragment()
            }
            4 -> {
                ProfileFragment()
            }
            else -> ProfileFragment()
        }

    }

    override fun getCount(): Int {

        return 5
    }
}