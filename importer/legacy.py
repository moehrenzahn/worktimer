import data
from datetime import datetime


class LegacyDaysFactory:
    def __init__(self, json):
        self.json = json
        self.days = []
        for day in self.json:
            date = datetime.strptime(day, '%Y-%m-%d').date()
            dayElement = json[day]
            self.processDay(dayElement, date)

    def create(self):
        return data.Days(self.days)

    def processDay(self, dayElement, date):
        if 'halbtags' in dayElement:
            goal = '4:00'
        elif 'zusatz' in dayElement:
            goal = '0:00'
        else:
            goal = '8:00'
        workArray = self.initWorkBlocks(dayElement)
        if date == datetime.now().date():
            day = data.Today(date, goal, workArray)
        else:
            day = data.Day(date, goal, workArray)
        self.days.append(day)

    def initWorkBlocks(self, dayElement):
        workArray = []
        if 'start' in dayElement and 'end' in dayElement:
            workArray.append(data.Work(dayElement['start'], dayElement['end']))
        elif 'start' in dayElement:
            workArray.append(data.Work(dayElement['start']))
        if len(workArray) == 0:
            raise ValueError('Day without work block found')
        return workArray
