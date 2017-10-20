import data
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import json


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

    def toJSON(self):
        return json.dumps(
            self.days,
            default=lambda o: self.json_default(o),
            sort_keys=True,
            indent=4
        )

    def getOvertime(self):
        overtime = timedelta(minutes=0)
        for day in self.days:
            overtime += day.getOvertime()
        return overtime

    def getToday(self):
        day = self.getDay(datetime.now().date())
        if isinstance(day, data.Today):
            return day
        else:
            raise ValueError("Today does not exist")

    def json_default(self, value):
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        if isinstance(value, timedelta):
            return data.format_delta(value)
        else:
            return value.__dict__

    def isPause(self):
        today = self.getToday()
        return today.paused

    def isTimer(self):
        for day in self.days:
            if day.isRunning():
                return 1
        return 0
