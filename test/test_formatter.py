import unittest
from datetime import timedelta
from data import formatter
from freezegun import freeze_time

class FormatterTestCase(unittest.TestCase):
    
    # The current date as far as the test is concernded 
    todayDateStr = '2017-01-02'
        
    def testFormatTimedelta(self):
        td = timedelta(hours=1,minutes=15)
        result = formatter.format_delta(td)
        self.assertEqual(result, "1:15")
        
        td = timedelta(hours=5,minutes=60)
        result = formatter.format_delta(td)
        self.assertEqual(result, "6:00")
        
        td = timedelta(days=1,hours=1,minutes=1)
        result = formatter.format_delta(td)
        self.assertEqual(result, "25:01")

        td = timedelta(hours=2000,minutes=30)
        result = formatter.format_delta(td)
        self.assertEqual(result, "2000:30")
        
        td = timedelta(hours=-1,minutes=-15)
        result = formatter.format_delta(td)
        self.assertEqual(result, "-1:15")

if __name__ == '__main__':
    unittest.main()
