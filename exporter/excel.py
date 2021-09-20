from typing import OrderedDict
from data import Days
from output import notification
from math import floor

def export(days: Days, templateFile: str, targetFile: str) -> bool:
    try:
        pyxl = __import__('openpyxl')
    except:
        raise ValueError('Module openpyxl is not installed.')

    newData = _collectNewDurationData(days)
    spreadsheet = pyxl.load_workbook(templateFile)
    updatedSpreadsheet = _applyToSpreadsheet(newData, spreadsheet)
    if not updatedSpreadsheet:
        raise ValueError('Could not apply data to spreadsheet template.')
    updatedSpreadsheet.save(targetFile)

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

def _createNewYear(year, spreadsheet):
    newSheet = spreadsheet.copy_worksheet(spreadsheet.active)
    newSheet.title = year

def _applyToSpreadsheet(newData, spreadsheet):
    for year in newData:
        if not year in spreadsheet:
            _createNewYear(year, spreadsheet)
    for year in newData:
        for category in newData[year]:
            for month in newData[year][category]:
                (row, column) = _findRowAndColumnForCategoryAndMonth(spreadsheet[year], category, month)
                if not column or not row:
                    raise ValueError('Could not find column for category "%s" in Excel file' % category)
                    return False
                # Write value to cell
                spreadsheet[year].cell(row=row,column=column).value = newData[year][category][month]
    return spreadsheet


def _findRowAndColumnForCategoryAndMonth(spreadsheet, category, month):
    for row in spreadsheet.iter_rows():
        for cell in row:
            if cell.value == category:
                return (cell.row, cell.column + int(month))
    return (False, False)