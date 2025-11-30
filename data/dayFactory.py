from datetime import datetime
from datetime import timedelta
import data
import config


def newDay(category="", summary = ""):
    return data.Today(
        datetime.now().date(),
        timedelta(hours=config.hoursPerDay()),
        None,
        [data.newWork(category, summary)]
    )


def newWork(category="", summary = ""):
    return data.block.Work(
        datetime.now().time(),
        category,
        summary
    )
