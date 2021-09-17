from data.days import Days
import io
import main
import json
import storage
import importer
from os import path, remove
from shutil import copyfile
from unittest.mock import patch
from freezegun import freeze_time
from contextlib import redirect_stdout


# Run command (on simulated date) and return standard output
def run(command = None, date = '2021-01-02 8:00', subcommand = None) -> str:
    testargs = [
        'WorkTimer.py',
        '--log=test/data/tmp_sample',
        '--sync_automatically=false',
        '--default_category=default',
        '--notifications=false',
        '--imessage=false',
        '--textbar=false'
    ]
    if command:
        testargs.insert(1, command)
        if subcommand:
            testargs.insert(2, subcommand)


    f = io.StringIO()
    with freeze_time(date), patch('sys.argv', testargs), redirect_stdout(f):
        exit = main.main()

    return f.getvalue()

def prepareSampleJson(name = 'sample1'):
    copyfile(sampleFilePath(name + '.json'), sampleFilePath('tmp_sample.json'))

def cleanUpSampleJson():
    remove(sampleFilePath('tmp_sample.json'))


def sampleFilePath(name):
    integrationPath = path.dirname(path.realpath(__file__))
    integrationPath = integrationPath.replace('integration', 'data')
    return  integrationPath + '/' + name

def getDays(file = 'tmp_sample', date = '2021-01-02 8:00') -> Days:
    path = sampleFilePath(file + '.json')
    with freeze_time(date):
        json = storage.load(path)
        return importer.getDays(json)