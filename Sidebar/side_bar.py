# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 19:54:18 2025

@author: Mamie
"""

import streamlit as st


def common_part(file:str, state:bool):
    # Texte dans la barre latérale
    st.sidebar.header("Sources loaded")
    if not st.session_state.df.empty:
        st.sidebar.markdown("__AMPT-CU :__")
        if state == False:
            st.sidebar.info(f"{file}")
        else:
            st.sidebar.error(f"{st.session_state.file}")

        
    if not  st.session_state.df_carlo.empty:  
        st.sidebar.markdown("__Carlo Gavazzi EM :__")
        st.sidebar.info(f"{st.session_state.data_file_to_load_carlo}")
