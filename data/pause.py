from datetime import datetime, date


class Pause:
    def __init__(self, start, end=0):
        self.start = start
        if end:
            self.end = end

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
