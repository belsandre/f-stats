#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
# from streamlit_folium import folium_static
# import folium
from geopy import distance
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="clinics-near-me")

df = pd.read_csv("csv/2019-by-clinic-gcode.csv")


# Sidebar inputs
st.sidebar.markdown("## Customize")
address = st.sidebar.text_input("Your address", '1033 Cordova St, Pasadena, California')
num_clinics = st.sidebar.text_input("Number of clinics", 10)


st.title('Clinics Near You')

my_coords = tuple(geolocator.geocode(address).point)

df['distance'] = df.apply(lambda x: distance.distance(my_coords, (x.lat,x.lon)).miles, axis=1)
closest = df.nsmallest(int(num_clinics),'distance')

st.markdown('### Closest ' + num_clinics + ' near you')
st.dataframe(closest)


# from folium.plugins import MarkerCluster
# # Create a map object and center it to the avarage coordinates to m
# m = folium.Map(location=closest[["lat", "lon"]].mean().to_list(), zoom_start=10)
# # if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster, add to m
# marker_cluster = MarkerCluster().add_to(m)
# # draw the markers and assign popup and hover texts
# # add the markers the the cluster layers so that they are automatically clustered
# for i,r in closest.iterrows():
#     location = (r["lat"], r["lon"])
#     folium.Marker(location=location,
#                       popup = r['CurrentClinicCity'],
#                       tooltip=r['CurrentClinicName1'])\
#     .add_to(marker_cluster)
# # display the map
# folium_static(m)


st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=my_coords[0],
        longitude=my_coords[1],
        zoom=11,
        pitch=0,
    ),
    layers=[
#        pdk.Layer(
#           'HexagonLayer',
#           data=closest[["lat", "lon", "CurrentClinicName1"]],
#           get_position=["lon", "lat"],
##           get_position='[lon, lat]',
#           radius=200,
#           elevation_scale=4,
#           elevation_range=[0, 1000],
#           pickable=True,
#           extruded=True,
#        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=closest[["lat", "lon", "CurrentClinicName1"]],
            get_position=["lon", "lat"],
#            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
            pickable=True,
            opacity=0.8,
            stoked=True,
            filled=True,
            radius_scale=5,
            radius_min_pixels=1,
            radius_max_pixels=10,
            line_width_min_pixels=1,
        ),
    ],
    tooltip = {
        "html": '{CurrentClinicName1}',
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"}
    }
))



closest["ND_NumIntentRet1"] = pd.to_numeric(closest["ND_NumIntentRet1"], errors='coerce')
closest["TotNumCycles1"] = pd.to_numeric(closest["TotNumCycles1"], errors='coerce')
closest["TotNumCyclesAll"] = pd.to_numeric(closest["TotNumCyclesAll"], errors='coerce')



st.markdown('### Clinics by distance')

labels = closest.CurrentClinicName1.apply(str.title)

fig = go.Figure(data=[
    go.Bar(x=closest.distance, y=labels, text=closest.distance.apply(lambda x: round(x, 1)), textposition='auto', orientation='h'),
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig['layout']['yaxis']['autorange'] = "reversed"
#fig.show()
st.plotly_chart(fig)



# fig, ax = plt.subplots()
# 
# ax.bar(closest.CurrentClinicName1, closest.distance)
# ax.set_title('Distance to closest clinics')
# ax.set_xlabel('Clinics')
# ax.set_ylabel('Miles')
# 
# plt.xticks(rotation='vertical')
# # plt.show()
# st.pyplot(fig)



st.markdown('### Number of intended retrievals in your age group per year')


fig = go.Figure(data=[
    go.Bar(x=closest.ND_NumIntentRet1, y=labels, text=closest.ND_NumIntentRet1, textposition='auto', orientation='h'),
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig['layout']['yaxis']['autorange'] = "reversed"
#fig.show()
st.plotly_chart(fig)



# fig, ax = plt.subplots()
# 
# ax.bar(closest.CurrentClinicName1, closest.ND_NumIntentRet1)
# ax.set_title('Number of intended retrievals in your age group per year')
# ax.set_xlabel('Clinics')
# ax.set_ylabel('# Cycles')
# 
# plt.xticks(rotation='vertical')
# # plt.show()
# st.pyplot(fig)



st.markdown('### Number of cycles per year')

cycles_my_age = closest.TotNumCycles1
cycles_other = closest.TotNumCyclesAll - cycles_my_age
# width = 0.35



fig = go.Figure(data=[
    go.Bar(name='My age group', x=cycles_my_age, y=labels, orientation='h'),
    go.Bar(name='All other age groups', x=cycles_my_age, y=labels, orientation='h')
])
# Change the bar mode
fig.update_layout(
    barmode='stack',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1,
        xanchor='right',
        x=1
    )
)
fig['layout']['yaxis']['autorange'] = "reversed"
#fig.show()
st.plotly_chart(fig)



# fig, ax = plt.subplots()
# 
# ax.bar(labels, cycles_my_age, width, label='Cycles in my age group')
# ax.bar(labels, cycles_other, width, bottom=cycles_my_age, label='All other cycles')
# ax.set_ylabel('Cycles')
# ax.set_title('Number of cycles per year')
# ax.legend()
# 
# plt.xticks(rotation='vertical')
# # plt.show()
# st.pyplot(fig)
