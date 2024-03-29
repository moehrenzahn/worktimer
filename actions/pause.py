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
    for work in today.work:
        # To be safe we stop all of today's
        # work blocks that are still running.
        if work.isRunning():
            work.stop = datetime.now().time()
    today.paused = 1
    storage.yaml.save(days)


def pauseStop(days):
    today = days.getToday()
    now = datetime.now().time()
    lastWork = today.getLastWork()
    if lastWork.stop.hour == now.hour and lastWork.stop.minute == now.minute:
        # If the break was 0 minutes, we cancel it.
        del lastWork.stop
    else:
        today.work.append(
            data.block.Work(
                now,
                lastWork.category
        ))
    today.paused = 0
    storage.yaml.save(days)
