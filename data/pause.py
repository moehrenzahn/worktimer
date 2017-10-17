from datetime import datetime, date


class Pause:

    def __init__(self, pauseItem):
        if "start" not in pauseItem:
            print("Pause must have a start item")
            exit(2)
        self.start = datetime.strptime(pauseItem["start"], '%H:%M').time()
        if "end" in pauseItem:
            self.end = datetime.strptime(pauseItem["end"], '%H:%M').time()

    def getDuration(self):
        if self.end:
            subtractEnd = self.end
        else:
            subtractEnd = datetime.now().time()
        return datetime.combine(
            date.min, subtractEnd
        ) - datetime.combine(
            date.min, self.start
        )

    def isRunning(self):
        if hasattr(self, 'end'):
            return 0
        else:
            return 1
