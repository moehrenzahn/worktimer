import io
import config
import json
from datetime import date, timedelta, time
import data

def save(days):
    data = {}
    # serialize with date keys
    for day in days.days:
        data[day.date.strftime("%Y-%m-%d")] = day
    data = json.dumps(
        data,
        sort_keys=True,
        default=lambda o: jsonDefault(o),
        indent=4
    )
    if data:
        file = io.open(config.log_path, 'w', encoding='utf8')
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
