import sys

class progressBar():
    def __init__(self, line, total, prefix, suffix, lenght):
        self.__line = line
        self.__iteration = 0
        self.__total = total
        self.__prefix = prefix
        self.__suffix = suffix
        self.__length = lenght
        self.__printProgressBar()

    def update(self, iteration):
        self.__iteration = iteration
        self.__printProgressBar()

    def __printProgressBar(self):
        move(self.__line, 0)

        percent = ("{0:.1f}").format(100 * (self.__iteration / float(self.__total)))
        filledLength = int(self.__length * self.__iteration // self.__total)
        bar = '█' * filledLength + '-' * (self.__length - filledLength)

        print(f'\r{self.__prefix} |{bar}| {self.__iteration}/{self.__total} | {percent}% {self.__suffix}', end="\r")

def move (y, x):
    sys.stdout.write("\033[%d;%dH" % (y, x))
    sys.stdout.flush()
