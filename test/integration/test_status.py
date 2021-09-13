import unittest
from os import path, remove
from shutil import copyfile
from test.integration.helper import run


class IntegrationStatusTestCase(unittest.TestCase):

    def setUp(self):
        integrationPath = path.dirname(path.realpath(__file__))
        copyfile(integrationPath + '/sample1.json', integrationPath + '/tmp_sample_1.json')

    def tearDown(self):
        integrationPath = path.dirname(path.realpath(__file__))
        remove(integrationPath + '/tmp_sample_1.json')

    def test_timer(self):
        output = run(None, '2021-01-03 8:00')
        self.assertIn('Free', output)
        self.assertIn('Total Overtime: -9:00', output)

    def test_timer_current(self):
        output = run(None, '2021-01-02 8:00')
        self.assertIn('Remaining: 7:00', output)
        self.assertIn('Worked 1:00', output)
        self.assertIn('Pause: 0:00', output)
        self.assertIn('Start: 07:00', output)
        self.assertIn('End: 15:00', output)


if __name__ == '__main__':
    unittest.main()
