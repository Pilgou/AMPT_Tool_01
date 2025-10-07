# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 21:32:07 2025
Streamlit FrontEnd

@author: Mamie
"""

import streamlit as st
import os
import json

st.title ("DC Tools suite")

st.markdown(
    """
    Tools to help analyse data and configurate DC Microgrid devices.  
    
""")
st.divider()

col10, col11 = st.columns([1,3])
with col10:
    AMPT_selector = st.radio("Select project (if exist)",("Solaris", "not yet created"))
with col11:
    with st.container(border=True):
        if AMPT_selector == "Solaris":
            st.markdown(f"I")
            st.markdown(f"I")
            st.markdown(f"I")
        else :
            st.markdown(f"")
            st.markdown("...")
        # st.markdown("[Datasheet](https://www.ampt.com/wp-content/uploads/2023/08/Ampt_i13.5_1000Vsys__Datasheet_EN_51770007-1P.pdf)")
st.divider()

current_path = os.getcwd()

st.markdown(
    """
    ### For AMPT PV Solar Optimizer   
        01_xxx.py / extract data from AMPT configuration file  
        02_xxx.py / analyse CSV files from AMPT-CU gateway  
    ###   
    
""")


col1, col2 = st.columns(2)
# with col1:
#     # st.image(os.path.join(current_path,"images","logoSCSystems.jpg"))#,width=200)
#     st.image(".\images\logoSCSystems.jpg")
# with col2:
#     # st.image(os.path.join(current_path,"images","AMPT.jpg"),width=250)#,width=200)
#     st.image(".\images\AMPT.jpg",width=250)

tab1, tab2, tab3 = st.tabs(["Settings", "Projects", "Optimizers"])

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
            
with tab2:
    st.write("Different projects description")
    
with tab3:
    # --- Charger le JSON ---
    with open(".\Details_Projects_Devices\AMPT_Datasheet.json", "r") as f:
        datasheet = json.load(f)

    # --- Extraire la liste des modèles ---
    models = datasheet["models"]

    st.markdown("<h2 style='color:orange;'>⚙️ Select AMPT</h2>", unsafe_allow_html=True)
    
    # --- Sélection par défaut : "V900" ---
    default_index = models.index("V900") if "V900" in models else 0
    
    # --- Sélecteur radio horizontal ---
    selected_model = st.radio(
        "Choose model :", 
        models, 
        horizontal=True,
        index=default_index,  # 👈 ici le modèle V900 est pré-sélectionné
        key="model_selector"
    )

    # --- Trouver l'index du modèle sélectionné ---
    index = models.index(selected_model)

    # --- Récupérer les données ---
    input_data = datasheet["Electrical"]["Input"]
    output_data = datasheet["Electrical"]["Output"]

    # --- Affichage stylé ---
    st.markdown(
        f"""
        <div style="
            border: 3px solid orange;
            border-radius: 12px;
            padding: 20px;
            background-color: #1e1e1e;
            margin-top: 20px;">
            <h3 style="color:orange;">DataSheet : <span style="color:white;">{selected_model}</span></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Disposition en deux colonnes ---
    col1, col2 = st.columns(2)

    # INPUT
    with col1:
        st.markdown("<h4 style='color:#ffa500;'>Input</h4>", unsafe_allow_html=True)
        for key, values in input_data.items():
            st.markdown(f"<p style='color:white;'>• <b>{key}</b> : {values[index]}</p>", unsafe_allow_html=True)

    # OUTPUT
    with col2:
        st.markdown("<h4 style='color:#ffa500;'>Output</h4>", unsafe_allow_html=True)
        for key, values in output_data.items():
            st.markdown(f"<p style='color:white;'>• <b>{key}</b> : {values[index]}</p>", unsafe_allow_html=True)

