from datetime import datetime, date
from datetime import timedelta
import data


class Day():
    def __init__(self, date, goal, workArray):
        """
        date: date
        goal: timedelta
        workArray: [Work]
        """
        self.date = date
        self.goal = goal
        self.workArray = workArray

    def calculatePauses(self):
        pauses = []
        for (i, workBlock) in enumerate(self.workArray):
            if i > 0:
                start = self.workArray[i - 1].end
                end = self.workArray[i].start
                pauses.append(data.block.Pause(start, end))
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
        return self.getFirstWorkStart()

    def getEndTime(self):
        return self.date + self.getRemainingWork()

    def getFirstWorkStart(self):
        startTimes = []
        for work in self.workArray:
            startTimes.append(work.start)
        startTimes.sort()
        return startTimes[0]

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
