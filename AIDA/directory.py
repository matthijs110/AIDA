import os
import glob
import logging as log
from sys import exit
import hashlib

def create_or_empty(directory):
    if(os.path.isdir(directory)):
        log.info(f"Directory ({directory}) found.")

        # Remove all files if directory is not emtpy
        clear_directory(directory)
    else:
        create(directory)

def check(directory, name):
    if(not os.path.isdir(directory)):
        answer = input(f"{name} ({directory}) does not exist. Do you want to create it? [Y/n] ")

        if(answer.upper() == "Y" or answer == ""):
            create(directory)
        else:
            log.error("Please create the directory before continuing.")
            exit()

    else:
        log.info(f"{name} ({directory}) found.")

def check_bbox_hash(config):

    bbox_string = f'{config["bbox"]["srs"]}{config["bbox"]["west"]}{config["bbox"]["south"]}{config["bbox"]["east"]}{config["bbox"]["north"]}'
    bbox_hash = str(hashlib.md5(bbox_string.encode('utf-8')).hexdigest())

    if(not os.path.isfile(f"{config['directory']['tmp']}/images/{bbox_hash}")):
        log.info("No hash file found.")

        clear_directory(f"{config['directory']['tmp']}/images/all")
        clear_directory(f"{config['directory']['tmp']}/images")

        f = open(f"{config['directory']['tmp']}/images/{bbox_hash}", "a")
        f.close()
    else:
        log.info("Correct hash file found.")

def create(directory):
    if(not os.path.isdir(directory)):
        try:
            os.makedirs(directory)
            log.info(f"Directory ({directory}) created successfully")
        except OSError as e:
            log.error(f"Could not create directory ({directory})")
            log.info(e)
            log.error("Exiting...")
            exit()
    else:
        log.info(f"Directory ({directory}) found.")

def clear_directory(directory):
    if(len(glob.glob(directory + "/*")) != 0):
        for f in glob.glob(directory + "/*"):
            try:
                if(os.path.isfile(f)):
                    os.remove(f)
                    log.info(f"File ({f}) Removed.")
            except Exception as e:
                log.error(f"Could not remove file ({f})")
                log.info(e)
                log.error("Exiting...")
                exit()
