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

if "rawdata_data_file_state" not in st.session_state:    
    st.session_state.rawdata_data_file_state = []

if "df_OutDCV_plot" not in st.session_state:
    st.session_state.df_OutDCV_plot = pd.DataFrame()
    
if "selection_v" not in st.session_state:
    st.session_state.selection_v = []

if "selection_a" not in st.session_state:
    st.session_state.selection_a = []

if "selection_p" not in st.session_state:
    st.session_state.selection_p = []

if "df_filtre" not in st.session_state:
    st.session_state.df_filtre = pd.DataFrame()

if "checkbox_All_AMPT_Power" not in st.session_state:
    st.session_state.checkbox_All_AMPT_Power = False

if "checkbox_energyAMPT" not in st.session_state:
    st.session_state.checkbox_energyAMPT = False

if "form_submit_button_trace" not in st.session_state:
    st.session_state.form_submit_button_trace = False
    
if "form_submit_button_traceInputs" not in st.session_state:
    st.session_state.form_submit_button_traceInputs = False

    


# Display common part of Sidebar
sb.common_part()

st.title ("Energy Meter Data Analyse")
st.markdown(" On this page : EM time series are evaluate ")


# col10, col11 = st.columns([1,3])
# with col10:
#     AMPT_selector = st.radio("Model",("V900 i13.5", "Optimizer 2"))
# with col11:
#     with st.container(border=True):
#         if AMPT_selector == "V900 i13.5":
#             st.markdown(f"Input Max voltage : {1000} V")
#             st.markdown(f"Input Max current (Imp) : {12.8} A")
#             st.markdown(f"Input Max short-circuit current (Isc) : {13.5} A")
#         else :
#             st.markdown(f"Input Max Voltage : {2}")
#             st.markdown("...")
#         st.markdown("[Datasheet](https://www.ampt.com/wp-content/uploads/2023/08/Ampt_i13.5_1000Vsys__Datasheet_EN_51770007-1P.pdf)")


    # st.write("👉 Vous avez choisi :", AMPT_selector)
