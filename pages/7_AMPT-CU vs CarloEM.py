# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 14:17:38 2025

@author: Mamie
"""

import streamlit as st
from Sidebar import side_bar as sb
import pandas as pd


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

st.title ("AMPT-CU vs CarloGavazzi EM")
st.markdown(" On this page : Comparison between AMPT-CU and CarloGavazzi EM time series ")
