import time
import sys
import os
from progressBar import progressBar, move
import shutil

def updateStatus():
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

    print("==============================================================================================") #94 - 27

    pb1 = progressBar(line=13, total=100, prefix="Overall progress:  ", suffix="Complete", lenght=50)

    move(15,0)

    print("==============================================================================================")

    print("Progress per Thread:")

    pb1 = progressBar(line=18, total=100, prefix="Thread 1 progress: ", suffix="Complete", lenght=50)
    pb1 = progressBar(line=19, total=100, prefix="Thread 2 progress: ", suffix="Complete", lenght=50)
    pb1 = progressBar(line=20, total=100, prefix="Thread 2 progress: ", suffix="Complete", lenght=50)
    pb1 = progressBar(line=21, total=100, prefix="Thread 2 progress: ", suffix="Complete", lenght=50)
    pb1 = progressBar(line=22, total=100, prefix="Thread 2 progress: ", suffix="Complete", lenght=50)





