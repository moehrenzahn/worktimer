from day import Day


class Today(Day):
    def __init__(self, date, goal, workArray):
        """
        A special kind of day used to easily identify current day.
        date: string "YYYY-MM-DD"
        goal: string "HH:MM"
        workArray: [Work]
        """
        Day.__init__(self, date, goal, workArray)
