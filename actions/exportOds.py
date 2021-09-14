from typing import OrderedDict
import config
import json
from data import Days
from output import notification
from math import floor

def export(days: Days, targetOds: str) -> bool:
    notification('Export Failed', 'Not implemented yet.')
    return False

    try:
        ods = __import__('pyexcel_ods')
    except:
        notification('Export Failed', 'Module pyexcel_ods is not installed.')
        return False

    newData = _collectNewDurationData(days)
    templateData = ods.get_data(targetOds)
    updatedTemplateData = _applyToTemplate(newData, templateData)
    ods.save_data(targetOds, updatedTemplateData)
    
    notification('Export Done', 'Find the updated file at %s' % targetOds)
    print('updatedTemplateData', updatedTemplateData)
    return True

def _collectNewDurationData(days: Days):
    newData = OrderedDict({})
    sortedDays = sorted(days.days, key=lambda x: x.date)
    for day in sortedDays:
        year = str(day.date.year)
        month = str(day.date.month)
        for work in day.work:
            category = work.category
            duration = floor(work.getDuration().total_seconds() / 60)
            if not year in newData:
                newData[year] = {}
            if not category in newData[year]:
                newData[year][category] = {}
            
            if month in newData[year][category]:
                duration += int(newData[year][category][month]);
            newData[year][category][month] = duration
    return newData

def _applyToTemplate(newData, template):
    for year in newData:
        for category in newData[year]:
            column = _findColumnIndexForCategory(template[year], category)
            if not column:
                notification('Export Failed', 'Could not find Column for category "%s"' % category)
                return False
            for month in newData[year][category]:
                print('month', month)
                line = _findLineIndexForMonth(template[year], month)
                if not line:
                    notification('Export Failed', 'Could not find Column for default category "div"')
                    return False

                while line >= len(template[year][column]):
                    template[year][column].append('')
                template[year][column][line] = newData[year][category][month]
    return template


def _findColumnIndexForCategory(sheetData, category):
    for idx, column in enumerate(sheetData):
        if category in column:
            return idx
    return False

def _findLineIndexForMonth(sheetData, month):
    for idx, column in enumerate(sheetData):
        if 'div' in column:
            return column.index('div') + int(month)
    return False