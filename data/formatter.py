from datetime import datetime
from datetime import time
from datetime import timedelta


def format_delta(td):
    if type(td) is not timedelta:
        return ''
    if td < timedelta(0):
        return '-' + format_delta(-td)
    s = td.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    minutes = str(minutes).zfill(2)
    return '' + '%s:%s' % (hours, minutes)


def format_time(t):
    if type(t) is timedelta:
        t = (datetime.min + t).time()
    if type(t) is time:
        t = datetime(2000, 1, 1, t.hour, t.minute)
    return datetime.strftime(t, "%H:%M")
