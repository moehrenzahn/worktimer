from day import Day
from datetime import datetime


class Today(Day):
    def __init__(self, day, dateString):
        Day.__init__(self, day, dateString)

        startDateTime = datetime.combine(self.date, self.start)

        self.currentWork = datetime.now() - startDateTime
        self.remainingWork = (self.goal + self.pauseTime) - self.currentWork
