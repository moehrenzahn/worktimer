from datetime import datetime, date, timedelta
from typing import List, Optional
import data
from data.block.work import Work

class Day():
    def __init__(self, date: date, goal: timedelta, comment: Optional[str], work: List[Work]):
        self.date = date
        self.goal = goal
        self.comment = comment
        self.work = work

    def calculatePauses(self):
        pauses = []
        for (i, workBlock) in enumerate(self.work):
            if i > 0:
                start = self.work[i - 1].stop
                stop = self.work[i].start
                pauses.append(data.block.Pause(start, stop))
        lastWork = self.getLastWork()
        if hasattr(lastWork, 'stop'):
            pauses.append(data.block.Pause(lastWork.stop))
        return pauses

    def isRunning(self) -> bool:
        for work in self.work:
            if work.isRunning():
                return 1
        return 0

    # estimation
    def isPause(self) -> bool:
        pauses = self.calculatePauses()
        if pauses:
            lastPauseLenght = pauses[-1].getDuration()
            remaining = self.getRemainingWork()
            if lastPauseLenght < timedelta(hours=1) and remaining > timedelta(hours=1):
                return 1
        return 0

    def getOvertime(self) -> timedelta:
        overtime = timedelta(0)
        for work in self.work:
            if hasattr(work, 'stop'):
                delta = datetime.combine(
                    date.min, work.stop
                ) - datetime.combine(
                    date.min, work.start
                )
                overtime += delta
        overtime = overtime - self.goal
        return overtime

    def getStartTime(self) -> timedelta:
        return self.__getFirstWorkStart()

    def getEndTime(self) -> timedelta:
        startDate = datetime.combine(
            datetime.now(),
            self.getStartTime()
        )
        endTime = startDate + self.goal + self.getPausetime()
        return endTime

    def __getFirstWorkStart(self) -> datetime:
        startTimes = []
        for work in self.work:
            startTimes.append(work.start)
        startTimes.sort()
        return startTimes[0]

    def getLastWork(self) -> Work:
        startTimes = []
        for work in self.work:
            startTimes.append(work.start)
        startTimes.sort()
        for work in self.work:
            if startTimes[-1] == work.start:
                return work
        raise TypeError('Last work block not found')

    def getCurrentWork(self) -> timedelta:
        time = timedelta(0)
        for work in self.work:
            time += work.getDuration()
        return time

    def getRemainingWork(self) -> timedelta:
        pauseTime = self.getPausetime()
        # calculate for 30 minutes pause if none taken yet
        if pauseTime == timedelta(0):
            pauseTime = timedelta(minutes=30)
        return (self.goal) - self.getCurrentWork()

    def getPausetime(self) -> timedelta:
        time = timedelta(0)
        for pause in self.calculatePauses():
            time += pause.getDuration()
        return time

    def getLastCategory(self) -> str:
        return self.getLastWork().category