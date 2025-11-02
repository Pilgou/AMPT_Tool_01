# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 15:55:21 2025

Streamlit FrontEnd for AMPT Optimizer

@author: Mamie
"""

import streamlit as st
import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from FileManagement import file_mng_fct as fm
from TimeManagement import DeltaTime
from Sidebar import side_bar as sb
import re
import matplotlib.pyplot as plt

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()

if "df_OutDCV_plot" not in st.session_state:
    st.session_state.df_OutDCV_plot = pd.DataFrame()

if "form_submit_button" not in st.session_state:
    st.session_state.form_submit_button = False
    
if "DispRawChecked" not in st.session_state:
    st.session_state.DispRawChecked = False

if "AMPT_file_loaded" not in st.session_state:
    st.session_state.AMPT_file_loaded = ""

if "EM_file_loaded" not in st.session_state:
    st.session_state.EM_file_loaded = ""

if "DispCurvChecked" not in st.session_state:
    st.session_state.DispCurvChecked = False
    
if "data_file_to_load_carlo" not in st.session_state:
    st.session_state.data_file_to_load_carlo = ""

if "rawdata_AMPT_data_file_state" not in st.session_state:    
    st.session_state.rawdata_AMPT_data_file_state = False
    
if "rawdata_EM_data_file_state" not in st.session_state:    
    st.session_state.rawdata_EM_data_file_state = False

if "iconDate" not in st.session_state:
    st.session_state.iconDate = ""

if "sidebarfile_Analyse" not in st.session_state:
    st.session_state.sidebarfile_Analyse = ""


def btn_displayDataframe():
    st.dataframe(st.session_state.df)

def btn_displayLine_chart() :
    st.line_chart(st.session_state.df_OutDCV_plot)

# # Clear shell
# os.system("cls")

st.title ("Raw Data from AMPT Optimizer")
st.markdown(" On this page : select raw data _(.csv file)_")

# AMPT_selector = st.radio("",("V900 i13.5 String Optimizer", "Optimizer 2"))
# st.write("👉 Vous avez choisi :", AMPT_selector)

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
csv_file_list_Path, csv_file_list_name = fm.search_files_by_extension(csv_path, ".csv") 
# Enlever les fichiers contenant "Carlo"
csv_file_list_name = [f for f in csv_file_list_name if "Carlo" not in f]
# Extraction des parties numériques
st.session_state.numerical_parts_ampt_csv = [re.findall(r'\d+', f)[0] for f in csv_file_list_name if re.findall(r'\d+', f)]
# print(st.session_state.numerical_parts_ampt_csv)

# Looking for .db files
db_file_list_Path, db_file_list_name = fm.search_files_by_extension(current_path, ".db") 
file_list_name = csv_file_list_name

if len(csv_file_list_name) > 0:
    st.subheader("Load AMPT-CU csv file")
    st.write(f"Found {len(csv_file_list_name)} .csv file(s)")
    # st.write(f"Found {len(db_file_list_name)} .db file: {db_file_list_name}")
    # st.write(f"The Dataframe below is extracted from {csv_file_list_name[0]}")
    # json_to_load = csv_file_list_name[0]
else:
    st.subheader("No csv file(s) found")

# Create a container box with file selector and load button    
with st.form(key = "source_selector"):
    data_file_to_load = st.selectbox("Select data source", file_list_name,
        index=len(file_list_name) - 1)  #  dernier élément)
    st.session_state.form_submit_button = st.form_submit_button(label = "Load")
    
if st.session_state.form_submit_button:
    st.session_state.DispRawChecked = False
    st.session_state.DispCurvChecked = False

    if ".csv" in data_file_to_load:
        # load csv file and convert it to dataframe
        st.session_state.df = pd.read_csv(f'./CSV/{data_file_to_load}')
        # st.metric(label="Rows", value = len(df))
        st.session_state.AMPT_file_loaded = data_file_to_load
               
        st.subheader("General information about the file")
        st.write(f"from {st.session_state.AMPT_file_loaded}")
        # Assuming that this timestamp is in milliseconds
        # format the timestamp column
        st.session_state.df['timestamp'] = pd.to_datetime(st.session_state.df['timestamp'], unit='ms')
        # Tronquer à la seconde
        st.session_state.df["timestamp"] = st.session_state.df["timestamp"].dt.floor("s")
        # Add column in df dataframe : the day of the week
        st.session_state.df["DayOfWeek"] = st.session_state.df["timestamp"].dt.day_name()
        
        # Add columns in df dataframe : power / AMPT
        
        # Determiner le nombre d'optimizer a partir du nombre de colonnes dans dataframe
        # liste des colonnes
        # nombre de valeurs par AMPT
        colonnes = st.session_state.df.columns.tolist()
        # st.write(colonnes)
        # Extraire les chiffres de fin si présents
        chiffres = [int(re.search(r'_(\d+)$', col).group(1)) 
                    for col in colonnes if re.search(r'_(\d+)$', col)]

        # Compter les numéros distincts
        # nb_diff = len(set(chiffres))
        # Localiser la valeur Max
        st.session_state.max_nb_AMPT = (max(set(chiffres)))

        for i in range(1, 7):  # de 1 à 6 inclus
            st.session_state.df[f"Out_Power_{i}"] = (
                st.session_state.df[f"OutDCV_{i}"] * st.session_state.df[f"OutDCA_{i}"])
            
        # Add columns in df dataframe : Total instantaneous power  all AMPT
        st.session_state.df["Out_Total_Power"] = st.session_state.df[[f"Out_Power_{i}" for i in range(1, 7)]].sum(axis=1)
        
        # add columns for energy counter
        # attention ! le contptage d'energy est indicatif car samplin 20s
        # Intervalle entre deux mesures en secondes (ex : 20 secondes)
        delta_t_sec = 20
        delta_t_hr = delta_t_sec / 3600  # conversion en heures
        
        # Calcul de l'énergie pour chaque ligne et chaque "i"
        for i in range(1, 7):
            st.session_state.df[f"Out_Energy_{i}"] = (
                st.session_state.df[f"OutDCV_{i}"] * st.session_state.df[f"OutDCA_{i}"] * delta_t_hr
            )
        
        # Transform dataframe into series pour courbes
        st.session_state.serie1 = st.session_state.df.set_index("timestamp")["OutDCV_1"]
        st.session_state.serie2 = st.session_state.df.set_index("timestamp")["OutDCV_2"]
        st.session_state.serie3 = st.session_state.df.set_index("timestamp")["OutDCV_3"]
        st.session_state.serie4 = st.session_state.df.set_index("timestamp")["OutDCV_4"]
        st.session_state.serie5 = st.session_state.df.set_index("timestamp")["OutDCV_5"]
        st.session_state.serie6 = st.session_state.df.set_index("timestamp")["OutDCV_6"]
        
        # Les réunir dans un DataFrame : OutDCV
        st.session_state.df_OutDCV_plot = pd.concat([st.session_state.serie1, st.session_state.serie2, st.session_state.serie3, st.session_state.serie4, st.session_state.serie5, st.session_state.serie6], axis=1)

# Extraction info sur cette new dataframe
if not st.session_state.df_OutDCV_plot.empty:
    with st.container(border=True):
        # Premier index
        st.session_state.ampt_startDate = st.session_state.serie1.index[0] 
        # second index
        ampt_secondDate = st.session_state.serie1.index[1]
        # Dernier index
        st.session_state.ampt_endDate = st.session_state.serie1.index[-1]
        # duration = endDate - startDate
        # or
        st.session_state.ampt_duration = st.session_state.df['timestamp'].max() - st.session_state.df['timestamp'].min()
        # st.session_state.ampt_sampling = ampt_secondDate - st.session_state.ampt_startDate
        # Calcul du sampling
        # Calculer la différence entre deux timestamps successifs
        st.session_state.df["delta"] = st.session_state.df["timestamp"].diff()
        
        #Temps moyen entre deux mesures
        mean_delta = st.session_state.df["delta"].mean()
        # print(f"Temps moyen entre deux échantillons : {mean_delta.seconds} ms")
        st.session_state.ampt_sampling = mean_delta

        # Détection d’anomalies temporelle(sur le sampling) : rupture de com (ex : si > 2× le temps moyen)
        threshold_sampling = 2 * mean_delta
        st.session_state.df["anomaly"] = st.session_state.df["delta"] > threshold_sampling
        # Compter le nombre total d’anomalies
        nb_anomalies_sampling = st.session_state.df["anomaly"].sum()
        
        
        # print(f"Nombre d’anomalies détectées : {nb_anomalies_sampling}")
        
        col3, col4 = st.columns(2)
        with col3:
            st.write("Start")
            st.write("End")
            st.session_state.ampt_sampling_s = (st.session_state.ampt_sampling.seconds)
            st.write("Sampling")
            st.write("Recording time")
            st.session_state.deltatimeHM = DeltaTime.format_delta(st.session_state.ampt_startDate, st.session_state.ampt_endDate)
            st.write("AMPT number")
        with col4:
            st.write(st.session_state.ampt_startDate)
            st.write(st.session_state.ampt_endDate)
            st.write(f"{st.session_state.ampt_sampling_s} s")
            st.write(f"{st.session_state.ampt_duration.seconds//60} mn -> {st.session_state.deltatimeHM}")
            st.write(st.session_state.max_nb_AMPT)
            
        # Vérifie les valeurs manquantes sauf dans la colonne "delta"
        # Liste des colonnes à exclure
        excluded_cols = ["delta", "anomaly"]
        # excluded_cols = ["delta"]
        cols_to_check = [c for c in st.session_state.df.columns if c not in excluded_cols]    
        if st.session_state.df[cols_to_check].isnull().values.any():
            st.error("❌ Le DataFrame contient des valeurs manquantes (None ou NaN).")
            st.session_state.rawdata_AMPT_data_file_state = True
        else:
            st.success("✅ Aucune valeur manquante détectée.")
            st.session_state.rawdata_AMPT_data_file_state = False
        
        if st.session_state.ampt_duration.seconds//60 < 1400:
            st.warning("⚠️ Record time ⏱ is not complete (24H).")
            st.session_state.rawdata_AMPT_data_file_state = True
            
        if nb_anomalies_sampling and not st.session_state.df[cols_to_check].isnull().values.any():
            st.warning(f"⚠️ Dataframe with {nb_anomalies_sampling} sampling anomalies")
            st.session_state.rawdata_AMPT_data_file_state = True
            anomalies = st.session_state.df[st.session_state.df["anomaly"]]
            st.write(anomalies[["timestamp", "delta"]])

            


            
    # Générer des statistiques descriptives rapidement
    with st.expander(f"ex : First statistics on the {st.session_state.max_nb_AMPT} AMPT's voltage outputs"):        
        # Display stats
        # st.subheader(f"ex : First statistics on the {nb_diff} AMPT's voltage outputs")
        # statistiques par series
        # stat1 = (serie1.describe())
        # st.write((stat1))
        
        # Statistiques de la dataframe
        # Decrire les valeurs std...
        st.write(st.session_state.df_OutDCV_plot.describe())
        # count → nombre de valeurs non nulles
        # mean → moyenne
        # std → écart-type (dispersion des données)
        # min → valeur minimale
        # 25% → premier quartile (25% des données ≤ cette valeur)
        # 50% → médiane (milieu de la distributionArithmeticError
        # 75% → troisième quartile (75% des données ≤ cette valeur)
        # max → valeur maximale


    st.session_state.checkbox_df = st.checkbox("Display RawData",value=st.session_state.get(""),key="DispRawChecked",help="Display DataFrame")
    st.session_state.checkbox_Curves_df = st.checkbox("Display Voltage Outputs Curves",value=st.session_state.get(""),key="DispCurvChecked",help="OutDCV_x")

if not st.session_state.df.empty:

    # Changer orde des colonnes du dataframe pour meilleur lecture
    # Nouvel ordre des colonnes
    # df2 = st.session_state.df[["timestamp", "OutDCV_1", "In1DCV_1","In2DCV_1","OutDCA","In1DCA_1","In2DCA_1"]]
    # print(st.session_state.df)
    previous_order = (list(st.session_state.df.columns))
    new_order = ['timestamp', 'OutDCV_1', 'In1DCV_1', 'In2DCV_1', 'DCWh_1','OutDCA_1',
                 'In1DCA_1', 'In2DCA_1', "Out_Power_1", 'OutDCV_2', 'In1DCV_2', 'In2DCV_2',
                 'DCWh_2', 'OutDCA_2', 'In1DCA_2', 'In2DCA_2', "Out_Power_2", 'OutDCV_3',
                 'In1DCV_3', 'In2DCV_3', 'DCWh_3', 'OutDCA_3', 'In1DCA_3', 'In2DCA_3',
                 "Out_Power_3", 'OutDCV_4', 'In1DCV_4', 'In2DCV_4', 'DCWh_4', 'OutDCA_4',
                 'In1DCA_4', 'In2DCA_4', "Out_Power_4", 'OutDCV_5', 'In1DCV_5', 'In2DCV_5',
                 'DCWh_5', 'OutDCA_5', 'In1DCA_5', 'In2DCA_5', "Out_Power_5", 'OutDCV_6',
                 'In1DCV_6', 'In2DCV_6', 'DCWh_6', 'OutDCA_6', 'In1DCA_6', 'In2DCA_6',
                 "Out_Power_6","Out_Total_Power","Out_Energy_1", "Out_Energy_2", "Out_Energy_3",
                 "Out_Energy_4" ,"Out_Energy_5", "Out_Energy_6", 'DayOfWeek',"delta","anomaly"]
    df2 = st.session_state.df[new_order]
    # Affichage dataframe
    if st.session_state.DispRawChecked:
        # st.dataframe(st.session_state.df)
        st.dataframe(df2)
        # print(df2.iloc[0:5])
    if st.session_state.DispCurvChecked:
        st.line_chart(st.session_state.df_OutDCV_plot)

# Display common part of Sidebar
# sb.common_part(file = st.session_state.AMPT_file_loaded, state = st.session_state.rawdata_AMPT_data_file_state)
sb.common_part()
