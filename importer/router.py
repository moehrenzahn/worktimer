import importer


# Check format of a given json string
def getDays(json):
    if not json:
        # empty json
        factory = importer.DaysFactory(json)
    else:
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
