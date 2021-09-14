import unittest
from actions.exportExcel import export
from os import remove
from shutil import copyfile
from test.integration.helper import getDays, sampleFilePath, prepareSampleJson, cleanUpSampleJson
import io
from contextlib import redirect_stdout
class ExcelExportTestCase(unittest.TestCase):
    
    def setUp(self):
        copyfile(sampleFilePath('sample1.xlsx'), sampleFilePath('tmp_sample_1.xlsx'))
        prepareSampleJson()

    def tearDown(self):
        remove(sampleFilePath('tmp_sample_1.xlsx'))
        cleanUpSampleJson()

    def testExport(self):
        days = getDays()
        f = io.StringIO()
        with redirect_stdout(f):
            result = export(days, sampleFilePath('tmp_sample_1.xlsx'))
        self.assertTrue(result) # Module openpyxl must be installed. Install it via "pip install openpyxl"


if __name__ == '__main__':
    unittest.main()
