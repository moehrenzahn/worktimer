import unittest
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
import data

class DayTestCase(unittest.TestCase):
    def setUp(self):
        date = datetime.strptime('2017-01-01', '%Y-%m-%d').date()
        goal = datetime.strptime('08:00', "%H:%M")
        goal = timedelta(hours=goal.hour, minutes=goal.minute)
        workArray = [
            data.block.Work(
                datetime.strptime('08:00', '%H:%M').time(),
                "cat",
                datetime.strptime('12:00', '%H:%M').time()
            ),
            data.block.Work(
                datetime.strptime('12:30', '%H:%M').time(),
                "cat",
                datetime.strptime('17:00', '%H:%M').time()
            )
        ]
        self.testDay = data.Day(date, goal, None, workArray)

    def test_overtime(self):
        overtime = self.testDay.getOvertime()
        self.assertEqual(overtime, timedelta(minutes=30))

    def test_currentWork(self):
        currentWork = self.testDay.getCurrentWork()
        self.assertEqual(currentWork, timedelta(hours=8, minutes=30))

    def test_pauseTime(self):
        with freeze_time('2017-01-01 17:00'):
            pauseTime = self.testDay.getPausetime()
            self.assertEqual(pauseTime, timedelta(minutes=30))
        with freeze_time('2017-01-01 17:30'):
            pauseTime = self.testDay.getPausetime()
            self.assertEqual(pauseTime, timedelta(minutes=60))

    def test_isRunning(self):
        date = datetime.strptime('2017-01-01', '%Y-%m-%d').date()
        goal = datetime.strptime('08:00', "%H:%M")
        goal = timedelta(hours=goal.hour, minutes=goal.minute)
        workArray = [
            data.block.Work('8:00', '', '12:00'),
            data.block.Work('12:30')
        ]
        runningDay = data.Day(date, goal, None, workArray)
        self.assertEqual(1, runningDay.isRunning())
        self.assertEqual(0, self.testDay.isRunning())


if __name__ == '__main__':
    unittest.main()
