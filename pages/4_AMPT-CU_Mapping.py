# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 18:53:02 2025

Load Mapping from AMPT-CU pdf file

@author: Mamie
"""
import streamlit as st
import pandas as pd
import os
import camelot

os.system("cls")
current_path = os.getcwd()
config_path = current_path + "/AMPTconfig"
from FileManagement import file_mng_fct as fm
from Sidebar import side_bar as sb

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()

if "form_submit_button_pdfFile" not in st.session_state:
    st.session_state.form_submit_button_pdfFile = False
    
if "pdf_file_to_load" not in st.session_state:
    st.session_state.pdf_file_to_load = ""

if "df_pdf" not in st.session_state:
    st.session_state.df_pdf = ""

st.title ("Extract Mapping ")
st.markdown("_Build or load AMPT-CU mapping_")
st.divider()
st.markdown(" Case 1 : select your  _.pdf file_ to extract the Modbus Map")

# Looking for .pdf files
pdf_file_list_Path, pdf_file_list_name = fm.search_files_by_extension(config_path, ".pdf") 
pdf_file_list_name = pdf_file_list_name

if len(pdf_file_list_name) > 0:
    st.subheader("Load AMPT-CU PDF file")
    st.write(f"Found {len(pdf_file_list_name)} .pdf file(s)")
else:
    st.subheader("No PDF file(s) found")

with st.form(key = "pdf_file_selector"):
    st.session_state.pdf_file_to_load = st.selectbox("Select PDF file", pdf_file_list_name)
    st.session_state.form_submit_button_pdfFile = st.form_submit_button(label = "Load")

if st.session_state.form_submit_button_pdfFile:
    if ".pdf" in st.session_state.pdf_file_to_load:
        # Lire toutes les tables de la page 1
        tables = camelot.read_pdf("C:/Users/Mamie/Documents/Python/DCS_Devices_tools/AMPT_Tool_01/AMPTconfig/Ampt Gen3CU.pdf", pages="1")
        # load csv file and convert it to dataframe
        df = tables[0].df  #premier tableau
        print(df)
        # Remplacer les sauts de ligne "\n" par un espace
        df = df.replace(r"\n", " ", regex=True)
        
        # Réinitialiser les colonnes si la première ligne contient les noms
        df.columns = df.iloc[0]   # première ligne = noms de colonnes
        df = df.drop(0).reset_index(drop=True)
        
        print(df.head(10))  # affiche les 10 premières lignes

# Nombre de tableaux trouvés
# print("Nombre de tableaux :", tables.n)

# Exporter en CSV / Excel / JSON
# tables[0].to_csv("tableau.csv")

# Display common part of Sidebar
sb.common_part()