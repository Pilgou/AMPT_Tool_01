# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 10:06:39 2025

@author: Mamie
"""

import streamlit as st
import pandas as pd
import os

os.system("cls")
current_path = os.getcwd()
config_path = current_path + "/AMPTconfig"
from FileManagement import file_mng_fct as fm
from Sidebar import side_bar as sb

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()

if "form_submit_button_configFile" not in st.session_state:
    st.session_state.form_submit_button_configFile = False
    
if "config_file_to_load" not in st.session_state:
    st.session_state.config_file_to_load = ""

if "df_config" not in st.session_state:
    st.session_state.df_config = ""

st.title ("Configuration file ")
st.markdown("_Build or load AMPT-CU configuration file_")
st.divider()
st.markdown(" Case 1 : select your configuration file _(.csv file)_")

# Looking for .csv files
config_file_list_Path, config_file_list_name = fm.search_files_by_extension(config_path, ".csv") 
config_file_list_name = config_file_list_name

if len(config_file_list_name) > 0:
    st.subheader("Load AMPT-CU config file")
    st.write(f"Found {len(config_file_list_name)} .csv file(s)")
else:
    st.subheader("No config file(s) found")

with st.form(key = "Config_file_selector"):
    st.session_state.config_file_to_load = st.selectbox("Select configuration file", config_file_list_name)
    st.session_state.form_submit_button_configFile = st.form_submit_button(label = "Load")

if st.session_state.form_submit_button_configFile:
    if ".csv" in st.session_state.config_file_to_load:
        # load csv file and convert it to dataframe
        df = pd.read_csv(f'./AMPTconfig/{st.session_state.config_file_to_load}',header=None)
        # Ignorer la première ligne (Solaris,1,1,2) si ce sont des métadonnées
        df = df.iloc[1:]
        
        # Remplir la première colonne vide avec la valeur précédente
        df[0] = df[0].fillna(method="ffill")
        
        # Garder uniquement les colonnes utiles
        st.session_state.df_config = df[[0, 1, 2]].rename(columns={0: "Type", 1: "Nom", 2: "Numéro de série"})
        st.metric(label="AMPTs configured : ", value = len(st.session_state.df_config))

        st.write(st.session_state.df_config)
               
        st.subheader("Deduction of Modbus mapping")
        st.write(f"from {st.session_state.config_file_to_load}")

# Display common part of Sidebar
sb.common_part()