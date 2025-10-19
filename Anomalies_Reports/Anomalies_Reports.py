# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 05:58:59 2025

@author: Mamie
"""

import os
import re
import streamlit as st
from datetime import datetime

"""
Fonctionnement
Le script parcourt le dossier Anomalies/.
Il cherche une date au format AAAAMMJJ dans chaque nom de fichier (ex : log_20251010.txt → 2025-10-10).
Il affiche un menu déroulant (st.selectbox) avec toutes les dates trouvées.
Lorsqu’une date est sélectionnée, il liste uniquement les fichiers correspondant à cette date.
"""
def AnomaliesList()->list:
    # --- CONFIGURATION DU DOSSIER ---
    # ANOMALIES_DIR = "Anomalies"
    ANOMALIES_DIR = "C:/Users/Mamie/Documents/Python/DCS_Devices_tools/AMPT_Tool_01/Anomalies"
    
    st.title("Anomalies recorded and reports management")
    
    # --- Vérifie que le dossier existe ---
    if not os.path.exists(ANOMALIES_DIR):
        st.error(f"Le dossier '{ANOMALIES_DIR}' n'existe pas.")
    else:
        # --- Lister tous les fichiers ---
        fichiers = os.listdir(ANOMALIES_DIR)
        print("anomalie files : ", fichiers)
        # pour la recherche Retirer le préfixe "errors_" et sufixe.json
        anomalie_files_sans_prefixe = [f.replace("errors_", "") for f in fichiers] 
        anomalie_files_sans_prefixe_sufixe = [f.replace(".json", "") for f in anomalie_files_sans_prefixe]
       
        AMPT_file_loaded_sans_sufixe = st.session_state.AMPT_file_loaded.removesuffix(".csv")
        print(anomalie_files_sans_prefixe_sufixe)
        print(AMPT_file_loaded_sans_sufixe)
        # Et que le nom de fichier chargé est :
        nom_recherche = AMPT_file_loaded_sans_sufixe
        
        # Vérification
        if nom_recherche in anomalie_files_sans_prefixe_sufixe:
            # info to display in sidebar
            st.session_state.sidebarfile_Analyse = ("Check analyse")
            
        # --- Extraire la date (AAAAMMJJ) du nom du fichier ---
        pattern_date = re.compile(r"(\d{8})")
        fichiers_dates = []
    
        for f in fichiers:
            match = pattern_date.search(f)
            if match:
                date_str = match.group(1)
                try:
                    date_obj = datetime.strptime(date_str, "%Y%m%d").date()
                    fichiers_dates.append((f, date_obj))
                except ValueError:
                    pass  # si la date est invalide
        # --- Si aucun fichier avec date ---
        if not fichiers_dates:
            st.warning("Aucun fichier avec une date (AAAAMMJJ) trouvée dans le dossier.")
        else:
            # --- Créer une liste unique de dates disponibles ---
            dates_uniques = sorted(list({d for _, d in fichiers_dates}))
            # print(dates_uniques)

        # --- Sélecteur de date ---
        date_selectionnee = st.selectbox("📅 Select date :", dates_uniques)

        # --- Filtrer les fichiers de cette date ---
        fichiers_selectionnes = [f for f, d in fichiers_dates if d == date_selectionnee]
        files_number = len(fichiers_selectionnes)
        st.write(f"{files_number} files found")
        st.subheader(f"{date_selectionnee.strftime('%Y/%m/%d')} files")
        for fichier in fichiers_selectionnes:
            st.markdown(f"- {fichier}")

if __name__ == '__main__':
    
    path_source_file = "C:/Users/Mamie/Documents/Python/DCS_Devices_tools/BESS_Tool_01/data_BESS.db"
    target_folder = "C:/Users/Mamie/Documents/Python/DCS_Devices_tools/BESS_Tool_01/Archives"
    AnomaliesList()