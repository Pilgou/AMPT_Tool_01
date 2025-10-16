# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 14:16:45 2025

Treatment of csv file from Energy Meters CarloGavazzi

@author: Mamie
"""

import streamlit as st
from Sidebar import side_bar as sb
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import json
import os


if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()
    
if "AMPT_file_loaded" not in st.session_state:
    st.session_state.AMPT_file_loaded = ""
    
if "EM_file_loaded" not in st.session_state:
    st.session_state.EM_file_loaded = ""

if "rawdata_EM_data_file_state" not in st.session_state:    
    st.session_state.rawdata_EM_data_file_state = []


    


# Display common part of Sidebar
sb.common_part()

st.title ("Energy Meter Data Analyse")
st.markdown(" On this page : EM time series are evaluate ")


col10, col11 = st.columns([1,3])
with col10:
        st.info("afficher ici model AMPT / model Carlo ???")
with col11:
    with st.container(border=True):
        st.info("afficher ici qq info datasheet AMPT / Carlo ???")
        st.markdown("[Datasheet](https://www.ampt.com/wp-content/uploads/2023/08/Ampt_i13.5_1000Vsys__Datasheet_EN_51770007-1P.pdf)")

# Affiche infos si dataframe chargée
if not st.session_state.df_carlo.empty:
    st.session_state.day = st.session_state.df_carlo.loc[1000, "DayOfWeek"]
    with st.container(border=True):
            st.write("EM data : ",st.session_state.day)
            col5, col6, col7 = st.columns(3)
            with col5:
                st.write("Start : ", st.session_state.EM_startDate)
                st.write(f"{st.session_state.EMdeltatimeHM}")
            with col6:
                st.write("End : ", st.session_state.EM_endDate)
                st.write(f"{st.session_state.EM_duration.seconds//60} mn")
            with col7:
                st.write(f"Sampling : {st.session_state.EM_sampling_s} s")
                if st.session_state.rawdata_EM_data_file_state == True:
                    st.markdown("❌ Raw data file error")

tab1, tab2 = st.tabs(["About", "Analyse 1"])

with tab1:
    st.header("About")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    st.markdown("[CarloGavazzi web site](https://www.ampt.com/products/string-optimizer/)")
    # st.link_button("AMPT web site","https://www.ampt.com/products/string-optimizer/)")
    st.markdown(
        """
    Treatment of csv file from Energy Meters : Analyse

    Reflexion :  
            ...

    __Postulat 1__ :  
         
        
    """)

with tab2:
    st.markdown(""" __Analyse 1__  
                👉 Visualization of EM values : voltage, current, power, energy  
                👉 Visualization of energy distribution 
                👉 Statistics""")
    st.divider()
    # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    
    if not st.session_state.df_carlo.empty:
        st.session_state.checkbox_Curves_df_carlo_tab_2 = st.checkbox("Curves",
                                                               value=st.session_state.get(""),
                                                               help="")

        if st.session_state.checkbox_Curves_df_carlo_tab_2:
            # # Selection du creneau de visualisation
            # # st.slider in Streamlit doesn’t natively support pandas.Timestamp objects.
            # # It only supports Python’s built-in datetime.datetime, date, time, int, or float.

            # # Extraire l'heure et les minutes seulement
            # st.session_state.df_carlo["time"] = st.session_state.df_carlo["timestamp"].dt.time
            
            # # Slider basé sur l’index des valeurs uniques de time
            # EM_time_values = st.session_state.df_carlo["time"].unique().tolist()
            # EM_start_idx, EM_end_idx = st.slider(
            #     "Select a range (points) :",
            #     min_value=0,
            #     max_value=len(EM_time_values)-1,
            #     value=(0, len(EM_time_values)-1)
            # )
            # EM_slider_nb_points = (EM_end_idx - EM_start_idx)
            # # Sélectionner les timestamps correspondants
            # EM_start_time = EM_time_values[EM_start_idx]
            # EM_end_time = EM_time_values[EM_end_idx]
            
            # # Filtrer DataFrame sur une plage de temps
            # st.session_state.df_carlo_filtre = st.session_state.df_carlo[(st.session_state.df_carlo["time"] >= EM_start_time) & (st.session_state.df_carlo["time"] <= EM_end_time)]
            # print(len(st.session_state.df_carlo_filtre))
            # print(len(st.session_state.df_carlo))

            # st.write(f"⏱ Range selected : {EM_start_time} → {EM_end_time}")
            # # st.dataframe(df_filtre)

            with st.form(key = "Analyse"):
                with st.expander("Infos : EM's data visualisation"):
                    st.markdown(
                        """
                        <ul>
                            <li><span style='color:orange'>Voltages</span></li>
                            <li><span style='color:cyan'>Currents</span></li>

                        </ul>
                        """,
                        unsafe_allow_html=True
                    )
    
        
                columns_list_carlo = (list(st.session_state.df_carlo.columns))
                # print(columns_list)
                carlo_voltage_columns_list = [col for col in columns_list_carlo if "Voltage" in col]
                carlo_current_columns_list = [col for col in columns_list_carlo if "Current" in col]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Select Voltage..")               
                    # Sélection dynamique des courbes avec checkbox
                    st.session_state.selection_v_carlo = [col for col in carlo_voltage_columns_list if st.checkbox(col, value=False)]
                with col2:
                    st.write("Select Current..")               
                    # Sélection dynamique des courbes avec checkbox
                    st.session_state.selection_a_carlo = [col for col in carlo_current_columns_list if st.checkbox(col, value=False)]

                st.session_state.form_submit_button_EM_trace = st.form_submit_button(label = "Trace")

            # Selection du creneau de visualisation
            # st.slider in Streamlit doesn’t natively support pandas.Timestamp objects.
            # It only supports Python’s built-in datetime.datetime, date, time, int, or float.

            # Extraire l'heure et les minutes seulement
            st.session_state.df_carlo["time"] = st.session_state.df_carlo["timestamp"].dt.time
            
            # Slider basé sur l’index des valeurs uniques de time
            EM_time_values = st.session_state.df_carlo["time"].unique().tolist()
            EM_start_idx, EM_end_idx = st.slider(
                "Select a range (points) :",
                min_value=0,
                max_value=len(EM_time_values)-1,
                value=(0, len(EM_time_values)-1)
            )
            EM_slider_nb_points = (EM_end_idx - EM_start_idx)
            # Sélectionner les timestamps correspondants
            EM_start_time = EM_time_values[EM_start_idx]
            EM_end_time = EM_time_values[EM_end_idx]
            
            # Filtrer DataFrame sur une plage de temps
            st.session_state.df_carlo_filtre = st.session_state.df_carlo[(st.session_state.df_carlo["time"] >= EM_start_time) & (st.session_state.df_carlo["time"] <= EM_end_time)]
            print(len(st.session_state.df_carlo_filtre))
            print(len(st.session_state.df_carlo))

            st.write(f"⏱ Range selected : {EM_start_time} → {EM_end_time}")
            # st.dataframe(df_filtre)

            if st.session_state.form_submit_button_EM_trace:
        
                EM_fusion_v = ["timestamp"] + st.session_state.selection_v_carlo
                EM_fusion_a = ["timestamp"] + st.session_state.selection_a_carlo
                
                if st.session_state.selection_v_carlo == st.session_state.selection_a_carlo == []:
                    st.warning("No datas selected !")

                if st.session_state.df_carlo_filtre.empty:
                   st.session_state.df_carlo_filtre = st.session_state.df_carlo


                # Affichage des colonnes choisies
                # Voltage per EM
                if st.session_state.selection_v_carlo !=[]:
                    # st.write("✅ Colonnes sélectionnées")
                    # st.write(fusion)
                    st.write("📈 EM Voltage")
                    st.line_chart(st.session_state.df_carlo_filtre[EM_fusion_v], x="timestamp")
                # Amps per EM 
                if st.session_state.selection_a_carlo !=[]:
                    st.write("📈 EM Current")
                    st.line_chart(st.session_state.df_carlo_filtre[EM_fusion_a], x="timestamp")
