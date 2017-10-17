import importer


# Check if a given json string is in legacy format
def getDays(json):
    if type(json[1]) is dict:
        return importer.DaysFactory(json)
    else:
        return importer.LegacyDaysFactory(json)
