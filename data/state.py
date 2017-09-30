from datetime import datetime


class State:
    def __init__(
        self,
        timer,
        overtime,
        today=None
    ):
        self.isTimer = timer
        self.overtime = overtime
        if today is not None:
            self.pause = today.pauseTime
            self.start = datetime.combine(today.date, today.start)
            self.goal = today.goal
            self.remainingWork = today.remainingWork
            self.currentWork = today.currentWork
            if today.pauses:
                self.isPause = today.pauses[-1].isRunning
            else:
                self.isPause = 0
