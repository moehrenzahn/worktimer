import unittest
from datetime import date
from datetime import datetime
from datetime import timedelta
import data


class BlockTestCase(unittest.TestCase):
    def setUp(self):
        start = datetime.strptime('08:00', '%H:%M').time()
        end = datetime.strptime('12:00', '%H:%M').time()
        self.testBlock1 = data.block.Block(start, end)
        self.testBlock2 = data.block.Block(start)

    def test_duration(self):
        duration = self.testBlock1.getDuration()
        self.assertEqual(duration, timedelta(hours=4))
        duration = self.testBlock2.getDuration()
        # This needs a mock for datetime.now().time()
        #
        # self.assertEqual(
        #     duration,
        #     datetime.combine(
        #         date.min, datetime.now().time()
        #     ) - datetime.combine(
        #         date.min, datetime.strptime('08:00', '%H:%M').time()
        #     )
        # )

    def test_running(self):
        isRunning1 = self.testBlock1.isRunning()
        isRunning2 = self.testBlock2.isRunning()
        self.assertEqual(isRunning1, 0)
        self.assertEqual(isRunning2, 1)


if __name__ == '__main__':
    unittest.main()
