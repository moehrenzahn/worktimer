from datetime import datetime, date


class Block:
    def __init__(self, start, category="", stop=0):
        """
        start: time
        category: string (optional)
        stop: time (optional)
        """
        self.start = start
        self.category = category
        if stop:
            self.stop = stop

    def getDuration(self):
        if hasattr(self, 'stop'):
            subtract = self.stop
        else:
            subtract = datetime.now().time()
        duration = datetime.combine(
            date.min, subtract
        ) - datetime.combine(
            date.min, self.start
        )
        return duration

    def isRunning(self):
        if hasattr(self, 'stop'):
            return 0
        else:
            return 1
