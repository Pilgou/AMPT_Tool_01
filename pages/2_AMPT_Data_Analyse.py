# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 09:45:47 2025
Treatment of csv file from AMPT optimizer

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


# Display common part of Sidebar
sb.common_part(file = st.session_state.AMPT_file_loaded, state = st.session_state.rawdata_data_file_state)

st.title ("AMPT-CU Data Analyse")
st.markdown(" On this page : AMPTs time series are evaluate ")


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


# Affiche infos si dataframe chargée
if not st.session_state.df_OutDCV_plot.empty:
    st.session_state.day = st.session_state.df.loc[1000, "DayOfWeek"]
    with st.container(border=True):
            st.write("AMPT_CU data : ",st.session_state.day)
            col5, col6, col7 = st.columns(3)
            with col5:
                st.write("Start : ", st.session_state.ampt_startDate)
                st.write(f"{st.session_state.deltatimeHM}")
            with col6:
                st.write("End : ", st.session_state.ampt_endDate)
                st.write(f"{st.session_state.ampt_duration.seconds//60} mn")
            with col7:
                st.write(f"Sampling : {st.session_state.ampt_sampling_s} s")
                if st.session_state.rawdata_data_file_state == True:
                    st.markdown("❌ Raw data file error")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["About", "Analyse 1", "Analyse 2", "???", "???"])

with tab1:
    st.header("About")
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    st.markdown("[AMPT web site](https://www.ampt.com/products/string-optimizer/)")
    # st.link_button("AMPT web site","https://www.ampt.com/products/string-optimizer/)")

    st.markdown(
        """
    Treatment of csv file from AMPT_CU : Analyse

    Reflexion :  
        L'__AMPT-CU__ ne donne aucun diagnostique, il faut donc deduire l'état des PV 
        et optimizer via ses datas :  
            OutDCA / OutDCV / In1DCV / In2DCV / DCWh / In1DCA / In2DCA   
            
            
            OutDCA : S'il ny à pas charge = 0  
            OutDCV : Tension de sortie de AMPT  
            In1DCV : Tension PV string 1  
            In2DCV : Tension PV string 2  
            ...
    Le courant étant dépendant de la charge, intuitivement la premiere analyse 
    portera sur les données en Tension

    __Postulat 1__ :  
        La tension d'entrée de l'optimizer (In.DCV) depend de l'état des PVs
            
        
    """)

