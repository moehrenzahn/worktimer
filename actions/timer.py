import storage
import data
import actions
import output
import config
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
    today = days.getToday()
    if not today:
        today = data.newDay()
        days.days.append(today)
    else:
        today.work.append(data.newWork())
    storage.save(days)


def timerStop(days):
    today = days.getToday()
    for work in today.work:
        if work.isRunning():
            work.stop = datetime.now().time()
    storage.save(days)
    if config.imessage:
        output.message(config.imessage_address, config.imessage_text)
