import config
from berechnung_feiertage import Holidays
from datetime import date, timedelta
from data import Days, Day, formatter

def process(days: Days, bundesland: str):
    firstDay = days.days[0].date
    lastDay = days.days[-1].date
    holidayDates = _getAllHolidays(firstDay, lastDay, bundesland)
    saxonHolidayDates = _getAllHolidays(firstDay, lastDay, "SN")

    effectOnOvertime = timedelta(seconds=0)

    workedOnHolidays = _getWorkedOnHolidays(days, holidayDates)
    if workedOnHolidays:
        print("⚠️ Entries on "+bundesland+" holidays that require 'goal: 0:00':")
        for day in workedOnHolidays:
            effectOnOvertime += day.goal
            print(str(day.date) + " (" + formatter.format_delta(day.goal) + ")")
    
    workedOnWeekendDays = _getWorkedOnWeekendDays(days)
    if workedOnWeekendDays:
        print("⚠️ Entries on weekends that require 'goal: 0:00':")
        for day in workedOnWeekendDays:
            effectOnOvertime += day.goal
            print(str(day.date) + " (" + formatter.format_delta(day.goal) + ")")

    notWorkedOnHolidays = _getNotWorkedOnHolidays(days, saxonHolidayDates) 
    notWorkedOnHolidays = list(filter(lambda date: date not in holidayDates, notWorkedOnHolidays))
    if notWorkedOnHolidays:
        print("⚠️ Entries missing for non-"+bundesland+" holiday that require 'goal: "+str(config.hoursPerDay())+":00':")
        for date in notWorkedOnHolidays:
            effectOnOvertime -= timedelta(hours=config.hoursPerDay())
            print(str(date))
    
    if effectOnOvertime.seconds > 0:
        print("⚠️ Effect on overtime: "+str(formatter.format_delta(effectOnOvertime)))

def _is_weekend(date: date) -> bool:
    if date.weekday() < 5:
        return False
    else:
        return True
    
def _getNotWorkedOnHolidays(days: Days, holidayDates: list[date]) -> list[date]:
    result = []
    for holidayDate in holidayDates:
        holidayMatch = False
        for day in days.days:
            if day.date == holidayDate:
                holidayMatch = True
                break
        if holidayMatch is False:
            result.append(holidayDate)
    return result

def _getWorkedOnHolidays(days: Days, holidayDates: list[date]) -> list[Day]:
    result = []
    for day in days.days:
        for holidayDate in holidayDates:
            if day.date == holidayDate and str(day.goal) != "0:00:00":
                result.append(day)
    return result
def _getWorkedOnWeekendDays(days: Days) -> list[Day]:
    result = []
    for day in days.days:
        if _is_weekend(day.date) and str(day.goal) != "0:00:00":
            result.append(day)
    return result

def _getAllHolidays(fromDate: date, toDate: date, stateCode: str) -> list[date]:
    result = []

    iterationYear = fromDate.year
    while iterationYear <= toDate.year:
        holidaysObj = Holidays(iterationYear, stateCode)
        result.extend(list(map(lambda i: i[0], holidaysObj.get_holiday_list())))
        iterationYear = iterationYear + 1

    
    result = list(filter(lambda date: date <= toDate, result))
    result = list(filter(lambda date: date >= fromDate, result))
    result = list(filter(lambda date: not _is_weekend(date), result))

    return result
