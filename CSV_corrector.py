# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 10:50:11 2025
!correcteur de fichier csv
@author: Mamie
"""

import os
import pandas as pd

# Clear shell
os.system("cls")
fileName = "ampt_20250901"

df = pd.read_csv(f"./CSV/{fileName}.csv")
print(f"open file {fileName}")
print(df.head())
# df.drop_duplicates()
df = df[df["timestamp"] != "timestamp"]
print(df.head())
# Sauvegarde en CSV
df.to_csv(f"./CSV/{fileName}C.csv", index=False)
print(f"Corrections save in file : {fileName}C")