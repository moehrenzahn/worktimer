from datetime import datetime
from datetime import timedelta
import data
import config


def newDay(category=""):
    return data.Today(
        datetime.now().date(),
        timedelta(hours=config.hoursPerDay()),
        [data.newWork(category)]
    )


def newWork(category=""):
    return data.block.Work(
        datetime.now().time(),
        category
    )