with tab2:
    st.markdown(""" __Analyse 1__  
                👉 Visualization of optimizer output : voltage, current, power  
                👉 Visualization of energy distribution / optimizer  
                👉 Statistics on Input/Output voltage""")
    st.divider()
    # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    
    if not st.session_state.df.empty:
        st.session_state.checkbox_Curves_dftab_2 = st.checkbox("Outputs Curves",
                                                               value=st.session_state.get(""),
                                                               help="OutDCV_x, OutDCA, Power")
        # st.session_state.checkbox_Statistics_dftab_2 = st.checkbox("Outputs Statistics",
        #                                                        value=st.session_state.get(""),
        #                                                        help="")
        st.session_state.checkbox_Anomalies_dftab_2 = st.checkbox("Search for anomalies on voltages",
                                                               value=st.session_state.get(""),
                                                               help="")

        if st.session_state.checkbox_Curves_dftab_2:
            with st.form(key = "Output_Analyse"):
                with st.expander("Infos : AMPT's Outputs visualisation"):
                    st.markdown(
                        """
                        <ul>
                            <li><span style='color:orange'>Voltages</span></li>
                            <li><span style='color:cyan'>Currents</span></li>
                            <li><span style='color:lime'>Power (individual / AMPTs)</span></li>
                            <li><span style='color:violet'>Aprox. Energy / AMPTs)</span></li>
                            <li><span style='color:white'>Total Power (All AMPTs)</span></li>

                        </ul>
                        """,
                        unsafe_allow_html=True
                    )
    
                # st.session_state.checkbox_Curves_df1 = st.checkbox("Display Outputs Curves",value=st.session_state.get(""),help="OutDCV_x")
        
                columns_list = (list(st.session_state.df.columns))
                # print(columns_list)
                output_voltage_columns_list = [col for col in columns_list if "OutDCV" in col]
                # print(output_voltage_columns_list)
                output_current_columns_list = [col for col in columns_list if "OutDCA" in col]
                output_power_columns_list = [col for col in columns_list if "Out_Power" in col]
               
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write("Select OutDCV..")               
                    # Sélection dynamique des courbes avec checkbox
                    st.session_state.selection_v = [col for col in output_voltage_columns_list if st.checkbox(col, value=False)]
                with col2:
                    st.write("Select OutDCA..")               
                    # Sélection dynamique des courbes avec checkbox
                    st.session_state.selection_a = [col for col in output_current_columns_list if st.checkbox(col, value=False)]
                with col3:
                    st.write("Select OutPower..")               
                    # Sélection dynamique des courbes avec checkbox
                    st.session_state.selection_p = [col for col in output_power_columns_list if st.checkbox(col, value=False)]
                with col4:
                    st.write("Others")
                    st.session_state.checkbox_energyAMPT = st.checkbox("Energy")
                    st.session_state.checkbox_All_AMPT_Power = st.checkbox("Total Power")
                    
                
                # Selection du creneau de visualisation
                # st.slider in Streamlit doesn’t natively support pandas.Timestamp objects.
                # It only supports Python’s built-in datetime.datetime, date, time, int, or float.
                # Sélection début et fin (dans la sidebar par ex.)
    
                # Extraire l'heure et les minutes seulement
                st.session_state.df["time"] = st.session_state.df["timestamp"].dt.time
                # st.dataframe(st.session_state.df.head)
                
                # Slider basé sur l’index des valeurs uniques de time
                time_values = st.session_state.df["time"].unique().tolist()
                start_idx, end_idx = st.slider(
                    "Select a range (points) :",
                    min_value=0,
                    max_value=len(time_values)-1,
                    value=(0, len(time_values)-1)
                )
                slider_nb_points = (end_idx - start_idx)
                # Sélectionner les timestamps correspondants
                start_time = time_values[start_idx]
                end_time = time_values[end_idx]
                
                # Filtrer DataFrame
                st.session_state.df_filtre = st.session_state.df[(st.session_state.df["time"] >= start_time) & (st.session_state.df["time"] <= end_time)]
                
                st.write(f"⏱ Range selected : {start_time} → {end_time}")
                # st.dataframe(df_filtre)
    
                st.session_state.form_submit_button_trace = st.form_submit_button(label = "Trace")
        
            if not st.session_state.df.empty:
                
                if st.session_state.form_submit_button_trace:
            
                    fusion_v = ["timestamp"] + st.session_state.selection_v
                    fusion_a = ["timestamp"] + st.session_state.selection_a
                    fusion_p = ["timestamp"] + st.session_state.selection_p
                    fusion_tp = ["timestamp"] + ["Out_Total_Power"]
                    
                    if st.session_state.selection_a == st.session_state.selection_v == st.session_state.selection_p == [] and not st.session_state.checkbox_energyAMPT:
                        st.warning("No datas selected !")
                    
                    if st.session_state.df_filtre.empty:
                       st.session_state.df_filtre = st.session_state.df 
                
                    # Affichage des colonnes choisies
                    # Voltage per optimizer
                    if st.session_state.selection_v !=[]:
                        # st.write("✅ Colonnes sélectionnées")
                        # st.write(fusion)
                        st.write("📈 AMPT Output Voltage")
                        st.line_chart(st.session_state.df_filtre[fusion_v], x="timestamp")
                    # Amps per optimizer 
                    if st.session_state.selection_a !=[]:
                        st.write("📊 AMPT Output Current")
                        st.line_chart(st.session_state.df_filtre[fusion_a], x="timestamp")
                    # Power per optimizer
                    if st.session_state.selection_p !=[]:
                        st.write("📊 Output Power / AMPT")
                        st.line_chart(st.session_state.df_filtre[fusion_p], x="timestamp")
                        
                    if st.session_state.checkbox_All_AMPT_Power:
                        st.write("📊 AMPT TOTAL Output Power")
                        st.line_chart(st.session_state.df_filtre[fusion_tp], x="timestamp")
                       
                    if st.session_state.checkbox_energyAMPT:
                        # --- Somme des énergies par colonne ---
                        energy_sums = st.session_state.df[[f"Out_Energy_{i}" for i in range(1, 7)]].sum()
                        
                        # --- Somme totale de toutes les énergies ---
                        total_energy = energy_sums.sum()
                        
                        # --- Affichage ---
                        st.subheader("PV Production")
                        st.warning("⚠️ Please note : approximate value (long sampling time), the AMPT is not an energy meter !")
                
                        # st.info("PV production : Approximatif")
                        # st.write("🔹 **Somme par colonne :**")
                        # st.write(energy_sums)
                        
                        st.write(f"⚡ **Total Energy : {total_energy/1000:.3f} KWh**")
                        # # --- Affichage ---
                        st.write("**Production / optimizer (Wh)**")
                        st.bar_chart(energy_sums)        
                        # --- Pie chart interactif ---
                        # st.subheader("Production Distribution")
                        fig = px.pie(
                            values=energy_sums.values,
                            names=energy_sums.index,
                            title=f"Production Distribution : {st.session_state.day}",
                            hole=0.3  # 0 = camembert plein, >0 = donut
                        )
                        
                        # # Ajouter labels avec % et valeur
                        # fig.update_traces(textinfo="label+percent+value")
                        fig.update_traces(textinfo="percent")
                        
                        st.plotly_chart(fig, use_container_width=True)
                         
    colonnesforstats = ['OutDCV_1', 'In1DCV_1', 'In2DCV_1', 'OutDCV_2', 'In1DCV_2',  
                        'In2DCV_2', 'OutDCV_3', 'In1DCV_3', 'In2DCV_3','OutDCV_4',
                        'In1DCV_4', 'In2DCV_4', 'OutDCV_5', 'In1DCV_5', 'In2DCV_5',
                        'OutDCV_6', 'In1DCV_6', 'In2DCV_6']
    
    if not st.session_state.df.empty:
        if st.session_state.checkbox_Anomalies_dftab_2:
            st.markdown("Statistics on Voltages (Input, Output")
            
            # Dictionnaire pour stocker les erreurs
            errors_report = {
                "date_generation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "anomalies": []
            }
            
            for col in colonnesforstats:
                desc = st.session_state.df[col].describe()
            
                # --- Détection d’anomalie ---
                stat_error = ""
                txt_error = ""
                seuil = 1e-6
                min_val = desc["min"]
            
                if np.isclose(min_val, 0, atol=seuil):  # tolérance 1e-6
                    stat_error = "⚠️"
                    txt_error = f"⚠️ Anomalie détectée : la valeur min de `{col}` est (quasi) nulle !"
                    
                    # compter les valeurs proches de zéro
                    nb_quasi_zero = (np.isclose(st.session_state.df[col], 0, atol=seuil)).sum()
                    mask = np.isclose(st.session_state.df[col], 0, atol=seuil)
            
                    # récupérer le premier timestamp concerné
                    if mask.any():
                        first_index = st.session_state.df[mask].index[0]
                        first_timestamp = st.session_state.df.loc[first_index, "timestamp"]
                    else:
                        first_timestamp = None
                        
                    number = int(col.split("_")[-1])  # on prend ce qui est après le dernier "_"
                    # 🔸 Enregistrer l’anomalie dans le dictionnaire JSON
                    errors_report["anomalies"].append({
                        "colonne": col,
                        "AMPT": number,
                        "type": "valeurs quasi nulles",
                        "nb_quasi_zero": int(nb_quasi_zero),
                        "premier_timestamp": str(first_timestamp),
                        "valeur_min": float(min_val)
                    })
                    
            
                # --- Affichage Streamlit ---
                with st.expander(f"{col} {stat_error}"):
                    st.table(desc.to_frame(name="Valeur").T)
                    if stat_error:
                        st.error(txt_error)
                        st.write(f"{nb_quasi_zero} valeurs sont quasi nulles.")
                        st.write(f"🕒 Première valeur quasi nulle : {first_timestamp}")
            
                   
            with st.container():
                # ✅ Transformer le JSON en texte lisible
                if errors_report["anomalies"]:
                    readable_text = f"📅 Rapport généré le : {errors_report['date_generation']}\n\n"
                    for a in errors_report["anomalies"]:
                        readable_text += (
                            f"🔸 Colonne : {a['colonne']}\n"
                            f"    Type : {a['type']}\n"
                            f"    Nb valeurs quasi nulles : {a['nb_quasi_zero']}\n"
                            f"    Première occurrence : {a['premier_timestamp']}\n"
                            f"    Valeur min : {a['valeur_min']}\n\n"
                        )
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div style="
                            border: 3px solid orange;
                            border-radius: 10px;
                            padding: 15px;
                            background-color: #1e1e1e;
                            color: white;
                            white-space: pre-wrap;
                            font-family: monospace;">
                            <h4 style="color: orange;">⚠️ Summary of detected anomalies</h4>
                            {readable_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Convertir le dictionnaire JSON en texte formaté lisible
                    json_text = json.dumps(errors_report, indent=4, ensure_ascii=False)
    
                    st.markdown(
                        f"""
                        <div style="
                            border: 3px solid orange;
                            border-radius: 10px;
                            padding: 15px;
                            background-color: #1e1e1e;
                            font-family: monospace;
                            color: white;
                            white-space: pre-wrap;">
                            <h4 style="color: orange;">⚠️ Complete json anomalies</h4>
                            <pre style="color: white;">{json_text}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )                
            with col2:
                if st.button("▶️ Save", key="Save_btn"):
                    # --- Création du dossier Anomalie ---
                    output_dir = "Anomalies"
                    os.makedirs(output_dir, exist_ok=True)
    
                    # --- Sauvegarde du rapport JSON ---
                    output_path = os.path.join(output_dir, f"errors_{st.session_state.AMPT_file_loaded}.json")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(errors_report, f, indent=4, ensure_ascii=False)                    
                        # st.success(f"✅ Rapport des anomalies enregistré dans `{output_path}`")
    
                    st.success("Saved !")
      
with tab3:
    st.markdown("Analyse 2")
    # st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    
    
    