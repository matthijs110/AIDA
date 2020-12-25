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
import sys
import numpy
import imageRange
import downloader
import progressBar
import threadsHelper
import threading

stdoutHandler = log.StreamHandler(sys.stdout)

def main():
    # Setting up parser with all arguments
    parser = argparse.ArgumentParser(description='Download and analyze arial imagery.', prog='AIDA')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0-dev')
    parser.add_argument('-v', "--verbose", action="store_true", help="run progam in verbose mode")
    parser.add_argument('config', help='imports a configuration file')
    args = parser.parse_args()

    # Setup logging
    root = log.getLogger()
    root.setLevel(log.DEBUG)

    # If verbose flag is true change logging config to debug level so info is showed.
    if args.verbose:
        stdoutHandler.setLevel(log.DEBUG)
    else:
        stdoutHandler.setLevel(log.WARNING)

    formatter = log.Formatter('[%(levelname)s] %(message)s')
    stdoutHandler.setFormatter(formatter)
    root.addHandler(stdoutHandler)

    # Setup logging to file
    fileHandler = log.FileHandler("debug.log")
    fileHandler.setLevel(log.DEBUG)
    formatter = log.Formatter('%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s')
    fileHandler.setFormatter(formatter)
    root.addHandler(fileHandler)

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

    # bla
    tempsize = int(config["image"]["tempsize"])
    size = int(config["image"]["size"])
    if((not (tempsize / size).is_integer()) or tempsize <= 0 or size <= 0):
        log.error("Image size/tempsize are incorrect. Please review your input and check the documentation.")
        exit()


    # Check if threads are avaiable
    max_threads = multiprocessing.cpu_count() * 2
    if(int(config["threads"]) > max_threads):
        log.error("Trying to allocate too many threads. MAX: " + str(max_threads))
        exit()

    log.info(f"{config['threads']}/{max_threads} threads allocated.")

    # Remove logging to stdout
    log.getLogger().removeHandler(stdoutHandler)

    print("Starting downloader...")
    time.sleep(0)

    # Get range for temp images
    temp_range = imageRange.get_range(
        mode = "bbox", 
        config = config, 
        size = config['image']['tempsize'])

    # Create printing thread
    print_queue = status.printQueue()

    # Create threads
    image_directory = f"{config['tmpdirectory']}/images/all"
    threads = threadsHelper.create(temp_range, image_directory, config['image']['tempsize'], config)

    # Initialize status
    total_number_of_images = threadsHelper.get_total(threads)
    pbTotal = status.init("Downloading images", total_number_of_images, print_queue)

    # Add progress bar to each thread
    threadsHelper.add_progress_bar(threads, print_queue)

    # Add total progress bar to each thread
    threadsHelper.add_total_progress_bar(threads, pbTotal)

    # Start threads

    print_queue.start()
    threadsHelper.start(threads)
  
    log.info("All threads started")

    # Wait for download to be finished by looping until active threading count drops below 3.
    try:
        while threading.active_count() > 2:
            pass
    # When crtl + c is pressed end all threads and exit.
    except (KeyboardInterrupt, SystemExit):
        log.error("EXIT")
        threadsHelper.stop(threads)
        print_queue.stop()
        exit()

    time.sleep(1)
    print_queue.stop()

    log.info("Finished downloading temp images")

    os.system('cls')

    print("Finished downloading!")
    print("Starting Anaylyzer...")

    time.sleep(0)


    
main()