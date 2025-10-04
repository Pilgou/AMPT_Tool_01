# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 08:12:55 2025

@author: Mamie
"""

from datetime import datetime

def delta_t(date1, date2, unite="secondes"):
    """
    Calcule la différence de temps entre deux dates.
    
    Args:
        date1, date2 : objets datetime (ou strings parsables)
        unite : "secondes", "minutes", "heures", "jours"
    
    Retourne : float (différence dans l’unité choisie)
    """
    # Si les entrées sont des strings → les convertir en datetime
    if isinstance(date1, str):
        date1 = datetime.fromisoformat(date1)
    if isinstance(date2, str):
        date2 = datetime.fromisoformat(date2)
    
    delta = date2 - date1
    secondes = delta.total_seconds()
    
    if unite == "secondes":
        return secondes
    elif unite == "minutes":
        return secondes / 60
    elif unite == "heures":
        return secondes / 3600
    elif unite == "jours":
        return secondes / 86400
    else:
        raise ValueError("Unité non reconnue. Utiliser : secondes, minutes, heures, jours")

def format_delta(date1, date2):
    """
    Calcule la différence de temps entre deux dates.
    
    Args:
        date1, date2 : objets datetime (ou strings parsables)
        unite : "secondes", "minutes", "heures", "jours"
    
    Retourne : f"{heures} heures {minutes} minutes"
    """

    delta = date2 - date1
    total_minutes = int(delta.total_seconds() // 60)
    heures, minutes = divmod(total_minutes, 60)
    return f"{heures} heures {minutes} minutes"