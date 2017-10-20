import storage
import data
from datetime import datetime


def pauseStart(days):
    today = days.getToday()
    today.getLastWork().end = datetime.now().time()
    today.paused = 1
    storage.save(days)


def pauseStop(days):
    today = days.getToday()
    today.work.append(data.block.Work(datetime.now().time()))
    today.paused = 0
    storage.save(days)
