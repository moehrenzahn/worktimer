import storage
import data
import actions
import output
from datetime import datetime


def timer(days):
    if days.isTimer():
        actions.timerStop(days)
        output.notification(
            "Work timer stopped",
            "Remember to stop any time tracking"
        )
    else:
        actions.timerStart(days)
        untilTime = data.formatter.format_time(days.getToday().getEndTime())
        output.notification(
            "Work timer started",
            "You will have to work until %s" % untilTime
        )


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
