import config
import json


def save(days):
    try:
        data = days.toJSON()
        json.dumps(data)
        file = open(config.log_path, 'w')
        file.write(data)
        file.close()
    except Exception as e:
        print "Save error"
        print e
        exit(2)
