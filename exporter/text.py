import subprocess
import config
from data import formatter


def export(days, targetPath):
    tab = '     '
    separator = ' - '
    newLine = '\n'
    exportString = ''

    sortedDays = sorted(days.days, key=lambda x: x.date)

    for day in sortedDays:
        exportString += day.date.strftime("%Y-%m-%d") + tab
        for work in day.work:
            exportString += formatter.format_time(work.start)
            if hasattr(work, 'stop'):
                exportString += separator + formatter.format_time(work.stop)
            exportString += newLine + tab + tab + tab
        exportString += newLine
    __save(exportString, targetPath)
    subprocess.call(["open", targetPath])


def __save(s, path):
    # make sure file exists
    open(path, 'a')
    file = open(path, 'w')
    file.write(s)
    file.close()
