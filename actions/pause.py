import storage
import data
from datetime import datetime


def pauseStart(days):
    newPause = data.newPause()
    day = days.getDay(datetime.now().date())
    day.pauses.append(newPause)
    days.today = Today(day)
    storage.save(days)


def pauseStop(days):
    day = days.getDay(datetime.now().date())
    day.pauses[-1].end = datetime.now().time()
    days.today = Today(day)
    storage.save(days)
