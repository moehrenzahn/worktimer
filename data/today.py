import datetime
from typing import List, Optional
from data.block.work import Work
from data.day import Day
from datetime import date, timedelta


class Today(Day):
    def __init__(self, date: date, goal: timedelta, comment: Optional[str], work: List[Work], paused: Optional[bool] = None):
        """
        A special kind of day used to easily identify current day.
        date: string "YYYY-MM-DD"
        goal: string "HH:MM"
        comment:  Optional[str] A text comment
        work: [Work]
        paused: bool (default None)
        """
        Day.__init__(self, date, goal, comment, work)
        if paused is not None:
            self.paused = paused
        else:
            self.paused = self.isPause()

    def isPause(self):
        if hasattr(self, 'paused'):
            return self.paused
        else:
            return Day.isPause(self)

    def getOvertime(self):
        if self.isRunning() or self.isPause():
            # don't coun't currently running day when calculating overtime
            overtime = timedelta(0)
        else:
            overtime = Day.getOvertime(self)
        return overtime
