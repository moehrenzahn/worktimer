import data
from datetime import datetime


class DaysFactory:
    def __init__(self, json):
        self.json = json
        self.days = []
        for dayElement in self.json:
            day = self.processDay(dayElement)
            self.days.append(day)

    def create(self):
        return data.Days(self.days)

    def processDay(self, dayElement):
        date = datetime.strptime(dayElement['date'], '%Y-%m-%d').date()
        goal = dayElement['goal']
        work = self.initWorkBlocks(dayElement)
        if date == datetime.now().date():
            day = data.Today(date, goal, work)
        else:
            day = data.Day(date, goal, work)
        return day

    def initWorkBlocks(self, dayElement):
        workBlocks = []
        if 'work' not in dayElement:
            raise ValueError('Day without work block found')
        for item in dayElement['work']:
            if 'end' in item:
                workBlocks.append(data.Work(item['start'], item['end']))
            else:
                workBlocks.append(data.Work(item['start']))
        return workBlocks