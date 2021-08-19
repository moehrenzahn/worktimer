from datetime import datetime
from datetime import timedelta
import data


def newDay(category=""):
    return data.Today(
        datetime.now().date(),
        timedelta(hours=8),
        [data.newWork(category)]
    )


def newWork(category=""):
    return data.block.Work(
        datetime.now().time(),
        category
    )
