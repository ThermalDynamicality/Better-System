"""
File: main.py
Name: Stanley Goodwin   
Date: 5/11/2022

Description:
    A simple program that reads from a JSON file to detect changes in particular
    folders and reporting back in the log file.
"""
from os import listdir
from json import load
from time import sleep


# Pre-Init
with open("system_check.json", "r") as f:
    SETTINGS = load(f)
DURATION = SETTINGS["duration"]
EXCLUDE = SETTINGS["exclude"]
FOLDERS = SETTINGS["folders"]


# Loop
while True:

    # Change log folder
    CHANGE_FILE = open("log.dat", "a+")

    # For all folders specified
    for folder in FOLDERS:

        # Stored data file
        top = str(folder[3:].replace("\\", " - "))
        stored_file = open(f"data/{top}.dat", "a+")
        stored_file.seek(0)
        stored_list = [i.strip() for i in stored_file.readlines()]

        # Lists file currently in directory
        current_list = [i for i in listdir(folder) if i not in EXCLUDE]

        # Adds new programs to data files
        new_files = [i for i in current_list if i not in stored_list]
        for program in new_files:
            CHANGE_FILE.write(f"Added File: {folder}\\{program}\n")
            stored_file.write(f"{program}\n")
        stored_file.close()

        # Adds old program to log files
        old_files = [i for i in stored_list if i not in current_list]
        for program in old_files:
            CHANGE_FILE.write(f"Removed File: {folder}\\{program}\n")
        
        # Removes old programs from data files
        with open(f"./data/{top}.dat", "r") as f:
            lines = f.readlines()
        with open(f"./data/{top}.dat", "w") as f:
            for line in [i for i in lines if i.strip() in current_list]: 
                f.write(line)

    # Finisher
    CHANGE_FILE.close()
    sleep(DURATION)