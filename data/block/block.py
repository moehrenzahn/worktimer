from datetime import datetime, date


class Block:
    def __init__(self, start, stop=0):
        """
        start: time
        stop: time (optional)
        """
        self.start = start
        if stop:
            self.stop = stop

    def getDuration(self):
        if hasattr(self, 'stop'):
            subtract = self.stop
        else:
            subtract = datetime.now().time()
        return datetime.combine(
            date.min, subtract
        ) - datetime.combine(
            date.min, self.start
        )

    def isRunning(self):
        if hasattr(self, 'stop'):
            return 0
        else:
            return 1
