import time
import sys
import os
from progressBar import progressBar
import shutil
import subprocess
import logging as log
import threading
import sys

bottomLine = 18

def init(task, total, printQueue):
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
    print(f"\nCurrent Task: {task}")
    print("==============================================================================================") 
    pbTotal = progressBar(line=13, total=total, prefix="Overall progress:  ", suffix="Complete", lenght=50, printQueue=printQueue)
    move(15,0)
    print("==============================================================================================")
    print("Progress per Thread:")

    return pbTotal

class printQueue(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "PrintQueueThread"
        self.__queue = list()
        self.__running = True
        log.info("Started printQueueThread")

    def enqueue(self, msg, line):
        self.__queue.append((msg, line))
        pass

    def dequeue(self):
        if(len(self.__queue) > 0):
            return self.__queue.pop(0)
    
    def __print(self):
        if(len(self.__queue) > 0):
            t = self.dequeue()
            msg = t[0]
            y = t[1]
            self.move(y)
            print(msg)

    def stop(self):
        self.move(bottomLine + 1)
        self.__running = False  
        log.info("Stopping printQueueThread.")

    def move(self, line):
        sys.stdout.write("\033[%d;%dH" % (line, 0))
        sys.stdout.flush()

    def run(self):
        while len(self.__queue) > 0 or self.__running:
            self.__print()
        self.stop()

def move (y, x):
    sys.stdout.write("\033[%d;%dH" % (y, x))
    sys.stdout.flush()