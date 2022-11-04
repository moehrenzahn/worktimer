import unittest
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
import data

class DaysTestCase(unittest.TestCase):
    
    # The current date as far as the test is concernded 
    todayDateStr = '2017-01-02'

    def setUp(self):
        
        date1 = datetime.strptime('2017-01-01', '%Y-%m-%d').date()
        date2 = datetime.strptime(self.todayDateStr, '%Y-%m-%d').date()
        work1 = data.block.Work(
            datetime.strptime('08:00', '%H:%M').time(),
            '',
            datetime.strptime('12:00', '%H:%M').time()
        )
        work2 = data.block.Work(
            datetime.strptime('12:30', '%H:%M').time(),
            '',
            datetime.strptime('17:00', '%H:%M').time()
        )
        work3 = data.block.Work(
            datetime.strptime('12:30', '%H:%M').time()
        )
        goal = timedelta(hours=8)
        workArray1 = [
            work1,
            work2
        ]
        workArray2 = [
            work1,
            work3
        ]
        testDay1 = data.Day(date1, goal, None, workArray1)
        testDay2 = data.Today(date2, goal, None, workArray1)
        testDay3 = data.Today(date2, goal, None, workArray2)

        self.testDays1 = data.Days([testDay1, testDay2])
        self.testDays2 = data.Days([testDay1, testDay3])

    def test_isTimer(self):
        with freeze_time(self.todayDateStr):
            isTimer = self.testDays1.isTimer()
            self.assertEqual(isTimer, 0)
            isTimer = self.testDays2.isTimer()
            self.assertEqual(isTimer, 1)

    def test_overtime(self):
        with freeze_time(self.todayDateStr):
            overtime = self.testDays1.getOvertime()
            self.assertEqual(
                overtime,
                timedelta(hours=1)
            )

if __name__ == '__main__':
    unittest.main()
