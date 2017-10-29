import importer
import storage
import data


def add(file, days):
    """
        file: string
        days: [Day]
    """
    json = storage.load(file)
    newDayList = importer.getDays(json).days
    oldDayList = days.days
    # check for duplicate days
    for oldDay in oldDayList:
        for newDay in newDayList:
            if oldDay.date == newDay.date:
                oldDay.work = oldDay.work + newDay.work
                newDayList.remove(newDay)
    newDays = data.Days(oldDayList + newDayList)
    storage.save(newDays)
