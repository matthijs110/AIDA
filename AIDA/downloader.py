import threading
import progressBar
import status
import os
import subprocess
import logging as log
from schemas import xml_template

class downloadThread (threading.Thread):
    def __init__(self, name, image_range, image_directory, size, config):
        threading.Thread.__init__(self)
        self.name = name
        self.image_range = image_range
        self.image_directory = image_directory
        self.size = size
        self.config = config
        self.progressBar = progressBar.progressBar
        self.totalProgessBar = progressBar.progressBar
        self.running = True

    def setProgressBar(self, pb):
        self.progressBar = pb
    
    def setTotalProgressBar(self, pb):
        self.totalProgessBar = pb

    def getNumberOfImages(self):
        return len(self.image_range)
    
    def updateProgressBar(self, iteration):
        self.progressBar.update(iteration)
    
    def stop(self):
        self.running = False
        log.info(f"Stopping {self.name}.")

    def run(self):
        self.download_images(self.image_range, self.image_directory, self.size, self.config)

    def download_images(self, image_range, image_directory, size, config):

        numOfDownloadedImages = 0

        log.info(f"Starting download {self.name}")

        for west_south in image_range:

            if(not self.running):
                return
            
            # Split west and south
            west = float(west_south.split(",")[0])
            south = float(west_south.split(",")[1])

            # Create Filenames
            filename = f"{image_directory}/{west}_{south}_{size}.gdal.{config['service']['format']}"
            tmpfilename = f"{config['tmpdirectory']}/xml/{west}-{south}.xml"

            # If file exists, skip.
            if(os.path.isfile(filename)):
                numOfDownloadedImages = numOfDownloadedImages + 1
                self.totalProgessBar.increment()
                self.updateProgressBar(numOfDownloadedImages)
                log.info(f"Skipping download of ({filename}). File already exists.")
                continue

            # Set XML Parameters
            xml_params = {
                'west': west,
                'south': south,
                'east': west + size,
                'north': south + size,
                'resolution': config['image']['resolution'],
                'timeout': config['timeout'],
                'projection': config['image']['projection'],
                'transparent': config['service']['transparent'],
                'bandscount': config['bandscount']
            }
            xml_params.update(config['service'])

            # Create temp XML file
            fileCreatedSuccesfully = False

            while fileCreatedSuccesfully == False:
                try:
                    file = open(tmpfilename, "w")
                    file.write(xml_template % xml_params)
                    file.close()
                    fileCreatedSuccesfully = True
                    log.info(f"Created file: {tmpfilename} succesfully.")
                except:
                    log.warning(f"Could not create file: {tmpfilename}. Retrying.")
                    pass
            
            numberOfTriesDownloadingFile = 0
            fileDownloadedSuccesfully = False

            # Start downloading file
            log.info(f"Starting to download image: {filename}")
            
            while numberOfTriesDownloadingFile < 10 and fileDownloadedSuccesfully == False:
                try:
                    numberOfTriesDownloadingFile = numberOfTriesDownloadingFile + 1
                    args = ['gdal_translate', '-of', config['service']
                            ['format'], tmpfilename, filename]

                    # Running gdal_translate in subprocess
                    f = open("gdal.error.log", "a")
                    subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=f)

                    # Cleaing up
                    os.remove(filename + '.aux.xml')
                    fileDownloadedSuccesfully = True
                    numOfDownloadedImages = numOfDownloadedImages + 1
                    log.info(f"Downloaded image: {filename} succesfully.")
                except:
                    log.warning(f"Could not download image: {filename}. Retrying {10 - numberOfTriesDownloadingFile} more time(s).")
            
            try:                        
                os.remove(tmpfilename)
                log.info(f"Removed file: {tmpfilename}.")
            except:
                log.warning(f"Could not remove file: {tmpfilename}.")

            self.totalProgessBar.increment()
            self.updateProgressBar(numOfDownloadedImages)