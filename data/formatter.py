from datetime import datetime
from datetime import time
from datetime import timedelta
import config

def format_delta(td):
    if type(td) is not timedelta:
        return ''
    if td < timedelta(0):
        return '-' + format_delta(-td)
    
    s = int(td.total_seconds())
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    minutes = str(minutes).zfill(2)
    return '' + '%s:%s' % (hours, minutes)


def format_time(t):
    if type(t) is timedelta:
        t = (datetime.min + t).time()
    if type(t) is time:
        t = datetime(2000, 1, 1, t.hour, t.minute)
    return datetime.strftime(t, "%-H:%M")

def format_category(category):
    if category in config.categories():
        return config.categories()[category]
    else:
        return category.title().replace('_', ' ')

def format_category_percentages(totalTime: timedelta, categorytimes: dict[str, timedelta]):
    result = ""
    for category, worked in categorytimes.items():
            result += format_category(category) + ": "
            result += format_percentage(totalTime, worked) + '\n'
    return result

def format_percentage(full, partial):
    return str(round((partial / full) * 100, 1)) + "%"