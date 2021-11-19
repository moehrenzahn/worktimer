import unittest
from exporter.excel import export
from os import remove
from test.integration.helper import getDays, sampleFilePath, prepareSampleFile, cleanUpSampleFile
import io
from contextlib import redirect_stdout
class ExcelExportTestCase(unittest.TestCase):
    
    def setUp(self):
        prepareSampleFile('sample2')

    def tearDown(self):
        remove(sampleFilePath('tmp_sample.xlsx'))
        cleanUpSampleFile()

    def testExport(self):
        days = getDays()
        f = io.StringIO()
        with redirect_stdout(f):
            # Module openpyxl must be installed. Install it via "pip install openpyxl"
            export(days, sampleFilePath('sample1.xlsx'), sampleFilePath('tmp_sample.xlsx'))


if __name__ == '__main__':
    unittest.main()
