#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import st_folium
from time import sleep as ts
from streamlit_folium import folium_static
from PIL import Image
img = Image.open("logo.jpg")


st.sidebar.title('Konteynerkent Yer Seçimi')
html_temp = """
<div style="background-color:blue;padding:1px">
<h3 style="color:white;text-align:center;">Konteynerkent Planlama </h3>
</div>"""
st.image(img, caption="***************",clamp=False)
st.markdown(html_temp, unsafe_allow_html=True)
st.markdown("####  ")







df = pd.read_excel("Konteyner Noktaları_TableToExcel_2023_04_03.xlsx")


    
il_liste = ["Tüm İller"]+df.il.unique().tolist()

city = st.sidebar.selectbox("Konteynerkentlerini görmek istediğiniz ili seçiniz:",il_liste)
if city != "Tüm İller" : 
    ilce_liste = ["Tüm İlçeler"]+df[df.il == city]["ilce"].unique().tolist()
    ilce = st.sidebar.selectbox("Konteynerkentlerini görmek istediğiniz ilçe seçiniz:" , ilce_liste)
    if ilce != "Tüm İlçeler":
        target = df[(df.il == city) & (df.ilce == ilce)][["il","ilce","planlanan_konteyner_sayisi","coor_x","coor_y"]]
    else:
        target = df[(df.il == city)][["il","ilce","planlanan_konteyner_sayisi","coor_x","coor_y"]]
else:
    target = df[["il","ilce","planlanan_konteyner_sayisi","coor_x","coor_y"]]
    

    

max_group = int(target["ilce"].count())
selection = st.sidebar.radio("Konteynerkentleri mesafelerine göre yapay zekayla gruplamak istiyor musunuz ?",("Evet","Hayır"))
if selection == "Evet":
    if target["ilce"].count() == 1:
        selected_n_clusters = 1
        st.info("Seçim yapılan konumda tek Konteynerkent vardır")
    elif max_group > 37:
        max_group = 37
        selected_n_clusters = st.sidebar.slider(label="Konteynerkentleri kaç gruba bölmek istersiniz?",min_value=1,max_value = max_group,step=1)
    else:
        selected_n_clusters = st.sidebar.slider(label="Konteynerkentleri kaç gruba bölmek istersiniz?",min_value=1,max_value = max_group,step=1)
elif selection == "Hayır":
    selected_n_clusters = 1
    ts(0.3)
    st.sidebar.success("Seçilen sınırlarındaki konteynerkentler tek grup olacaktır")

target.dropna(how="any",inplace=True)


colors = ['red', 'green', 'purple', 'orange', 'darkred', \
     'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', \
     'darkpurple', 'pink', 'lightblue',  'gray', \
     'black', 'lightgray', 'red', 'blue', 'green', 'purple', \
     'orange', 'darkred', 'lightred', 'beige', 'darkblue', \
     'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', \
    'gray', 'black', 'lightgray',"red",'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', \
     'black', 'lightgray', 'red', 'blue', 'green', 'purple', \
     'orange', 'darkred', 'lightred', 'beige', 'darkblue', \
     'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', \
     'lightgreen', 'gray', 'black', 'lightgray',"red" ]

colorss = {i:j  for i,j in zip(df.ilce.unique(),range(300))}



#st.subheader("{}".format(city))
if selection == "Evet" : 
    from sklearn.cluster import KMeans
    X=target[["coor_x","coor_y"]]
    y=target["ilce"]
    model = KMeans(n_clusters=selected_n_clusters,init='k-means++')
    target["kume"] = (model.fit(X).labels_)+1
    ## Creating a map with first GBM location
    location = folium.Map(location = [i for i in target.iloc[0,[3,4]].values],zoom_start=13)
    for i,j in zip(target.coor_x,target.coor_y):
        folium.Marker([i,j],popup = target[(target.coor_x == i) & (target.coor_y == j)]["ilce"].values[0],
        tooltip = target[(target.coor_x == i) & (target.coor_y == j)][["planlanan_konteyner_sayisi","kume"]].values[0],
        icon=folium.Icon(color=colors[target[(target.coor_x == i) & (target.coor_y == j)]["kume"].values[0]], icon="info-sign")).add_to(location)
    location.fit_bounds([target[["coor_x","coor_y"]].min().values.tolist(),target[["coor_x","coor_y"]].max().values.tolist()])
    w = target.groupby("kume")["planlanan_konteyner_sayisi"].sum().reset_index()
    col1, col2, col3 = st.columns(3)
    col1.metric("TOPLAM KONTEYNER SAYISI",target.planlanan_konteyner_sayisi.sum())
    col2.metric("TOPLAM KONTEYNERKENT SAYISI",target.planlanan_konteyner_sayisi.count())
    col3.metric("COEFFICENT OR VARIATION",round(np.std(w.planlanan_konteyner_sayisi)/w.planlanan_konteyner_sayisi.mean(),2))
    
    
    #st.write("Değişim Katsayısı: {0:.2f}".format(np.std(w.planlanan_konteyner_sayisi)/w.planlanan_konteyner_sayisi.mean()))
    folium_static(location, width=700, height=400)
    st.table(target.groupby("kume")["planlanan_konteyner_sayisi"].sum().reset_index())
    
    
    
else: 
    location = folium.Map(location = [i for i in target.iloc[0,[3,4]].values],zoom_start=13)
    for i,j in zip(target.coor_x,target.coor_y):
        folium.Marker([i,j],popup=target[(target.coor_x == i) & (target.coor_y == j)]["ilce"].values[0],
        tooltip=target[(target.coor_x == i) & (target.coor_y == j)]["planlanan_konteyner_sayisi"].values[0],
        icon=folium.Icon(color = colors[colorss[target[(target.coor_x == i)  & (target.coor_y == j)]["ilce"].values[0]]], icon="info-sign")).add_to(location)
    location.fit_bounds([target[["coor_x","coor_y"]].min().values.tolist(),target[["coor_x","coor_y"]].max().values.tolist()])
    
    w = target.groupby(["il","ilce"])["planlanan_konteyner_sayisi"].sum().reset_index()
    col1, col2, col3 = st.columns(3)
    col1.metric("TOPLAM KONTEYNER SAYISI",target.planlanan_konteyner_sayisi.sum())
    col2.metric("TOPLAM KONTEYNERKENT SAYISI",target.planlanan_konteyner_sayisi.count())
    col3.metric("COEFFICENT OR VARIATION",round(np.std(w.planlanan_konteyner_sayisi)/w.planlanan_konteyner_sayisi.mean(),2))
    #st.write("Değişim Katsayısı: {0:.2f}".format(np.std(w.planlanan_konteyner_sayisi)/w.planlanan_konteyner_sayisi.mean()))
    folium_static(location, width=700, height=400)
    st.table(target.groupby(["il","ilce"])["planlanan_konteyner_sayisi"].sum().reset_index())
    



    



