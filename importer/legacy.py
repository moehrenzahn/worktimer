import data
from datetime import datetime
from datetime import timedelta


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
            goal = datetime.strptime('04:00', "%H:%M")
        elif 'zusatz' in dayElement:
            goal = datetime.strptime('00:00', "%H:%M")
        else:
            goal = datetime.strptime('08:00', "%H:%M")
        goal = timedelta(hours=goal.hour, minutes=goal.minute)
        workArray = self.initWorkBlocks(dayElement)
        if date == datetime.now().date():
            day = data.Today(date, goal, workArray)
        else:
            day = data.Day(date, goal, workArray)
        self.days.append(day)

    def initWorkBlocks(self, dayElement):
        workArray = []
        if 'start' in dayElement and 'end' in dayElement:
            start = datetime.strptime(dayElement['start'], "%H:%M").time()
            end = datetime.strptime(dayElement['end'], "%H:%M").time()
            workArray.append(data.block.Work(start, end))
        elif 'start' in dayElement:
            start = datetime.strptime(dayElement['start'], "%H:%M").time()
            workArray.append(data.block.Work(start))
        if len(workArray) == 0:
            raise ValueError('Day without work block found')
        return workArray
