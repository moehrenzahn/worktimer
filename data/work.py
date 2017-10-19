from datetime import datetime, date


class Work:
    def __init__(self, start, end=0):
        """
        start: time
        end: time (optional)
        """
        self.start = start
        if end:
            self.end = end

    def getDuration(self):
        if hasattr(self, 'end'):
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
