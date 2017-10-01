from day import Day
from datetime import datetime
from datetime import timedelta

class Today(Day):
    def __init__(self, day):
        Day.__init__(self, day)

        startDateTime = datetime.combine(self.date, self.start)

        self.currentWork = datetime.now() - startDateTime
        if self.pauseTime == timedelta(0):
            # calculate for 30 minutes pause if none is taken yet
            self.remainingWork = (self.goal + timedelta(minutes=30)) - self.currentWork
        else:
            self.remainingWork = (self.goal + self.pauseTime) - self.currentWork