from day import Day


class Today(Day):
    def __init__(self, date, goal, work):
        Day.__init__(self, date, goal, work)

    def getEndtime(self):
        return self.start + self.getPausetime() + self.goal
