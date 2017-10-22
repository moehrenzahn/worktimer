import data
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta


class Days:
    def __init__(self, days):
        """
        days: [Day]]
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
        overtime = timedelta(minutes=0)
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
