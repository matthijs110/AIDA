import time
import sys
import os
from progressBar import progressBar, move
import shutil
import subprocess
import logging as log

bottomLine = 18
iteration = 0

def init(total):
    os.system('cls')

    banner = """
                                  ░█████╗░██╗██████╗░░█████╗░
                                  ██╔══██╗██║██╔══██╗██╔══██╗
                                  ███████║██║██║░░██║███████║
                                  ██╔══██║██║██║░░██║██╔══██║
                                  ██║░░██║██║██████╔╝██║░░██║
                                  ╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝
                             Aerial Imagery Downloader and Analyzer"""

    print(banner)
    print("\nCurrent Task: Downloading Images")
    print("==============================================================================================") 

    pbTotal = progressBar(line=13, total=total, prefix="Overall progress:  ", suffix="Complete", lenght=50)

    move(15,0)

    print("==============================================================================================")

    print("Progress per Thread:")

    return pbTotal