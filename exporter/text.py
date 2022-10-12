from datetime import timedelta
import string
import subprocess
import config
from data import formatter
from data.days import Days


def export(days: Days, targetPath: string):
    tab = '     '
    separator = ' - '
    newLine = '\n'
    exportString = ''

    sortedDays = sorted(days.days, key=lambda x: x.date)

    currentMonth: string = sortedDays[0].date.strftime("%m")
    currentMonthWorked: timedelta = timedelta(minutes=0)
    currentMonthOvertime: timedelta = timedelta(minutes=0)
    currentYear: string = sortedDays[0].date.strftime("%Y")
    currentYearWorked: timedelta = timedelta(minutes=0)
    currentYearOvertime: timedelta = timedelta(minutes=0)
    currentTotalWorked: timedelta = timedelta(minutes=0)
    currentTotalOvertime: timedelta = timedelta(minutes=0)

    for day in sortedDays:
        if day.date.strftime("%m") != currentMonth:
            exportString += newLine + currentYear + "-" + currentMonth + newLine
            exportString += "Month Worked: " + formatter.format_delta(currentMonthWorked) + newLine
            exportString += "Month Overtime: " + formatter.format_delta(currentMonthOvertime) + newLine
            exportString += "Total Worked: " + formatter.format_delta(currentTotalWorked) + newLine
            exportString += "Total Overtime: " + formatter.format_delta(currentTotalOvertime) + newLine
            currentMonthWorked = timedelta(minutes=0)
            currentMonthOvertime = timedelta(minutes=0)
        if day.date.strftime("%Y") != currentYear:
            exportString += newLine + currentYear + " (Year summary)" + newLine
            exportString += "Year Worked : " + formatter.format_delta(currentYearWorked) + newLine
            exportString += "Year Overtime : " + formatter.format_delta(currentYearOvertime) + newLine
            currentYearWorked = timedelta(minutes=0)
            currentYearOvertime = timedelta(minutes=0)

        currentMonthWorked += day.getCurrentWork()
        currentMonthOvertime += day.getOvertime()
        currentYearWorked += day.getCurrentWork()
        currentYearOvertime += day.getOvertime()
        currentTotalWorked += day.getCurrentWork()
        currentTotalOvertime += day.getOvertime()

        currentMonth = day.date.strftime("%m")
        currentYear = day.date.strftime("%Y")

    exportString += newLine + currentYear + "-" + currentMonth + " (ONGOING)" + newLine
    exportString += "Month Worked: " + formatter.format_delta(currentMonthWorked) + newLine
    exportString += "Month Overtime : " + formatter.format_delta(currentMonthOvertime) + newLine
    exportString += "Total Worked: " + formatter.format_delta(currentTotalWorked) + newLine
    exportString += "Total Overtime: " + formatter.format_delta(currentTotalOvertime) + newLine

    exportString += newLine + newLine + newLine

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
