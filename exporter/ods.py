from typing import OrderedDict
import config
import json
from data import Days
from output import notification
from math import floor

def export(days: Days, targetOds: str) -> bool:
    raise ValueError('Not implemented yet.')

    try:
        ods = __import__('pyexcel_ods')
    except:
        raise ValueError('Module pyexcel_ods is not installed.')

    newData = _collectNewDurationData(days)
    templateData = ods.get_data(targetOds)
    updatedTemplateData = _applyToTemplate(newData, templateData)
    ods.save_data(targetOds, updatedTemplateData)
    
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
                raise ValueError('Could not find Column for category "%s"' % category)
            for month in newData[year][category]:
                print('month', month)
                line = _findLineIndexForMonth(template[year], month)
                if not line:
                    raise ValueError('Could not find Column for default category')

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