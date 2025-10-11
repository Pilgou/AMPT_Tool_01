# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 19:54:18 2025

@author: Mamie
"""

import streamlit as st


# def common_part(file:str, state:bool):
def common_part():

    # Texte dans la barre latérale
    st.sidebar.header("Sources loaded")
    if not st.session_state.df.empty:
        st.sidebar.markdown("__AMPT-CU :__")
        if st.session_state.rawdata_AMPT_data_file_state == False:
            st.sidebar.info(f"{st.session_state.AMPT_file_loaded}")
        else:
            st.sidebar.error(f"{st.session_state.AMPT_file_loaded}")

        
    if not  st.session_state.df_carlo.empty:  
        st.sidebar.markdown("__Carlo Gavazzi EM :__")
        if st.session_state.rawdata_EM_data_file_state == False:
            st.sidebar.info(f"{st.session_state.EM_file_loaded}")
        else:
            st.sidebar.error(f"{st.session_state.EM_file_loaded}")
        
