from datetime import datetime
from datetime import timedelta


class Day:

    def __init__(self, day):
        self.date = datetime.strptime(day["date"], '%Y-%m-%d').date()
        self.start = self.start(day)
        self.goal = self.goal(day)

        if "end" in day:
            self.end = self.end(day)

        delta = self.end - self.start
        self.overtime = delta - self.pause - self.goal

    def start(day):
        start = datetime.strptime(day["start"], '%H:%M')
        return start

    def pause(day):
        if "pause" in day:
            pause = timedelta(minutes=0)
            for item in day["pause"]:
                if "start" in item and "end" in item:
                    pauseStart = datetime.strptime(item["start"], '%H:%M')
                    pauseEnd = datetime.strptime(item["end"], '%H:%M')
                    pause += pauseEnd - pauseStart
        else:
            pause = timedelta(minutes=30)
        return pause

    def goal(day):
        if "halbtags" in day:
            goal = timedelta(minutes=240)
        elif "zusatz" in day:
            goal = timedelta(minutes=0)
        else:
            goal = timedelta(minutes=480)
        return goal

    def end(day):
        end = datetime.strptime(day["end"], '%H:%M')
        return end
