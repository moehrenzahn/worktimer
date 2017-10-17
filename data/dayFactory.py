from datetime import datetime
import data


def newDay():
    dateString = datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.now().strftime("%H:%M")
    day = {
        "date": dateString,
        "work":
        {
            "start": timeString
        }
    }
    newDay = data.Today(day, dateString)
    return newDay


def newPause():
    timeString = datetime.now().strftime("%H:%M")
    pauseItem = {
        "start": timeString,
    }
    newPause = data.Pause(pauseItem)
    return newPause


def newWork():
    timeString = datetime.now().strftime("%H:%M")
    return data.Work(timeString)
