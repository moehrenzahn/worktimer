import shutil
import unittest
from unittest.mock import patch
from freezegun import freeze_time
import io
from os import path, remove
from contextlib import redirect_stdout
import main
from shutil import copyfile

class IntegrationTimerTestCase(unittest.TestCase):
    # Run command (on simulated date) and return standard output
    def _run(self, command = None, date = '2021-01-02 8:00'):
        testargs = [
            'WorkTimer.py',
            '--log=test/integration/tmp_sample_1',
            '--textbar=false'
        ]
        if command:
            testargs.insert(1, command)

        f = io.StringIO()
        with freeze_time(date), patch('sys.argv', testargs), redirect_stdout(f):
            exit = main.main()

        self.assertEqual(exit, 0)    
        return f.getvalue()

    def setUp(self):
        integrationPath = path.dirname(path.realpath(__file__))
        copyfile(integrationPath + '/sample1.json', integrationPath + '/tmp_sample_1.json')

    def tearDown(self):
        integrationPath = path.dirname(path.realpath(__file__))
        remove(integrationPath + '/tmp_sample_1.json')

    def test_timer(self):
        output = self._run(None, '2021-01-03 8:00')
        self.assertIn('Free', output)
        self.assertIn('Total Overtime: -9:00', output)

    def test_timer_current(self):
        output = self._run(None, '2021-01-02 8:00')
        self.assertIn('Remaining: 7:00', output)
        self.assertIn('Worked 1:00', output)
        self.assertIn('Pause: 0:00', output)
        self.assertIn('Start: 07:00', output)
        self.assertIn('End: 15:00', output)

    def test_timer_pause(self):
        # Start pause
        output = self._run('pause', '2021-01-02 8:00')
        self.assertIn('Started break at 08:00', output)
        
        # Status
        output = self._run(None, '2021-01-02 8:15')
        self.assertIn('Pause: 0:15', output)
        self.assertIn('Worked 1:00', output)

        # Stop pause
        output = self._run('pause', '2021-01-02 8:30')
        self.assertIn('Full break time: 00:30', output)

        # Status
        output = self._run(None, '2021-01-02 9:00')
        self.assertIn('Pause: 0:30', output)
        self.assertIn('Worked 1:30', output)

    def test_timer_pause_multi(self):
        # Start pause
        output = self._run('pause', '2021-01-02 8:00')
        # Stop pause
        output = self._run('pause', '2021-01-02 8:30')
        self.assertIn('Full break time: 00:30', output)

        # Start pause
        output = self._run('pause', '2021-01-02 9:00')
        # Stop pause
        output = self._run('pause', '2021-01-02 9:30')
        self.assertIn('Full break time: 01:00', output)

        # Status
        output = self._run(None, '2021-01-02 10:00')
        self.assertIn('Pause: 1:00', output)
        self.assertIn('Worked 2:00', output)


if __name__ == '__main__':
    unittest.main()
