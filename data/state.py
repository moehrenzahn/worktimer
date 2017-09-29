class State:
    def __init__(
        self,
        timer,
        pause,
        startTime,
        remainingTime,
        currentTime,
        pauseTime,
        overtime
    ):
        self.timer = timer
        self.pause = pause
        self.startTime = startTime
        self.remainingTime = remainingTime
        self.currentTime = currentTime
        self.pauseTime = pauseTime
        self.overtime = overtime
