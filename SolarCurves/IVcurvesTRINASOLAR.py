# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 07:36:38 2025

@author: Mamie
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px

# --- Titre ---
st.title("I–V Curves of PV Module (430 W)")
st.subheader("BIFACIAL DUAL GLASS  N type i-TOPCon MODULE")
st.write("TrinaSolar")

# --- Charger le fichier JSON ---
uploaded_file = st.file_uploader("📂 Importer le fichier JSON", type=["json"])

if uploaded_file is not None:
    # Lecture du contenu
    data = json.load(uploaded_file)
    pv_data = data["PV_Module_430W"]

    # Préparer les données pour Plotly
    all_data = []
    for irradiance, points in pv_data.items():
        df = pd.DataFrame(points)
        df["Irradiance"] = irradiance
        all_data.append(df)
    df_all = pd.concat(all_data, ignore_index=True)

    # --- Affichage interactif ---
    fig = px.line(
        df_all,
        x="Voltage(V)",
        y="Current(A)",
        color="Irradiance",
        title="I–V Curves for Different Irradiance Levels",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Affichage du tableau ---
    with st.expander("Voir les données brutes"):
        st.dataframe(df_all)
else:
    st.info("⬆️ Charge ton fichier JSON pour afficher les courbes.")
