from datetime import datetime
from datetime import timedelta
import data


def newDay():
    return data.Today(
        datetime.now().date(),
        timedelta(hours=8),
        [data.newWork()]
    )


def newPause():
    return data.block.Pause(datetime.now().time())


def newWork():
    return data.block.Work(datetime.now().time())
