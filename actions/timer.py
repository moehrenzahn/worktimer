import storage
import data
import output
from datetime import datetime


def timerStart(days):
    today = data.newDay()
    days.today = today
    days.days.append(today)
    storage.save(days)


def timerStop(days):
    try:
        currentDay = days.getDay(datetime.now().date())
        currentDay.end = datetime.now().time()
        storage.save(days)
    except ValueError as error:
        output.notification("Timer not stopped", error)
        exit(2)
