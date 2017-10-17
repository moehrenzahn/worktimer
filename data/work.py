from datetime import datetime, date


class Work:

    def __init__(self, start, end=0):
        self.start = datetime.strptime(start, '%H:%M').time()
        if end:
            self.end = datetime.strptime(end, '%H:%M').time()

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
