import unittest
from os import path, remove
from shutil import copyfile
from test.integration.helper import run


class IntegrationPauseTestCase(unittest.TestCase):
    
    def setUp(self):
        integrationPath = path.dirname(path.realpath(__file__))
        copyfile(integrationPath + '/sample1.json', integrationPath + '/tmp_sample_1.json')

    def tearDown(self):
        integrationPath = path.dirname(path.realpath(__file__))
        remove(integrationPath + '/tmp_sample_1.json')

    def test_pause(self):
        # Start pause
        output = run('pause', '2021-01-02 8:00')
        self.assertIn('Started break at 8:00', output)
        
        # Status
        output = run(None, '2021-01-02 8:15')
        self.assertIn('Pause: 0:15', output)
        self.assertIn('Worked 1:00', output)

        # Stop pause
        output = run('pause', '2021-01-02 8:30')
        self.assertIn('Full break time: 0:30', output)

        # Status
        output = run(None, '2021-01-02 9:00')
        self.assertIn('Pause: 0:30', output)
        self.assertIn('Worked 1:30', output)

    def test_pause_multi(self):
        # Start pause
        output = run('pause', '2021-01-02 8:00')
        # Stop pause
        output = run('pause', '2021-01-02 8:30')
        self.assertIn('Full break time: 0:30', output)

        # Start pause
        output = run('pause', '2021-01-02 9:00')
        # Stop pause
        output = run('pause', '2021-01-02 9:30')
        self.assertIn('Full break time: 1:00', output)

        # Status
        output = run(None, '2021-01-02 10:00')
        self.assertIn('Pause: 1:00', output)
        self.assertIn('Worked 2:00', output)

    def test_timer_while_paused(self):
        # Start pause
        output = run('pause', '2021-01-02 8:00')

        # Toggle timer, which should fail
        output = run('timer', '2021-01-02 8:30')
        self.assertIn('Please end pause before starting or stopping the timer', output)

        # Status is still paused
        output = run(None, '2021-01-02 10:00')
        self.assertIn('Pause: 2:00', output)

if __name__ == '__main__':
    unittest.main()
