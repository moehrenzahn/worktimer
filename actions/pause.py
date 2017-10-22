import storage
import data
import actions
import output
from datetime import datetime


def pause(days):
    if days.isPause():
        actions.pauseStop(days)
        pauseTime = data.formatter.format_time(days.getToday().getPausetime())
        output.notification(
            "Break ended",
            "Full break time: %s" % pauseTime
        )
    else:
        actions.pauseStart(days)
        stopTime = data.formatter.format_time(days.getToday().getLastWork().stop)
        output.notification(
            "Break started",
            "Started break at %s" % stopTime
        )


def pauseStart(days):
    today = days.getToday()
    today.getLastWork().stop = datetime.now().time()
    today.paused = 1
    storage.save(days)


def pauseStop(days):
    today = days.getToday()
    today.work.append(data.block.Work(datetime.now().time()))
    today.paused = 0
    storage.save(days)
