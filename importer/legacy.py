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

        if 'pause' in dayElement:
            work = self.initWorkBlocksWithPauses(dayElement)
        else:
            work = self.initWorkBlocks(dayElement)
        if len(work) == 0:
            raise ValueError('Day without work block found')

        if date == datetime.now().date():
            day = data.Today(date, goal, work)
        else:
            day = data.Day(date, goal, work)
        self.days.append(day)

    def initWorkBlocks(self, dayElement):
        if 'end' in dayElement:
            start = datetime.strptime(dayElement['start'], "%H:%M").time()
            stop = datetime.strptime(dayElement['end'], "%H:%M").time()
            work = [data.block.Work(start, stop)]
        else:
            start = datetime.strptime(dayElement['start'], "%H:%M").time()
            work = [data.block.Work(start)]
        return work

    def initWorkBlocksWithPauses(self, dayElement):
        work = []
        start = datetime.strptime(dayElement['start'], "%H:%M").time()
        for pause in dayElement['pause']:
            stop = datetime.strptime(pause['start'], "%H:%M").time()
            work.append(data.block.Work(start, stop))
            start = datetime.strptime(pause['end'], "%H:%M").time()
        if 'end' in dayElement:
            stop = datetime.strptime(dayElement['end'], "%H:%M").time()
            work.append(data.block.Work(start, stop))
        else:
            work.append(data.block.Work(start))
        return work
