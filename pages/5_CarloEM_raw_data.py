# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 18:59:23 2025

Treatment CSV from CarloGavazzi Energy meters

@author: Mamie
"""

import streamlit as st
import os
import pandas as pd
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from FileManagement import file_mng_fct as fm
from TimeManagement import DeltaTime
from Sidebar import side_bar as sb
import re
import matplotlib.pyplot as plt

if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_carlo_Voltage_plot" not in st.session_state:
    st.session_state.df_carlo_Voltage_plot = pd.DataFrame()

if "form_submit_button_carlo" not in st.session_state:
    st.session_state.form_submit_button_carlo = False
    
if "checkbox_df_carlo" not in st.session_state:
    st.session_state.checkbox_df_carlo = False

if "checkbox_Curves_df_carlo" not in st.session_state:
    st.session_state.checkbox_Curves_df_carlo = False
    
if "AMPT_file_loaded" not in st.session_state:
    st.session_state.AMPT_file_loaded = ""
    
if "EM_file_loaded" not in st.session_state:
    st.session_state.EM_file_loaded = ""
    
if "rawdata_AMPT_data_file_state" not in st.session_state:    
    st.session_state.rawdata_AMPT_data_file_state = []

if "rawdata_EM_data_file_state" not in st.session_state:    
    st.session_state.rawdata_EM_data_file_state = []


def btn_displayDataframe_carlo():
    st.dataframe(st.session_state.df_carlo)

def btn_displayLine_chart_carlo() :
    st.line_chart(st.session_state.df_carlo_Voltage_plot)

# Clear shell
os.system("cls")

st.title ("Raw Data from EM CarloGavazzi")
st.markdown(" On this page : select raw data _(.csv file)_")

st.divider()

current_path = os.getcwd()
csv_path = current_path + "/CSV"
# main_path = os.path.dirname(current_path)

# col1, col2 = st.columns(2)
# with col1:
#     st.image(os.path.join(current_path,"images","logoSCSystems.jpg"))#,width=200)

# with col2:
#     st.image(os.path.join(current_path,"images","AMPT.jpg"),width=250)#,width=200)

# Looking for .csv files
csv_file_list_Path_carlo, csv_file_list_name_carlo = fm.search_files_by_extension(csv_path, ".csv") 
file_list_name_carlo = csv_file_list_name_carlo

# Ne garder que les fichiers contenant "Carlo"
file_list_name_carlo = [f for f in file_list_name_carlo if "Carlo"  in f]


if len(csv_file_list_name_carlo) > 0:
    st.subheader("Load Carlo Gavazzi csv file")
    st.write(f"Found {len(csv_file_list_name_carlo)} .csv file(s)")
    # st.write(f"Found {len(db_file_list_name)} .db file: {db_file_list_name}")
    # st.write(f"The Dataframe below is extracted from {csv_file_list_name[0]}")
    # json_to_load = csv_file_list_name[0]
else:
    st.subheader("No csv file(s) found")
    
# Dans une "form" creation du selecteur de fichier et du bouton de chargement    
with st.form(key = "source_selector_carlo"):
    data_file_to_load_carlo = st.selectbox("Select data source", file_list_name_carlo,  
                                           index=len(file_list_name_carlo) - 1)  #  dernier élément)
    st.session_state.form_submit_button_carlo = st.form_submit_button(label = "Load")

# Lecture du CSV
if st.session_state.form_submit_button_carlo:
    if ".csv" in data_file_to_load_carlo:
        # load csv file and convert it to dataframe
        st.session_state.df_carlo = pd.read_csv(f'./CSV/{data_file_to_load_carlo}')
        # st.metric(label="Rows", value = len(df))
        st.session_state.EM_file_loaded = data_file_to_load_carlo
             
        st.subheader("General information about the file")
        st.write(f"from {data_file_to_load_carlo}")
        # Assuming that this timestamp is in milliseconds
        # format the timestamp column
        st.session_state.df_carlo['timestamp'] = pd.to_datetime(st.session_state.df_carlo['timestamp'], unit='ms')
        # Tronquer à la seconde
        st.session_state.df_carlo["timestamp"] = st.session_state.df_carlo["timestamp"].dt.floor("s")
        # Add column in df dataframe : the day of the week
        st.session_state.df_carlo["DayOfWeek"] = st.session_state.df_carlo["timestamp"].dt.day_name()

        # Transform dataframe into series pour courbes
        st.session_state.carlo_serie1 = st.session_state.df_carlo.set_index("timestamp")["Voltage1"]
        st.session_state.carlo_serie2 = st.session_state.df_carlo.set_index("timestamp")["Voltage2"]
        st.session_state.carlo_serie3 = st.session_state.df_carlo.set_index("timestamp")["Voltage3"]
        st.session_state.carlo_serie4 = st.session_state.df_carlo.set_index("timestamp")["Voltage4"]
        st.session_state.carlo_serie5 = st.session_state.df_carlo.set_index("timestamp")["Voltage5"]
        st.session_state.carlo_serie6 = st.session_state.df_carlo.set_index("timestamp")["Voltage6"]
        
        # Les réunir dans un DataFrame : Voltage
        st.session_state.df_carlo_Voltage_plot = pd.concat([st.session_state.carlo_serie1, st.session_state.carlo_serie2, st.session_state.carlo_serie3, st.session_state.carlo_serie4, st.session_state.carlo_serie5, st.session_state.carlo_serie6], axis=1)

# Extraction info sur cette new dataframe
if not st.session_state.df_carlo_Voltage_plot.empty:
    with st.container(border=True):
        # Premier index
        startDate = st.session_state.carlo_serie1.index[0] 
        # second index
        secondDate = st.session_state.carlo_serie1.index[1]
        # Dernier index
        endDate = st.session_state.carlo_serie1.index[-1]
        # duration = endDate - startDate
        # or
        duration = st.session_state.df_carlo['timestamp'].max() - st.session_state.df_carlo['timestamp'].min()
        sampling = secondDate - startDate
        # Determiner le nombre d'optimizer a partir du nombre de colonnes dans dataframe
        # liste des colonnes
        # nombre de valeurs par AMPT
        colonnes = st.session_state.df_carlo.columns.tolist()
        # st.write(colonnes)
        print(colonnes)
        # Extraire les chiffres  si présents
        # Extraire tous les nombres présents
        numbers = [int(re.search(r'\d+', col).group()) for col in colonnes if re.search(r'\d+', col)]
        print(numbers)        
        # Compter les numéros distincts
        # nb_diff = len(set(chiffres))
        # Localiser la valeur Max
        max_nb_carlo = (max(set(numbers)))

        col3, col4 = st.columns(2)
        with col3:
            st.write("Start")
            st.write("End")
            sampling_s = (sampling.seconds)
            st.write("Sampling")
            st.write("Recording time (mn)")
            a = DeltaTime.format_delta(startDate, endDate)
            st.write("Recording time (H:MN")
            st.write("EM number")
        with col4:
            st.write( startDate)
            st.write( endDate)
            st.write(f"{sampling_s} s")
            st.write(f"{duration.seconds//60} mn")
            st.write(a)
            st.write(max_nb_carlo)
            
        if st.session_state.df_carlo.isnull().values.any():
            st.error("❌ Le DataFrame contient des valeurs manquantes (None ou NaN).")
            st.session_state.rawdata_EM_data_file_state = True
        else:
            st.success("✅ Aucune valeur manquante détectée.")
            st.session_state.rawdata_EM_data_file_state = False


    with st.expander(f"ex : First statistics on the {max_nb_carlo} EM's voltage Measurement"):        
        # Display stats
        # st.subheader(f"ex : First statistics on the {nb_diff} AMPT's voltage outputs")
        # statistiques par series
        # stat1 = (serie1.describe())
        # st.write((stat1))
        
        # Statistiques de la dataframe
        # Decrire les valeurs std...
        st.write(st.session_state.df_carlo_Voltage_plot.describe())

    st.session_state.checkbox_df_carlo = st.checkbox("Display EM RawData",value=st.session_state.get(""),help="Display DataFrame")
    st.session_state.checkbox_Curves_df_carlo = st.checkbox("Display Voltage EM Curves",value=st.session_state.get(""),help="Voltage")

if not st.session_state.df_carlo.empty:

    # Changer orde des colonnes du dataframe pour meilleur lecture
    # Nouvel ordre des colonnes
    # df2 = st.session_state.df[["timestamp", "OutDCV_1", "In1DCV_1","In2DCV_1","OutDCA","In1DCA_1","In2DCA_1"]]
    # print(st.session_state.df)
    previous_order = (list(st.session_state.df_carlo.columns))
    print(previous_order)
    new_order = ['timestamp', 'OutDCV_1', 'In1DCV_1', 'In2DCV_1', 'DCWh_1','OutDCA_1', 'In1DCA_1', 'In2DCA_1', 'OutDCA_2', 'OutDCV_2', 'In1DCV_2', 'In2DCV_2', 'DCWh_2', 'In1DCA_2', 'In2DCA_2', 'OutDCA_3', 'OutDCV_3', 'In1DCV_3', 'In2DCV_3', 'DCWh_3', 'In1DCA_3', 'In2DCA_3', 'OutDCA_4', 'OutDCV_4', 'In1DCV_4', 'In2DCV_4', 'DCWh_4', 'In1DCA_4', 'In2DCA_4', 'OutDCA_5', 'OutDCV_5', 'In1DCV_5', 'In2DCV_5', 'DCWh_5', 'In1DCA_5', 'In2DCA_5', 'OutDCA_46', 'OutDCV_6', 'In1DCV_6', 'In2DCV_6', 'DCWh_6', 'In1DCA_6', 'In2DCA_6', 'DayOfWeek']
    # df2 = st.session_state.df[new_order]
    # Affichage dataframe
    if st.session_state.checkbox_df_carlo:
        st.dataframe(st.session_state.df_carlo)
        # st.dataframe(df2)
    if st.session_state.checkbox_Curves_df_carlo:
        st.line_chart(st.session_state.df_carlo_Voltage_plot)

# Display common part of Sidebar
sb.common_part()
