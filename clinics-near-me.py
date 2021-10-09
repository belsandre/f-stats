#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import folium
from geopy.geocoders import Nominatim
from geopy import distance

geolocator = Nominatim(user_agent="clinics-near-me")

df = pd.read_csv("csv/2019-by-clinic-gcode.csv")
df.head()


# In[2]:


my_location = geolocator.geocode("1033 Cordova St, Pasadena, California")
my_coords = tuple(my_location.point)
print(my_coords)


# In[5]:


df['distance'] = df.apply(lambda x: distance.distance(my_coords, (x.lat,x.lon)).miles, axis=1)
closest = df.nsmallest(10,'distance')
closest


# In[7]:


from folium.plugins import MarkerCluster
# Create a map object and center it to the avarage coordinates to m
m = folium.Map(location=closest[["lat", "lon"]].mean().to_list(), zoom_start=10)
# if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster, add to m
marker_cluster = MarkerCluster().add_to(m)
# draw the markers and assign popup and hover texts
# add the markers the the cluster layers so that they are automatically clustered
for i,r in closest.iterrows():
    location = (r["lat"], r["lon"])
    folium.Marker(location=location,
                      popup = r['CurrentClinicCity'],
                      tooltip=r['CurrentClinicName1'])\
    .add_to(marker_cluster)
# display the map
folium_static(m)


# In[23]:


import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[24]:

fig, ax = plt.subplots()

ax.bar(closest.CurrentClinicName1, closest.distance)
ax.set_title('Distance to closest clinics')
ax.set_xlabel('Clinics')
ax.set_ylabel('Miles')

plt.xticks(rotation='vertical')
plt.show()
st.pyplot(fig)


# In[28]:

fig, ax = plt.subplots()

ax.bar(closest.CurrentClinicName1, closest.ND_NumIntentRet1)
ax.set_title('Number of cycles per year')
ax.set_xlabel('Clinics')
ax.set_ylabel('# Cycles')

plt.xticks(rotation='vertical')
plt.show()
st.pyplot(fig)


# In[36]:


closest[["TotNumCycles1","TotNumCyclesAll"]] = closest[["TotNumCycles1","TotNumCyclesAll"]].apply(pd.to_numeric)

labels = closest.CurrentClinicName1
cycles_my_age = closest.TotNumCycles1
cycles_all = closest.TotNumCyclesAll - cycles_my_age
width = 0.35

fig, ax = plt.subplots()

ax.bar(labels, cycles_my_age, width, label='Cycles in my age group')
ax.bar(labels, cycles_all, width, bottom=cycles_my_age, label='All other cycles')
ax.set_ylabel('Cycles')
ax.set_title('Number of cycles per year')
ax.legend()

plt.xticks(rotation='vertical')
plt.show()
st.pyplot(fig)


# In[ ]:




