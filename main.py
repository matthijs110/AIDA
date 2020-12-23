import argparse
import os
import yaml
import schemas
import logging as log
import glob
from cerberus import Validator
import directory
import multiprocessing
import status
import time

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

        # When config file is not valid, throw error and exit
        if(not valid_yaml):
            log.error("Your configuration file was not valid.")
            log.error(v.errors)
            exit()

    except FileNotFoundError:
        log.error("File could not be found.")
        exit()
    except Exception as e:
        log.error("File can be found, but something went wrong.")
        log.error(e)
        exit()
    
    start(config)

def start(config):
    log.info("Config loaded succesfully.")

    # Create or emtpy all directories
    directory.check(config["tmpdirectory"], "Temp directory")
    directory.create_or_empty(f"{config['tmpdirectory']}/images")
    directory.create_or_empty(f"{config['tmpdirectory']}/images/all")
    directory.create_or_empty(f"{config['tmpdirectory']}/images/analyzed/set1")
    directory.create_or_empty(f"{config['tmpdirectory']}/images/analyzed/set2")
    directory.create_or_empty(f"{config['tmpdirectory']}/index")
    directory.create_or_empty(f"{config['tmpdirectory']}/xml")
    directory.check(config["image"]["directory"], "Image directory")

    log.info("All directories created/emptied succesfully.")

    max_threads = multiprocessing.cpu_count() * 2

    if(int(config["threads"]) > max_threads):
        log.error("Trying to allocate too many threads. MAX: " + str(max_threads))
        exit()

    log.info(f"{config['threads']}/{max_threads} threads allocated.")

    print("Starting downloader...")
    #time.sleep(1)

    status.updateStatus()


main()