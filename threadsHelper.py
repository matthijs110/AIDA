import downloader
import progressBar
import status

def create(ranges, image_directory, size, config):
    threadid = 0
    threads = list()

    for r in ranges:
        threadname = "Thread-" + str(threadid)
        threadid = threadid + 1
        thread = downloader.downloadThread(threadname,  r, image_directory, size, config)
        threads.append(thread)
    
    return threads

def get_total(threads):
    total = 0

    for thread in threads:
        total += thread.getNumberOfImages()

    return total

def add_progress_bar(threads):
    for thread in threads:

        prefix = f"{thread.name} progress: "

        if(len(thread.name) == 9):
            prefix = prefix.strip()

        pb = progressBar.progressBar(line=status.bottomLine, total=thread.getNumberOfImages(), prefix=prefix, suffix="Complete", lenght=50)
        thread.setProgressBar(pb)
        status.bottomLine = status.bottomLine + 1

def add_total_progress_bar(threads, pb):
    for thread in threads:
        thread.setTotalProgressBar(pb)

def start(threads):
    for thread in threads:
        thread.start()
