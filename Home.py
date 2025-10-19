# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 21:32:07 2025
Streamlit FrontEnd Home page

@author: Mamie
"""

import streamlit as st
import os
import json
import pandas as pd
from Anomalies_Reports import Anomalies_Reports as ar
from Sidebar import side_bar as sb


# Clear shell
os.system("cls")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
    
if "df_carlo" not in st.session_state:
    st.session_state.df_carlo = pd.DataFrame()

if "input_AMPTdatasheet" not in st.session_state:
    st.session_state.input_AMPTdatasheet = {}

if "output_AMPTdatasheet" not in st.session_state:
    st.session_state.output_AMPTdatasheet = {}

if "indexModel" not in st.session_state:
    st.session_state.indexModel = 2
    # --- Charger le JSON AMPT_Datasheet ---
    with open(".\Details_Projects_Devices\AMPT_Datasheet.json", "r") as f:
        st.session_state.datasheet = json.load(f)

if "AMPT_file_loaded" not in st.session_state:
    st.session_state.AMPT_file_loaded = ""

if "EM_file_loaded" not in st.session_state:
    st.session_state.EM_file_loaded = ""
    
if "selected_project" not in st.session_state:
    st.session_state.selected_project = "Solaris"

    # --- Charger le fichier JSON Project_Details ---
    with open(".\Details_Projects_Devices\Project_Details.json", "r") as file:
        st.session_state.project_data = json.load(file)
        
    # --- Trouver le projet sélectionné ---
    st.session_state.project = next((p for p in st.session_state.project_data["projects"] if p["name"] == st.session_state.selected_project), None)

    

st.title ("DC Tools suite")

st.markdown(
    """
    Tools to help analyse data and configurate DC Microgrid devices.  
    
