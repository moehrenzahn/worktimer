import storage
import data
import actions
import output
import config
from datetime import datetime


def timer(days, category="", summary = ""):
    if days.isPause():
        output.notification(
            "Timer is Paused",
            "Please end pause before starting or stopping the timer"
        )
        return
    if days.isTimer() and not category:
        actions.timerStop(days)
        output.notification(
            "Work timer stopped",
            "Remember to stop any time tracking"
        )
        if config.autoSync():
            actions.syncUp()
            output.notification(
                "Synchronisation",
                "Work log synced with remote repo"
            )
    else:
        if config.autoSync():
            actions.syncDown()
        actions.timerStart(days, category, summary)

def timerStart(days, category="", summary = ""):
    if not category:
        category = config.default_category()
    
    today = days.getToday()
    if today:
        lastWork = today.getLastWork()
        if lastWork.isRunning():
            # A timer is running
            if lastWork.category == category and (lastWork.summary == summary or not summary):
                output.notification(
                    "Work timer running",
                    "You already have a timer running for %s." % output.formatter.format_category(category)
                )
                return
            else:
                # Stop the last work block in another category
                lastWork.stop = datetime.now().time()

    if not today:
        today = data.newDay(category, summary)
        days.days.append(today)
    else:
        today.work.append(data.newWork(category, summary))
    storage.yaml.save(days)

    untilTime = data.formatter.format_time(days.getToday().getEndTime())
    descr = output.formatter.format_category(category)
    if summary:
        descr = "%s: %s" % (descr, summary)
    output.notification(
        "Work timer started for '%s'" % descr,
        "You will have to work until %s" % untilTime
    )


def timerStop(days):
    today = days.getToday()
    for work in today.work:
        if work.isRunning():
            work.stop = datetime.now().time()
    storage.yaml.save(days)
    if config.imessage():
        output.message(config.imessage_address(), config.imessage_text())
