from day import Day
from today import Today
from datetime import Datetime


class Days:
    def __init__(self, json):
        self.overtime = 0
        self.days = []
        self.today
        for dayElement in json:
            dayElement = json[dayElement]
            self.processDay(dayElement)

    def processDay(self, dayElement):
        day = Day(dayElement)
        self.overtime += day.overtime
        self.days.append(day)
        # process current day
        if day.date == Datetime.now().date():
            self.today = Today(dayElement)