""")

st.markdown(
    "<h2 style='text-align: center; font-size:22px;'>Project selected</h2>",
    unsafe_allow_html=True
)
st.divider()

col10, col11 = st.columns([1,3])
with col10:
    st.markdown(
        f"<h3 style='text-align: center; color: orange;'>{st.session_state.selected_project}</h3>",
        unsafe_allow_html=True
    )
    # st.write(st.session_state.selected_project)
with col11:
    st.info(st.session_state.project['description']['installation_type'])
    # st.markdown(("Type d'installation", ", ".join(st.session_state.project['description']['installation_type'])), unsafe_allow_html=True)
    # st.markdown("[Datasheet](https://www.ampt.com/wp-content/uploads/2023/08/Ampt_i13.5_1000Vsys__Datasheet_EN_51770007-1P.pdf)")

st.divider()

current_path = os.getcwd()


col1, col2 = st.columns(2)
# with col1:
#     # st.image(os.path.join(current_path,"images","logoSCSystems.jpg"))#,width=200)
#     st.image(".\images\logoSCSystems.jpg")
# with col2:
#     # st.image(os.path.join(current_path,"images","AMPT.jpg"),width=250)#,width=200)
#     st.image(".\images\AMPT.jpg",width=250)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Settings", "Projects", "Optimizers", "Anomalies", "About"])

with tab1:

    FILENAME = "settings.json"
    
    # Valeurs par défaut
    DEFAULT_SETTINGS = {
        "seuil_quasi_zero": 1e-6,
        "colonnes_a_surveiller": ["OutDCV_1", "OutDCV_2", "OutDCV_3", "OutDCV_4", "OutDCV_5", "OutDCV_6"],
        "affichage": {
            "theme": "dark",
            "couleur_warning": "orange",
            "couleur_error": "red"
        }
    }
    
    def load_settings(filename=FILENAME):
        """Charge les paramètres depuis le JSON, ou valeurs par défaut si absent/corrompu"""
        if not os.path.exists(filename):
            return DEFAULT_SETTINGS
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_SETTINGS
    
    def update_settings(new_settings, filename=FILENAME):
        """Sauvegarde les paramètres dans un fichier JSON"""
        with open(filename, "w") as f:
            json.dump(new_settings, f, indent=4)
    
    # Charger paramètres existants
    settings = load_settings()
    
    # 🖥️ Zone paramètres dans la page principale
    st.header("⚙️ Software parameters")
    
    # Slider pour seuil
    seuil = st.number_input(
        "Seuil quasi nul",
        value=settings["seuil_quasi_zero"],
        step=1e-6,
        format="%.6f"
    )
    
    
    # Deux colonnes pour les boutons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Sauvegarder les paramètres"):
            settings["seuil_quasi_zero"] = seuil
            update_settings(settings)
            st.success("✅ Paramètres sauvegardés")
    
    with col2:
        if st.button("♻️ Réinitialiser les paramètres"):
            update_settings(DEFAULT_SETTINGS)
            st.warning("⚠️ Paramètres réinitialisés aux valeurs par défaut")

# Project details tab            
with tab2:
    
    # --- Sélecteur de projet ---
    project_names = [p["name"] for p in st.session_state.project_data["projects"]]
    nouveau_choix = st.selectbox("📁 Select a projet :", project_names)
    if nouveau_choix != st.session_state.selected_project:
        st.session_state.selected_project = nouveau_choix
        st.rerun()  # Force le rafraîchissement pour mettre à jour l'affichage amont
    
    # --- Trouver le projet sélectionné ---
    st.session_state.project = next((p for p in st.session_state.project_data["projects"] if p["name"] == st.session_state.selected_project), None)
   
    if st.session_state.project:
        st.title(f"🔆 Projet : {st.session_state.project['name']}")
    
        # --- Style HTML pour différencier clé/valeur ---
        def styled_item(key, value, color_key="#00B4D8", color_value="#F0F0F0"):
            return f"<b style='color:{color_key}'>{key} :</b> <span style='color:{color_value}'>{value}</span>"
    
        # === SECTION DESCRIPTION ===
        st.header("Description Générale")
        st.markdown(styled_item("Adresse", st.session_state.project['description']['address']), unsafe_allow_html=True)
        gps = st.session_state.project['description']['gps_coordinates'] or "Non spécifié"
        st.markdown(styled_item("Coordonnées GPS", gps), unsafe_allow_html=True)
        st.markdown(styled_item("Type d'installation", ", ".join(st.session_state.project['description']['installation_type'])), unsafe_allow_html=True)
    
        # === SECTION SPÉCIFICATIONS ===
        st.header("Spécifications Techniques")
    
        # PV Section
        pv = st.session_state.project["specifications"]["PV"]
        st.subheader("☀️ Photovoltaïque (PV)")
        st.markdown(styled_item("Puissance PV", f"{pv['power_kwp']} kWp"), unsafe_allow_html=True)
        st.markdown(styled_item("Modèle PV", pv['PV model']), unsafe_allow_html=True)
        st.markdown(styled_item("Nb PV", pv['Nb_PV']), unsafe_allow_html=True)
        st.markdown(styled_item("Modèle Optimizer", pv['optimizer_model']), unsafe_allow_html=True)
    
        # BESS Section
        bess = st.session_state.project["specifications"]["BESS"]
        st.subheader("🔋 BESS (Battery Energy Storage System)")
        st.markdown(styled_item("Model", bess['Model'] or "Non spécifié"), unsafe_allow_html=True)
        st.markdown(styled_item("Nombre de batteries", bess['Nb batteries'] or "Non spécifié"), unsafe_allow_html=True)
        st.markdown(styled_item("Puissance", f"{bess['Power kw Total'] or 'Non spécifiée'} kW"), unsafe_allow_html=True)
        st.markdown(styled_item("Capacité", f"{bess['Capacity kwh Total'] or 'Non spécifiée'} kWh"), unsafe_allow_html=True)
        st.markdown(styled_item("Tension", f"{bess['Voltage v']} V"), unsafe_allow_html=True)
    
        # ESEV Section
        st.subheader("🚗 ESEV (Bornes de Recharge)")
        for i, ev in enumerate(st.session_state.project["specifications"]["ESEV"], start=1):
            st.markdown(styled_item(f"Borne {i}", f"{ev['brand']} — {ev['power_kw']} kW"), unsafe_allow_html=True)
    
    else:
        st.error(f"Projet '{st.session_state.selected_project}' non trouvé dans le fichier JSON.")

# AMPT Datasheet tab               
with tab3:

    # --- Extraire la liste des modèles ---
    models = st.session_state.datasheet["models"]

    st.markdown("<h3 style='color:orange;'>⚙️ Select AMPT</h3>", unsafe_allow_html=True)
    
    # # --- Sélection par défaut : "V900" ---
    # default_index = models.index("V900") if "V900" in models else 0
    
    # --- Sélecteur radio horizontal ---
    st.session_state.selected_model = st.radio(
        "Choose model :", 
        models, 
        horizontal=True,
        index=st.session_state.indexModel,  # 👈 ici le modèle V900 est pré-sélectionné
        key="model_selector"
    )

    # --- Trouver l'index du modèle sélectionné ---
    st.session_state.indexModel = models.index(st.session_state.selected_model)
    # print(st.session_state.indexModel)

    # --- Récupérer les données ---
    st.session_state.input_AMPTdatasheet = st.session_state.datasheet["Electrical"]["Input"]
    st.session_state.output_AMPTdatasheet = st.session_state.datasheet["Electrical"]["Output"]
    # print(st.session_state.datasheet["Electrical"]["Input"]["Maximum voltage per input (V)"][st.session_state.indexModel])
    # print(st.session_state.input_AMPTdatasheet["Maximum voltage per input (V)"][st.session_state.indexModel])

    # --- Affichage stylé ---
    st.markdown(
        f"""
        <div style="
            border: 3px solid orange;
            border-radius: 12px;
            padding: 20px;
            background-color: #1e1e1e;
            margin-top: 20px;">
            <h3 style="color:orange;">DataSheet : <span style="color:white;">{st.session_state.selected_model}</span></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Disposition en deux colonnes ---
    col1, col2 = st.columns(2)

        # INPUT
    with col1:
        st.markdown("<h4 style='color:#ffa500; text-align:center;'>Input</h4>", unsafe_allow_html=True)
        for key, values in st.session_state.input_AMPTdatasheet.items():
            value = values[st.session_state.indexModel]
            st.markdown(
                f"""
                <p style='margin:2px 0;'>
                    <b style='color:#00B4D8;'>{key}</b> :
                    <span style='color:#FFFFFF;'>{value}</span>
                </p>
                """,
                unsafe_allow_html=True
            )
    
    # OUTPUT
    with col2:
        st.markdown("<h4 style='color:#ffa500; text-align:center;'>Output</h4>", unsafe_allow_html=True)
        for key, values in st.session_state.output_AMPTdatasheet.items():
            value = values[st.session_state.indexModel]
            st.markdown(
                f"""
                <p style='margin:2px 0;'>
                    <b style='color:#00B4D8;'>{key}</b> :
                    <span style='color:#FFFFFF;'>{value}</span>
                </p>
                """,
                unsafe_allow_html=True
            )
    st.image(os.path.join(current_path,"images","AMPT.jpg"),width=250)#,width=200)
    st.markdown("[AMPT web site](https://www.ampt.com/products/string-optimizers)")

with tab4:
    st.write("Anomalies recorded")
    
    ar.AnomaliesList()

with tab5:
    with st.expander("Python scrips description"):
        st.markdown(
            """
            ### Python scrips description :   
                01_xxx.py / Load CSV files from AMPT-CU gateway
                02_xxx.py / Analyse CSV files from AMPT-CU gateway  
                03_xxx.py /   
                04_xxx.py /   
                05_xxx.py /   
                06_xxx.py /   
                07_xxx.py /   
        
            ###   
            
        """)
sb.common_part()

