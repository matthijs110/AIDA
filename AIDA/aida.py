import os
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import analyzer 
import downloader 
import progressBar 
import imageRange 
import directory 
import indexer 
import report 
import schemas 
import threadsHelper 

import threading
import numpy
import sys
import time
import status
import multiprocessing
from cerberus import Validator
import glob
import logging as log
import yaml
import argparse
from datetime import datetime
import shutil

stdoutHandler = log.StreamHandler(sys.stdout)
VERSION = "1.0.0"

def main():
    start_time = datetime.now()

    args = setup_parser()
    setup_logging(args)
    config = get_configuration(args)
    check_config(config)

    # Remove logging to stdout
    log.getLogger().removeHandler(stdoutHandler)

    # Download temp images
    number_temp_of_images = download_temp_images(config)

    # Analyze images
    number_of_buildup_images = analyze_images(config, number_temp_of_images)

    # Index build-up images
    number_of_images = index_images(config)

    # Download final images
    download_final_images(config)

    # Clean up
    clean_up(config)

    # End
    end_time = datetime.now()
    total_time = end_time - start_time

    data = {
        "number_of_analyzed_images": number_temp_of_images,
        "number_of_images": number_of_images,
        "number_of_buildup_images": number_of_buildup_images,
        "total_time": str(total_time).split(".")[0],
        "version": VERSION
    }

    print_end_report(config, data)
    log.info("Finished.")

def setup_parser():
    """Sets up the parser

    Returns:
        args: args
    """

    # Setting up parser with all arguments
    parser = argparse.ArgumentParser(description='Download and analyze arial imagery.', prog='AIDA')
    parser.add_argument('--version', action='version', version='%(prog)s '+ VERSION)
    parser.add_argument('-v', "--verbose", action="store_true", help="run progam in verbose mode")
    parser.add_argument('config', help='imports a configuration file')
    args = parser.parse_args()
    
    return args

def setup_logging(args):
    """Sets logging

    Returns:
        args: args
    """

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


def get_configuration(args):
    """Returns config and validates config

    Args:
        args (args): args from parser

    Returns:
        object: Configuration json object
    """

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

    return config


def check_config(config):
    """Prepares folders and checks if configuration is set correctly

    Args:
        config (object): configuration json object
    """

    # Create or emtpy all directories
    directory.check(config["tmpdirectory"], "Temp directory")
    directory.create_or_empty(f"{config['tmpdirectory']}/images")
    directory.create(f"{config['tmpdirectory']}/images/all")
    directory.create_or_empty(f"{config['tmpdirectory']}/images/filtered")
    directory.create_or_empty(f"{config['tmpdirectory']}/index")
    directory.create_or_empty(f"{config['tmpdirectory']}/xml")
    directory.check(config["image"]["directory"], "Image directory")

    log.info("All directories created/emptied succesfully.")

    # Check if Projection is correct
    if(config["image"]["projection"] != "EPSG:28992"):
        log.error("Projection is not set to EPSG:28992. In this version of AIDA you must use EPSG:28992. Please review your config file.")
        exit()

    # Check if tempsize and image size are ok
    tempsize = int(config["image"]["tempsize"])
    size = int(config["image"]["size"])
    if((not (tempsize / size).is_integer()) or tempsize <= 0 or size <= 0):
        log.error(
            "Image size/tempsize are incorrect. Please review your input and check the documentation.")
        exit()

    # Check if threads are avaiable
    max_threads = multiprocessing.cpu_count() * 2
    if(int(config["threads"]) > max_threads):
        log.error("Trying to allocate too many threads. MAX: " + str(max_threads))
        exit()

    log.info(f"{config['threads']}/{max_threads} threads allocated.")

def download_temp_images(config):
    """Downloads the temp images data set

    Args:
        config (object): configuration json object
    """

    print("Starting downloader...")
    time.sleep(1)

    # Get range for temp images
    temp_range = imageRange.get_range(
        mode="bbox",
        config=config,
        size=config['image']['tempsize'])

    # Create printing thread
    print_queue = status.printQueue()

    # Create threads
    image_directory = f"{config['tmpdirectory']}/images/all"
    threads = threadsHelper.create(
        temp_range, image_directory, config['image']['tempsize'], config)

    # Initialize status
    total_number_of_images = threadsHelper.get_total(threads)
    pbTotal = status.init("Downloading temp images",
                          total_number_of_images, print_queue)

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

    os.system('cls')
    print("Finished downloading!")
    log.info("Finished downloading temp images")

    return total_number_of_images

def analyze_images(config, total_number_of_images):
    """Analyzes the images using machine learning

    Args:
        config (object): configuration json object
    """

    print("Starting Anaylyzer...")
    log.info("Analyzer started")
    time.sleep(1)

    # Initialize status
    pbTotal = status.init("Analyzing images",
                          total_number_of_images, "NOQUEUE")
    status.bottomLine = 18

    number_of_images = 0 

    # Analyze images
    try:
        number_of_images = analyzer.analyze(config, pbTotal)
    except (KeyboardInterrupt, SystemExit):
        log.error("EXIT")
        exit()

    time.sleep(1)

    os.system('cls')
    log.info("Finished analyzing images")
    print("Finished analyzing images!")

    return number_of_images

def index_images(config):
    """Indexes the analyzed images

    Args:
        config (object): configuration json object
    """
  
    os.system('cls')
    print("Indexing images...")
    log.info("Start indexing images")

    number_of_images = indexer.index(config)

    print("Finished indexing images!")
    log.info("Finished indexing images")
    time.sleep(1)

    return number_of_images

def download_final_images(config):
    """Downloads the final images data set

    Args:
        config (object): configuration json object
    """

    print("Starting downloader...")
    log.info("Downloading of final images started")
    time.sleep(1)

    # Create image range
    image_range = imageRange.get_range(
        mode="indexFile",
        config=config,
        size=0)

    # Create printing thread
    print_queue = status.printQueue()

    # Create threads
    image_directory = config['image']['directory']
    threads = threadsHelper.create(
        image_range, image_directory, config['image']['size'], config)

    # Initialize status
    total_number_of_images = threadsHelper.get_total(threads)
    pbTotal = status.init("Downloading images",
                          total_number_of_images, print_queue)

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

    log.info("Finished downloading images!")
    time.sleep(1)

def print_end_report(config, data):
    """Prints report

    Args:
        config (object): configuration json object
    """

    os.system('cls')

    report.print_report(config, data)

def clean_up(config):
    log.info("Cleaning up")

    try:
        shutil.rmtree(f"{config['tmpdirectory']}/images")
        shutil.rmtree(f"{config['tmpdirectory']}/index")
        shutil.rmtree(f"{config['tmpdirectory']}/xml")
    except:
        log.error("Somthing went wrong while cleaning up files. You may have to manualy remove the contents of the tmp directory.")
    
main()
