import argparse
import os
import yaml
import schemas
import logging as log
import glob
from cerberus import Validator

def main():
    # Setting up parser with all arguments
    parser = argparse.ArgumentParser(description='Download and analyze arial imagery.', prog='AIDA')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0-dev')
    parser.add_argument('-v', "--verbose", action="store_true", help="run progam in verbose mode")
    parser.add_argument('config', help='imports a configuration file')
    args = parser.parse_args()

    # If verbose flag is true change logging config to debug level so info is showed.
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    try:
        # Try to open config file
        with open(args.config) as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)

        # Validate config file
        v = Validator(schemas.yml_schema)
        valid_yaml = v.validate(config)

        # When config file is not valid, throw error, otherwise start program.
        if(not valid_yaml):
            log.error("Your configuration file was not valid.")
            log.error(v.errors)
        else:
            start(config)

    except FileNotFoundError:
        log.error("File could not be found.")
    except Exception as e:
            log.error("File can be found, but something went wrong.")
            log.error(e)

def start(config):
    log.info("Config loaded succesfully.")

    if(not os.path.isdir(config['tmpdirectory'])):
        answer = input("Temp directory (" + config['tmpdirectory'] + ") does not exist. Do you want to create it? [Y/n] ")

        if(answer.upper() == "Y" or answer == ""):
            if(not create_directory(config['tmpdirectory'])):
                return
    else:
        log.info("Temp directory (" + config['tmpdirectory'] + ") found.")
    
    # check other directories

def create_directory(directory):
    try:
        os.makedirs(directory)
        log.info("Directory created successfully")
        return True
    except OSError:
        log.error("Could not create directory")
        return False


main()