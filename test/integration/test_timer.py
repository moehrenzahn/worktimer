import unittest
from test.integration.helper import run, prepareSampleJson, cleanUpSampleJson


class IntegrationTimerTestCase(unittest.TestCase):

    def setUp(self):
        prepareSampleJson()

    def tearDown(self):
        cleanUpSampleJson()

    def test_timer(self):
        # Stop ongoing timer to land at 0:00 overtime
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        # Start timer on next day
        output = run('timer', '2021-01-03 8:00')
        self.assertIn('work until 16:00', output)

        output = run(None, '2021-01-03 8:30')
        self.assertIn('Remaining: 7:30', output)

        output = run(None, '2021-01-03 16:30')
        self.assertIn('Remaining: -0:30', output)

        # Stop timer
        output = run('timer', '2021-01-03 17:00')
        self.assertIn('timer stopped', output)

        output = run(None, '2021-01-03 16:30')
        self.assertIn('Overtime: 1:00', output)

    def test_timer_multiple(self):
        # Stop ongoing timer to land at 1 hour worked
        output = run('timer', '2021-01-02 8:00')
        self.assertIn('timer stopped', output)

        # Start timer on same day.
        output = run('timer', '2021-01-02 10:00')
        self.assertIn('work until 17:00', output)

        # Stop timer
        output = run('timer', '2021-01-02 17:00')
        self.assertIn('timer stopped', output)

        # No overtime added
        output = run(None, '2021-01-02 17:00')
        self.assertIn('Overtime: -1:00', output)


    def test_timer_past(self):
        # Stop ongoing timer to land at 0:00 overtime
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        output = run('timer', '1980-01-01 0:00')
        self.assertIn('work until 8:00', output)
        output = run('timer', '1980-01-01 9:00')
        self.assertIn('timer stopped', output)
        output = run(None, '1980-01-01 9:00')
        self.assertIn('Overtime: 1:00', output)


if __name__ == '__main__':
    unittest.main()
