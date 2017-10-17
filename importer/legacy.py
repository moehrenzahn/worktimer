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

    def processDay(self, dayElement, date):
        if 'halbtags' in dayElement:
            goal = '4:00'
        elif 'zusatz' in dayElement:
            goal = '0:00'
        else:
            goal = '8:00'
        work = self.initWorkBlocks(dayElement)
        if date == datetime.now().date():
            day = data.Today(date, goal, work)
        else:
            day = data.Day(date, goal, work)
        self.days.append(day)

    def initWorkBlocks(self, dayElement):
        work = []
        if 'start' in dayElement and 'end' in dayElement:
            work.append(data.Work(dayElement['start'], dayElement['end']))
        elif 'start' in dayElement:
            work.append(data.Work(dayElement['start']))
        if len(work) == 0:
            print('Error: No work block in date!')
            exit(2)
        return work
