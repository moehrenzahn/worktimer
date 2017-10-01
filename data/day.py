from datetime import datetime, date
from datetime import timedelta
import data


class Day():
    def __init__(self, day, dateString=""):
        if "date" in day:
            dateString = day["date"]
        self.date = datetime.strptime(dateString, '%Y-%m-%d').date()
        self.start = self.setStart(day)
        self.goal = self.setGoal(day)
        self.pauses = self.setPauses(day)
        self.pauseTime = timedelta(0)
        for pause in self.pauses:
            self.pauseTime += pause.duration

        if "end" in day:
            self.end = self.setEnd(day)
            delta = datetime.combine(date.min, self.end) - datetime.combine(date.min, self.start)
            self.overtime = delta - self.pauseTime - self.goal

    def setStart(self, day):
        start = datetime.strptime(day["start"], '%H:%M').time()
        return start

    def setPauses(self, day):
        pauses = []
        if "pauses" in day:
            for item in day["pauses"]:
                pauses.append(data.Pause(item))
        return pauses

    def setGoal(self, day):
        if "zusatz" in day:
            goal = timedelta(minutes=0)
        else:
            goal = timedelta(minutes=480)
        return goal

    def setEnd(self, day):
        end = datetime.strptime(day["end"], '%H:%M').time()
        return end
