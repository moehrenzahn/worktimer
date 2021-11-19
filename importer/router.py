import importer

# Check format of given data
def getDays(daysData):
    if not daysData:
        # empty daysData
        factory = importer.DaysFactory(daysData)
    else:
        # could be an array or dict
        if isinstance(daysData, list):
            element = daysData[0]
        elif isinstance(daysData, dict):
            element = daysData[next(iter(daysData))]
        if 'start' in element:
            factory = importer.LegacyDaysFactory(daysData)
        elif 'work' in element:
            factory = importer.DaysFactory(daysData)
        else:
            raise ValueError('Could not determine type of log file')
    return factory.create()
