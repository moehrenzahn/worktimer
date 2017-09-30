from datetime import datetime
import data


def newDay():
    dateString = datetime.now().strftime("%Y-%m-%d")
    timeString = datetime.now().strftime("%H:%M")
    day = {
        "date": dateString,
        "start": timeString
    }
    newDay = data.Today(day, dateString)
    return newDay
