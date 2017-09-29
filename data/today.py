from day import Day
from datetime import datetime


class Today(Day):
    def __init__(self, day):
        Day.__init__(self, day)

        startDateTime = datetime.combine(self.date, self.start.time())

        self.currentWork = datetime.now() - startDateTime
        self.remainingWork = (self.goal + self.pause) - self.currentWork
        self.runningPause = self.runningPause(day)

    def runningPause(day):
        if "pause" in day:
            lastPause = day["pause"][-1]
            if "start" in lastPause:
                isPauseStart = 1
            if "end" in lastPause:
                isPauseEnd = 1
            if isPauseStart and not isPauseEnd:
                startTime = datetime.strptime(lastPause["start"], '%H:%M')
                runningPause = datetime.now() - startTime
                return runningPause
