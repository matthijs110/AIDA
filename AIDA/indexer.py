import pathlib
import re

def index(config):

    data_dir = pathlib.Path(f"{config['tmpdirectory']}/images/filtered")
    images = list(data_dir.glob('*.jpeg'))

    tempsize = config['image']['tempsize']
    size = config['image']['size']
    outputFile = f"{config['tmpdirectory']}/index/index.csv"

    number_of_images = 0

    f = open(outputFile, "w")

    for image in images:
        west = float(re.findall(r"(\d{1,6}\.0)", str(image))[0])
        south = float(re.findall(r"(\d{1,6}\.0)", str(image))[1])
        east = float(west) + tempsize
        north = float(south) + tempsize

        west_range = list(arange(west, east, size))
        south_range = list(arange(south, north, size))

        for west in west_range:
            for south in south_range:
                    f.write(f"{west},{south}\n")
                    number_of_images = number_of_images + 1

    f.close()
    return number_of_images

def arange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step