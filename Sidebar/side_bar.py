# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 19:54:18 2025

@author: Mamie
"""

import streamlit as st
import re

if "iconDate" not in st.session_state:
    st.session_state.iconDate = ""

if "sidebarfile_Analyse" not in st.session_state:
    st.session_state.sidebarfile_Analyse = ""

    
# def common_part(file:str, state:bool):
def common_part():

    # Texte dans la barre latérale
    st.sidebar.header("Sources loaded")
    if not st.session_state.df.empty:
        st.sidebar.markdown("__AMPT-CU :__")
        if st.session_state.rawdata_AMPT_data_file_state == False:
            st.sidebar.info(f"{st.session_state.AMPT_file_loaded}")
            if st.session_state.sidebarfile_Analyse !="" :
                st.sidebar.write(f"👉 {st.session_state.sidebarfile_Analyse}")
        else:
            st.sidebar.error(f"{st.session_state.AMPT_file_loaded}")
            st.sidebar.write("👉 Check rawdata")
    # if st.session_state.numerical_parts_ampt_csv

        
    if not  st.session_state.df_carlo.empty:  
        st.sidebar.markdown("__Carlo Gavazzi EM :__")
        if st.session_state.rawdata_EM_data_file_state == False:
            st.sidebar.info(f"{st.session_state.EM_file_loaded}")
        else:
            st.sidebar.error(f"{st.session_state.EM_file_loaded}")
        
    # --- Fonction pour extraire la partie numérique ---
    def extract_number(s):
        match = re.search(r"\d+", s)
        return match.group() if match else None
    
    # --- Vérification de la présence des deux variables ---
    if (
        "AMPT_file_loaded" in st.session_state
        and "EM_file_loaded" in st.session_state
        and st.session_state.AMPT_file_loaded
        and st.session_state.EM_file_loaded
    ):
        ampt_str = st.session_state.AMPT_file_loaded
        em_str = st.session_state.EM_file_loaded
    
        ampt_num = extract_number(ampt_str)
        em_num = extract_number(em_str)
    
        # st.write(f"🔹 AMPT : `{ampt_str}`")
        # st.write(f"🔹 EM   : `{em_str}`")
    
        if ampt_num != em_num:
            st.sidebar.warning("⚠️ Les dates des fichiers AMPT et EM ne correspondent pas !")
        else:
            st.sidebar.write("✅ same date")
    
