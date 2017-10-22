from datetime import datetime, date
from datetime import timedelta
import data


class Day():
    def __init__(self, date, goal, work):
        """
        date: date
        goal: timedelta
        work: [Work]
        """
        self.date = date
        self.goal = goal
        self.work = work

    def calculatePauses(self):
        pauses = []
        for (i, workBlock) in enumerate(self.work):
            if i > 0:
                start = self.work[i - 1].end
                end = self.work[i].start
                pauses.append(data.block.Pause(start, end))
        return pauses

    def isRunning(self):
        for work in self.work:
            if work.isRunning():
                return 1
        return 0

    # estimation
    def isPause(self):
        pauses = self.calculatePauses()
        if pauses:
            lastPauseLenght = pauses[-1].getDuration()
            remaining = self.getRemainingWork()
            if lastPauseLenght < timedelta(hours=1) and remaining > timedelta(hours=1):
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
        overtime = overtime - self.goal
        return overtime

    def getStartTime(self):
        return self.__getFirstWorkStart()

    def getEndTime(self):
        startDate = datetime.combine(
            datetime.now(),
            self.getStartTime()
        )
        endTime = startDate + self.goal + self.getPausetime()
        return endTime

    def __getFirstWorkStart(self):
        startTimes = []
        for work in self.work:
            startTimes.append(work.start)
        startTimes.sort()
        return startTimes[0]

    def getLastWork(self):
        startTimes = []
        startTimes = []
        for work in self.work:
            startTimes.append(work.start)
        startTimes.sort()
        for work in self.work:
            if startTimes[-1] == work.start:
                return work
        raise TypeError('Last work block not found')

    def getCurrentWork(self):
        time = timedelta(0)
        for work in self.work:
            time += work.getDuration()
        return time

    def getRemainingWork(self):
        pauseTime = self.getPausetime()
        # calculate for 30 minutes pause if none is taken yet
        if pauseTime == timedelta(0):
            pauseTime = timedelta(minutes=30)
        return (self.goal + pauseTime) - self.getCurrentWork()

    def getPausetime(self):
        time = timedelta(0)
        for pause in self.calculatePauses():
            time += pause.getDuration()
        return time
