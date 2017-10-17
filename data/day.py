from datetime import datetime, date
from datetime import timedelta
import data


class Day():
    def __init__(self, date, goal, work):
        self.date = date
        self.goal = goal
        self.work = work

    def calculatePauses(self):
        pauses = []
        for (i, workBlock) in self.work:
            if i > 0:
                start = self.work[i - 1].end
                end = self.work[i].start
                pauses.append(data.Pause(start, end))
        return pauses

    def isRunning(self):
        for work in self.work:
            if work.isRunning:
                return 0
        return 1

    def isPause(self):
        for pause in self.calculatePauses():
            if pause.isRunning:
                return 1
        return 0

    def getOvertime(self):
        overtime = timedelta(0)
        for work in self.work:
            if hasattr(work, 'end'):
                delta = datetime.combine(
                    date.min, work.end
                ) - datetime.combine(
                    date.min, work.start
                )
                overtime += delta
        overtime = overtime - self.getPausetime() - self.goal
        return overtime

    def getStartTime(self):
        return datetime.combine(self.date, self.work[0].start)

    def getEndTime(self):
        return self.date + self.getRemainingWork()

    def getCurrentWork(self):
        time = timedelta(0)
        for work in self.work:
            time += work.getDuration()
        return time - self.getPausetime()

    def getRemainingWork(self):
        pauseTime = self.getPausetime()
        if pauseTime == timedelta(0):
            # calculate for 30 minutes pause if none is taken yet
            return (self.goal + timedelta(minutes=30)) - self.getCurrentWork()
        else:
            return (self.goal + pauseTime) - self.getCurrentWork()

    def getPausetime(self):
        time = timedelta(0)
        for pause in self.calculatePauses():
            time += pause.getDuration()
        return time
