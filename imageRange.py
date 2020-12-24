import numpy

def get_range(mode, config, size):

    west_south_ranges = list()

    if(mode == "bbox"):
        west_range = list(arange(config['bbox']['west'], config['bbox']['east'], size))
        south_range = list(arange(config['bbox']['south'], config['bbox']['north'], size))
        south_ranges = numpy.array_split(south_range, config['threads'])

        for south_range_part in south_ranges:
            west_south_range = list()
            for west in west_range:
                for south in south_range_part:
                    west_south_range.append(str(west)+","+str(south))
            west_south_ranges.append(west_south_range)

    elif(mode == "indexFile"):
        cords_file = open(f"{config['tmpdirectory']}/index/index.csv", 'r')
        west_south_range = cords_file.readlines()
        west_south_ranges = numpy.array_split(west_south_range, config['threads'])

    return west_south_ranges

def arange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step
