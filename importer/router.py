import importer


# Check if a given json string is in legacy format
def getDays(json):

    # could be an array or dict
    if isinstance(json, list):
        element = json[0]
    elif isinstance(json, dict):
        element = json.itervalues().next()

    if 'start' in element:
        factory = importer.LegacyDaysFactory(json)
    elif 'work' in element:
        factory = importer.DaysFactory(json)
    else:
        raise ValueError('Could not determine type of json file')
    return factory.create()
