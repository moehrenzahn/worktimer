import unittest
from test.integration.helper import run, getDays, prepareSampleFile, cleanUpSampleFile


class IntegrationTimerTestCase(unittest.TestCase):

    def setUp(self):
        prepareSampleFile()

    def tearDown(self):
        cleanUpSampleFile()

    def test_default_category(self):
        # Get sample data categories
        firstDay = getDays().days[0]
        self.assertEqual(firstDay.work[0].category, 'div')
        self.assertEqual(firstDay.work[1].category, 'test')


        # Stop ongoing timer to land at 0:00 overtime
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        lastDay = getDays().days[-1]
        self.assertEqual(lastDay.work[0].category, 'div')

        # Start timer on next day
        output = run('timer', '2021-01-03 8:00')
        self.assertIn('timer started for \'Default\'', output)

        # Stop timer
        output = run('timer', '2021-01-03 17:00')
        self.assertIn('timer stopped', output)

        lastDay = getDays().days[-1]
        self.assertEqual(lastDay.work[0].category, 'default')

    def test_switch_category(self):
        # Switch category
        output = run('timer', '2021-01-02 14:00', 'switched')
        self.assertIn('timer started for \'Switched\'', output)
        
        # Switch category again
        output = run('timer', '2021-01-02 15:00', 'another_switch')
        self.assertIn('timer started for \'Another Switch\'', output)
        
        # Stop timer
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        lastDay = getDays().days[-1]
        self.assertEqual(lastDay.work[0].category, 'div')
        self.assertEqual(lastDay.work[1].category, 'switched')
        self.assertEqual(lastDay.work[2].category, 'another_switch')

    def test_pointless_category_switch(self):
        # Switch category
        output = run('timer', '2021-01-02 14:00', 'div')
        self.assertIn('You already have a timer running for', output)
        
        # Stop timer
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        lastDay = getDays().days[-1]
        self.assertEqual(1, len(lastDay.work))
        self.assertEqual(lastDay.work[0].category, 'div')

    def test_category_after_pause(self):
        # Pause
        output = run('pause', '2021-01-02 14:00')
        self.assertIn('Break started', output)
        
        # Stop pause
        output = run('pause', '2021-01-02 14:30')
        self.assertIn('Break ended', output)

        lastDay = getDays().days[-1]
        self.assertEqual(2, len(lastDay.work))
        # New work block should inherit category from before break 
        self.assertEqual(lastDay.work[0].category, 'div')
        self.assertEqual(lastDay.work[1].category, 'div')

    def test_update_category(self):
        # Update Summary
        output = run('update', '2021-01-02 14:10', 'other')
        self.assertIn('Category updated: Work category retroactively changed to Other', output)

        # Stop timer
        output = run('timer', '2021-01-02 16:00')
        self.assertIn('timer stopped', output)

        lastDay = getDays().days[-1]
        self.assertEqual(lastDay.work[0].category, 'other')


if __name__ == '__main__':
    unittest.main()
