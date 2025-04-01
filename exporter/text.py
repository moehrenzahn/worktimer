from datetime import timedelta
import string
import subprocess
import config
from data import formatter
from data.days import Days


def export(days: Days, targetPath: string):
    tab = '     '
    separator = ' - '
    NL = '\n'
    exportString = ''

    sortedDays = sorted(days.days, key=lambda x: x.date)

    currentMonth: string = sortedDays[0].date.strftime("%m")
    currentMonthWorked: timedelta = timedelta(minutes=0)
    currentMonthOvertime: timedelta = timedelta(minutes=0)
    currentMonthCategories: dict[str, timedelta] = {}
    currentYear: string = sortedDays[0].date.strftime("%Y")
    currentYearWorked: timedelta = timedelta(minutes=0)
    currentYearOvertime: timedelta = timedelta(minutes=0)
    currentYearCategories: dict[str, timedelta] = {}
    currentTotalWorked: timedelta = timedelta(minutes=0)
    currentTotalOvertime: timedelta = timedelta(minutes=config.overtime_offset_in_minutes())
    currentTotalCategories: dict[str, timedelta] = {}

    for day in sortedDays:
        if day.date.strftime("%m") != currentMonth:
            exportString += NL
            exportString += "Month " + currentYear + "-" + currentMonth + NL
            exportString += "-------------" + NL
            exportString += "Month Worked: " + formatter.format_delta(currentMonthWorked) + NL
            if currentMonthWorked != currentMonthOvertime:
                exportString += "Month Overtime: " + formatter.format_delta(currentMonthOvertime) + NL
            exportString += "Total Worked: " + formatter.format_delta(currentTotalWorked) + NL
            if currentTotalWorked != currentTotalOvertime:
                exportString += "Total Overtime: " + formatter.format_delta(currentTotalOvertime) + NL
            exportString += formatter.format_category_total_and_percentages(currentMonthWorked, currentMonthCategories)
            currentMonthWorked = timedelta(minutes=0)
            currentMonthCategories.clear()
            currentMonthOvertime = timedelta(minutes=0)
        if day.date.strftime("%Y") != currentYear:
            exportString += NL
            exportString += "Year " + currentYear + NL
            exportString += "=========" + NL
            exportString += "Year Worked : " + formatter.format_delta(currentYearWorked) + NL
            if currentYearWorked != currentYearOvertime:
                exportString += "Year Overtime : " + formatter.format_delta(currentYearOvertime) + NL
            exportString += formatter.format_category_total_and_percentages(currentYearWorked, currentYearCategories)
            exportString += NL
            currentYearCategories.clear()
            currentYearWorked = timedelta(minutes=0)
            currentYearOvertime = timedelta(minutes=0)

        currentMonthWorked += day.getCurrentWork()
        for work in day.work:
            existingWorked = currentMonthCategories.get(
                work.category,
                timedelta(minutes=0) # default
            )
            currentMonthCategories.update({work.category: existingWorked + work.getDuration()})

            existingWorked = currentYearCategories.get(
                work.category,
                timedelta(minutes=0) # default
            )
            currentYearCategories.update({work.category: existingWorked + work.getDuration()})

            existingWorked = currentTotalCategories.get(
                work.category,
                timedelta(minutes=0) # default
            )
            currentTotalCategories.update({work.category: existingWorked + work.getDuration()})
        currentMonthOvertime += day.getOvertime()
        currentYearWorked += day.getCurrentWork()
        currentYearOvertime += day.getOvertime()
        currentTotalWorked += day.getCurrentWork()
        currentTotalOvertime += day.getOvertime()

        currentMonth = day.date.strftime("%m")
        currentYear = day.date.strftime("%Y")

    exportString += NL + "Month " + currentYear + "-" + currentMonth + " (ONGOING)" + NL
    exportString += "-----------------------" + NL
    exportString += "Month Worked: " + formatter.format_delta(currentMonthWorked) + NL
    if currentMonthWorked != currentMonthOvertime:
        exportString += "Month Overtime : " + formatter.format_delta(currentMonthOvertime) + NL
    exportString += formatter.format_category_total_and_percentages(currentMonthWorked, currentMonthCategories)

    exportString += NL

    exportString += "Year " + currentYear + " (ONGOING)" + NL
    exportString += "==================" + NL
    exportString += "Year Worked : " + formatter.format_delta(currentYearWorked) + NL
    if currentYearOvertime != currentYearWorked:
        exportString += "Year Overtime : " + formatter.format_delta(currentYearOvertime) + NL
    exportString += formatter.format_category_total_and_percentages(currentYearWorked, currentYearCategories)

    exportString += NL + NL
    exportString += "Totals (ONGOING)" + NL
    exportString += "==================" + NL
    exportString += "Total Worked: " + formatter.format_delta(currentTotalWorked) + NL
    if currentTotalOvertime != currentTotalWorked:
        exportString += "Total Overtime: " + formatter.format_delta(currentTotalOvertime) + NL
    exportString += formatter.format_category_total_and_percentages(currentTotalWorked, currentTotalCategories)

    exportString += NL + NL + "===============" + NL + NL

    for day in sortedDays:
        exportString += day.date.strftime("%Y-%m-%d") + tab
        for work in day.work:
            exportString += formatter.format_time(work.start)
            if hasattr(work, 'stop'):
                exportString += separator + formatter.format_time(work.stop)
            exportString += NL + tab + tab + tab
        exportString += NL

    __save(exportString, targetPath)
    subprocess.call(["open", targetPath])


def __save(s, path):
    # make sure file exists
    open(path, 'a')
    file = open(path, 'w')
    file.write(s)
    file.close()
