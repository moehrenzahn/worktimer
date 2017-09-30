from datetime import datetime, date


class Pause:

    def __init__(self, pauseItem):
        self.isRunning = 0
        if "start" in pauseItem:
            self.start = datetime.strptime(pauseItem["start"], '%H:%M').time()
            self.isRunning = 1
        if "end" in pauseItem:
            self.end = datetime.strptime(pauseItem["end"], '%H:%M').time()
            self.isRunning = 0
        # simulate a full date to enable subtraction
        if self.start and self.end:
            subtractEnd = self.end
        else:
            subtractEnd = datetime.now().time
        self.duration = datetime.combine(date.min, subtractEnd) - datetime.combine(date.min, self.start)
