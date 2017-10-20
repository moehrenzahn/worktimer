from day import Day


class Today(Day):
    def __init__(self, date, goal, work, paused=None):
        """
        A special kind of day used to easily identify current day.
        date: string "YYYY-MM-DD"
        goal: string "HH:MM"
        work: [Work]
        paused: bool (default None)
        """
        Day.__init__(self, date, goal, work)
        if paused is not None:
            self.paused = paused
        else:
            self.paused = self.isPause()

    def isPause(self):
        if hasattr(self, 'paused'):
            return self.paused
        else:
            return Day.isPause(self)
