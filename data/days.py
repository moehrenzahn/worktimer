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
        for day in reversed(self.days):
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
        return self.getDay(datetime.now().date())

    def json_default(self, value):
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        if isinstance(value, timedelta):
            return data.format_delta(value)
        else:
            return value.__dict__

    def isTimer(self):
        for day in self.days:
            if day.isRunning():
                return 1
        return 0

    def isPause(self):
        for day in self.days:
            if day.isPause():
                return 1
        return 0
