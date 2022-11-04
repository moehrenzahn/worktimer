import data
from datetime import datetime
from datetime import timedelta


class DaysFactory:
    def __init__(self, daysData):
        self.daysData = daysData
        self.days = []
        for day in self.daysData:
            dayElement = daysData[day]
            if day != dayElement['date']:
                raise ValueError('Date mismatch at %s' % day)
            newDay = self.processDay(dayElement)
            self.days.append(newDay)

    def create(self):
        return data.Days(self.days)

    def processDay(self, dayElement):
        date = datetime.strptime(dayElement['date'], '%Y-%m-%d').date()
        goal = datetime.strptime(dayElement['goal'], "%H:%M")
        # goal describes not a time, but a timedelta
        goal = timedelta(hours=goal.hour, minutes=goal.minute)
        if 'comment' in dayElement:
            comment = dayElement['comment']
        else:
            comment = None
        work = self.initWorkBlocks(dayElement)
        if date == datetime.now().date():
            if 'paused' in dayElement:
                day = data.Today(date, goal, comment, work, dayElement['paused'])
            else:
                day = data.Today(date, goal, comment, work)
        else:
            day = data.Day(date, goal, comment, work)
        return day

    def initWorkBlocks(self, dayElement):
        workBlocks = []
        if 'work' not in dayElement:
            raise ValueError('Day without work block found')
        for item in dayElement['work']:
            start = datetime.strptime(item['start'], "%H:%M").time()
            category = item['category'] if ('category' in item) else ''
            if 'stop' in item:
                stop = datetime.strptime(item['stop'], "%H:%M").time()
                workBlocks.append(data.block.Work(start, category, stop))
            else:
                workBlocks.append(data.block.Work(start, category))
        return workBlocks
