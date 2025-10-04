# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 13:01:58 2025

@author: Mamie
"""

import os
import glob
import string
from ctypes import windll


def get_drives()->list:
    """drives list in this computer
    return a list of drives"""
    drives_list = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives_list.append(letter)
        bitmask >>= 1
    return drives_list

def search_files_by_extension(path: str, ext: str) -> list:
    """list of files with a given extension
    param path : directory path for reshearch
    param ext : extention
    return : List of path, list of file name
    """
    list_path = []  # Paths list
    list_file = []  # Files name list
    
    try:
        # construction filtre sur fichiers .ini
        folder_path = ("{}/*{}").format(path, ext)
        # Looking for .ini files
        list_path.append(glob.glob(folder_path))
        
    except Exception:
        print(" No '*.{ext}' file in this folder")
        
    if len(folder_path) > 1:
        for filePath in list_path[0]:
            path = os.path.normpath(filePath)
            pathSplit = path.split(os.sep)
            # print(pathSplit[len(pathSplit)-1])
            list_file.append(pathSplit[len(pathSplit)-1])
        # print(list_file)


    return list_path[0], list_file
    

def ReadFile(file2Read:str): 
    """ Read file
    param : path of file2read
    
    return lines : list of lines
    return file_name : without extension
    """
    # Ouvrir le fichier en lecture seule
    file = open(file2Read, "r")

    # utiliser readlines pour lire toutes les lignes du fichier
    # La variable "lignes" est une liste contenant toutes les lignes du fichier
    lines = file.readlines()
    file.close()
    #print("file openned :",fileName)

    # print("file openned : ",file2Read)
    fileName1 = file2Read.split(".")[0]
    # print(fileName1)
    fileName = fileName1.split("\\")
    print("File Name : ", fileName[len(fileName)-1])
    
    return lines, fileName

def move_rename_if_duplicate(path_source_file, target_folder):
    """ Move a file and rename it if same name already exist
    """

    # file name and ext Extraction
    extr1 = path_source_file.split("/")
    file_name = extr1[len(extr1)-1]
    ext = file_name.split(('.'))[1]

    json_in_targetfolder = []
    # Travers all the branch of a specified path
    print("Listing json file in target folder :")
    for dirpath, dirnames, filenames in os.walk(target_folder):
       for filename in filenames:
          if filename.endswith(f'.{ext} '):
             json_in_targetfolder.append(filename)
    print(json_in_targetfolder)
    
    
    
    # # isolate base / extention of file name
    # base, ext = os.path.splitext(file_name)
    # print(base,ext)
    # # Check if folder or file exist
    # print(os.path.exists(target_folder))
    # print(target_folder)
    # target_test = (target_folder + "/" + file_name)
    # if not(os.path.exists(target_test)):
    #     print("file {} doesn't exist in {} folder".format(file_name, target_folder))
    # else:
    #     print("! file {} already exist in {} folder".format(file_name, target_folder))
 
    
    # file_mame = 
    # base, ext = os.path.splitext(filename)
    # extensions = {".txt"} # use a set for a collection just to look up in
    
    # for root, dirs, files in os.walk(source_dir):
    #     for filename in files:
    #         base, ext = os.path.splitext(filename)
    #         if ext in extensions:
    #             src_path = os.path.join(root, filename)
    #             dup = 0
    #             while True:
    #                 dst_path = os.path.join(target_folder, filename)
    #                 if not os.path.exists(dst_path):
    #                     break
    #                 dup += 1
    #                 filename = f'{base}_{dup}{ext}'
    #             os.rename(src_path, dst_path)

if __name__ == '__main__':
    
    # drives_list = get_drives()
    # # print ("!drives list : ", drives_list  )
    # r = (search_files_by_extension("C:/Users/Mamie/Documents/Python/DCS_Devices_tools/BESS_Tool_01/AM_ini_files", ".ini"))
    # list_strings = r[1]
    # print(list_strings)
    # print(search_chars_in_string_list(list_strings, "generated"))
    path_source_file = "C:/Users/Mamie/Documents/Python/DCS_Devices_tools/BESS_Tool_01/data_BESS.db"
    target_folder = "C:/Users/Mamie/Documents/Python/DCS_Devices_tools/BESS_Tool_01/Archives"
    move_rename_if_duplicate(path_source_file, target_folder)