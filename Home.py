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
with col1:
    # st.image(os.path.join(current_path,"images","logoSCSystems.jpg"))#,width=200)
    st.image(".\images\logoSCSystems.jpg")
with col2:
    # st.image(os.path.join(current_path,"images","AMPT.jpg"),width=250)#,width=200)
    st.image(".\images\AMPT.jpg",width=250)

tab1, tab2 = st.tabs(["Settings", "Projects"])

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
