import storage
import data
from datetime import datetime


def timerStart(days):
    if not days.getToday():
        today = data.newDay()
        days.days.append(today)
    days.getToday().work.append(data.newWork())
    storage.save(days)


def timerStop(days):
    today = days.getToday()
    for work in today.work:
        if work.isRunning():
            work.end = datetime.now().time()
    storage.save(days)
