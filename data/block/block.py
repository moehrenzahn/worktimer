from datetime import datetime, date, timedelta


class Block:
    def __init__(self, start, category="", summary = "", stop=0):
        """
        start: time
        category: string (optional)
        stop: time (optional)
        """
        self.start = start
        self.category = category
        self.summary = summary
        if stop:
            self.stop = stop

    def getDuration(self) -> timedelta:
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

    def isRunning(self) -> int:
        if hasattr(self, 'stop'):
            return 0
        else:
            return 1
