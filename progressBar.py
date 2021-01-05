import sys

class progressBar:
    def __init__(self, line, total, prefix, suffix, lenght, printQueue):
        self.__line = line
        self.__iteration = 0
        self.__total = total
        self.__prefix = prefix
        self.__suffix = suffix
        self.__length = lenght
        self.__printQueue = printQueue
        self.__printProgressBar()

    def getProgressBar(self):
        return self

    def update(self, iteration):
        self.__iteration = iteration
        self.__printProgressBar()

    def increment(self):
        self.__iteration = self.__iteration + 1
        self.__printProgressBar()

    def __moveLine(self, line):
        sys.stdout.write("\033[%d;%dH" % (line, 0))
        sys.stdout.flush()

    def __printProgressBar(self):

        if(self.__total < 1):
            percent = 100.0
            filledLength = int(self.__length * 1)
            bar = '█' * filledLength
        else:
            percent = ("{0:.1f}").format(100 * (self.__iteration / float(self.__total)))
            filledLength = int(self.__length * self.__iteration // self.__total)
            bar = '█' * filledLength + '-' * (self.__length - filledLength)

        if(self.__printQueue == "NOQUEUE"):
            self.__moveLine(self.__line)
            print(
                f'\r{self.__prefix} |{bar}| {self.__iteration}/{self.__total} | {percent}% {self.__suffix}')
        else:
            self.__printQueue.enqueue(
                f'\r{self.__prefix} |{bar}| {self.__iteration}/{self.__total} | {percent}% {self.__suffix}', self.__line)
