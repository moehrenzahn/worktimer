import subprocess
import config
from data import formatter


def export(days):
    tab = '     '
    separator = ' - '
    newLine = '\n'
    exportString = ''

    for day in days.days:
        exportString += day.date.strftime("%Y-%m-%d") + tab
        for work in day.work:
            exportString += formatter.format_time(work.start)
            if hasattr(work, 'stop'):
                exportString += separator + formatter.format_time(work.stop)
            exportString += newLine + tab + tab + tab
        exportString += newLine
    __save(exportString)
    subprocess.call(["open", config.export_path])


def __save(s):
    file = open(config.export_path, 'w')
    file.write(s)
    file.close()
