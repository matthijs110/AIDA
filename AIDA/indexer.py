import pathlib
import re

def index(config):

    data_dir = pathlib.Path(f"{config['directory']['tmp']}/images/filtered")
    images = list(data_dir.glob('*.jpeg'))

    tempsize = config['image']['tempsize']
    size = config['image']['size']
    outputFile = f"{config['directory']['tmp']}/index/index.csv"

    number_of_images = 0

    f = open(outputFile, "w")

    for image in images:
        west = int((re.findall(r"(\d{1,7}_)", str(image))[0]).replace('_', ''))
        south = int((re.findall(r"(\d{1,7}_)", str(image))[1]).replace('_', ''))
        east = int(west) + tempsize
        north = int(south) + tempsize

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