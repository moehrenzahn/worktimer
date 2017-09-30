import data
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import json


class Days:
    def __init__(self, json):
        self.json = json
        self.overtime = timedelta(minutes=0)
        self.days = []
        for day in self.json:
            if type(day) is dict:
                dayElement = day
            else:
                dayElement = json[day]
            self.processDay(dayElement, day)

    def processDay(self, dayElement, date):
        day = data.Day(dayElement, date)
        if hasattr(day, "overtime"):
            self.overtime += day.overtime
        self.days.append(day)
        # process current day
        if day.date == datetime.now().date():
            self.today = data.Today(dayElement, date)

    def getDay(self, date):
        for day in reversed(self.days):
            if day.date == date:
                return day
        print("Day not found")
        exit(2)

    def toJSON(self):
        return json.dumps(
            self.days,
            default=lambda o: self.json_default(o),
            sort_keys=True,
            indent=4
        )

    def json_default(self, value):
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        if isinstance(value, timedelta):
            return data.format_delta(value)
        else:
            return value.__dict__
