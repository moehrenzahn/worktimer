from data.days import Days
import io
import main
import storage
import importer
from os import path
from unittest.mock import patch
from freezegun import freeze_time
from contextlib import redirect_stdout


# Run command (on simulated date) and return standard output
def run(command = None, date = '2021-01-02 8:00', subcommand = None) -> str:
    testargs = [
        'WorkTimer.py',
        '--log=test/integration/tmp_sample_1',
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

def getDays(file = 'tmp_sample_1') -> Days:
    json = storage.load(path.dirname(path.realpath(__file__)) + '/' + file + '.json')
    return importer.getDays(json)