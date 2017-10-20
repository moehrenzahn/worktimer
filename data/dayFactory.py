from datetime import datetime
import data


def newDay():
    return data.Today(
        datetime.now().date(),
        datetime.timedelta(hours=8),
        [data.newWork()]
    )

def newPause():
    return data.block.Pause(datetime.now().time())


def newWork():
    return data.block.Work(datetime.now().time())
