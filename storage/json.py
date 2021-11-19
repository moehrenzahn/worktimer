import os
import json as jsonlib
import io
import config
from datetime import date, timedelta, time
import data

def load(file):
    # return empty array if file is empty
    if os.stat(file).st_size == 0:
        os.remove(file)
        return []
    with io.open(file, 'r') as data:
        jsonData = jsonlib.load(data)
    return jsonData

def save(days):
    data = {}
    # serialize with date keys
    for day in days.days:
        data[day.date.strftime("%Y-%m-%d")] = day
    data = jsonlib.dumps(
        data,
        sort_keys=True,
        default=lambda o: jsonDefault(o),
        indent=4
    )
    if data:
        file = io.open(config.log_path(), 'w', encoding='utf8')
        file.write(data)
        file.close()


def jsonDefault(value):
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        if isinstance(value, timedelta):
            return data.format_delta(value)
        else:
            return value.__dict__
