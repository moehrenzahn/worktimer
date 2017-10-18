import importer


# Check if a given json string is in legacy format
def getDays(json):
    if 'start' in json[0]:
        return importer.LegacyDaysFactory(json)
    elif 'work' in json[0]:
        return importer.DaysFactory(json)        
    else:
        print 'Critical Error: Could not determine type of json file'
        exit(2)
