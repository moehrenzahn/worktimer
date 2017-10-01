from datetime import datetime, date


class Pause:

    def __init__(self, pauseItem):
        if "start" not in pauseItem:
            print("Pause must have a start item")
            exit(2)
        self.start = datetime.strptime(pauseItem["start"], '%H:%M').time()
        self.isRunning = 1
        if "end" in pauseItem:
            self.end = datetime.strptime(pauseItem["end"], '%H:%M').time()
            self.isRunning = 0
        # simulate a full date to enable subtraction
        if hasattr(self, "end"):
            subtractEnd = self.end
        else:
            subtractEnd = datetime.now().time()
        self.duration = datetime.combine(date.min, subtractEnd) - datetime.combine(date.min, self.start)
