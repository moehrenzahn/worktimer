import unittest
from datetime import timedelta
import data


class WorkTestCase(unittest.TestCase):
    def setUp(self):
        start = '8:00'
        end = '12:00'
        self.testWork1 = data.Work(start, end)
        self.testWork2 = data.Work(start)

    def test_duration(self):
        duration = self.testWork1.getDuration()
        self.assertEqual(duration, timedelta(hours=4))

    def test_running(self):
        isRunning1 = self.testWork1.isRunning()
        isRunning2 = self.testWork2.isRunning()
        self.assertEqual(isRunning1, 0)
        self.assertEqual(isRunning2, 1)


if __name__ == '__main__':
    unittest.main()
