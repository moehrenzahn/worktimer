import unittest
from actions.exportOds import export
from os import remove
from shutil import copyfile
from test.integration.helper import getDays, sampleFilePath, prepareSampleJson, cleanUpSampleJson

class OdsExportTestCase(unittest.TestCase):
    
    def setUp(self):
        copyfile(sampleFilePath('sample1.ods'), sampleFilePath('tmp_sample.ods'))
        prepareSampleJson()

    def tearDown(self):
        remove(sampleFilePath('tmp_sample.ods'))
        cleanUpSampleJson()

    @unittest.skip("Not implemented yet")
    def testExport(self):
        days = getDays()
        result = export(days, sampleFilePath('tmp_sample.ods'))
        self.assertTrue(result) # Module pyexcel_ods must be installed. Install it via "pip install pyexcel_ods"


if __name__ == '__main__':
    unittest.main()
