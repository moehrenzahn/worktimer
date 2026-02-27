import data
import config
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from typing import List

class Days:
    def __init__(self, days: List[data.Day]):
        """
        days: List[Day]]
        """
        self.days = days

    def getDay(self, searchDate):
        for day in self.days:
            if day.date == searchDate:
                return day
        raise ValueError(
            'Day with date %s does not exist' % date.strftime(searchDate, "%Y-%m-%d")
        )

    def getOvertime(self):
        overtime = timedelta(minutes=config.overtime_offset_in_minutes())
        for day in self.days:
            overtime += day.getOvertime()
        return overtime

    def getToday(self):
        try:
            day = self.getDay(datetime.now().date())
        except ValueError:
            day = 0
        # check if day is of type Today
        if isinstance(day, data.Today):
            return day
        else:
            return 0

    def getRecentSummaries(self, limit: int = 5, category: str = "") -> list[str]:
        summaries = []
        for day in self.days:
            for task in day.work:
                if category and task.category != category:
                    continue
                if not task.summary or task.summary in summaries:
                    continue
                summaries.append(task.summary)
                if len(summaries) >= limit: break
        return summaries

    def isPause(self):
        today = self.getToday()
        if today:
            return today.paused
        return 0

    def isTimer(self):
        if self.isPause():
            return 1
        today = self.getToday()
        if today:
            return today.isRunning()
        return 0
