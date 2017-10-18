from datetime import datetime, date
from datetime import timedelta
import data


class Day():
    def __init__(self, date, goal, workArray):
        self.date = date
        goal = datetime.strptime(goal, "%H:%M")
        self.goal = timedelta(hours=goal.hour, minutes=goal.minute)
        self.workArray = workArray

    def calculatePauses(self):
        pauses = []
        for (i, workBlock) in enumerate(self.workArray):
            if i > 0:
                start = self.workArray[i - 1].end
                end = self.workArray[i].start
                pauses.append(data.Pause(start, end))
        return pauses

    def isRunning(self):
        for work in self.workArray:
            if work.isRunning():
                return 1
        return 0

    def getOvertime(self):
        overtime = timedelta(0)
        for work in self.workArray:
            if hasattr(work, 'end'):
                delta = datetime.combine(
                    date.min, work.end
                ) - datetime.combine(
                    date.min, work.start
                )
                overtime += delta
        overtime = overtime - self.goal
        return overtime

    def getStartTime(self):
        return datetime.combine(self.date, self.work[0].start)

    def getEndTime(self):
        return self.date + self.getRemainingWork()

    def getCurrentWork(self):
        time = timedelta(0)
        for work in self.workArray:
            time += work.getDuration()
        return time

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
