import unittest
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
import data

class BlockTestCase(unittest.TestCase):
    def setUp(self):
        start = datetime.strptime('08:00', '%H:%M').time()
        stop = datetime.strptime('12:00', '%H:%M').time()
        self.testBlock1 = data.block.Block(start, "", stop)
        self.testBlock2 = data.block.Block(start, "")

    def test_duration(self):
        duration = self.testBlock1.getDuration()
        self.assertEqual(duration, timedelta(hours=4))
        with freeze_time('2017-01-01 10:00'):
            duration = self.testBlock2.getDuration()
            self.assertEqual(duration, timedelta(hours=2))

    def test_running(self):
        isRunning1 = self.testBlock1.isRunning()
        isRunning2 = self.testBlock2.isRunning()
        self.assertEqual(isRunning1, 0)
        self.assertEqual(isRunning2, 1)

if __name__ == '__main__':
    unittest.main()
