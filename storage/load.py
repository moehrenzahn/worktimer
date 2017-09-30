import json


def load(file):
    try:
        data = open(file, 'r')
        jsonData = json.load(data)
        data.close()
        return jsonData
    except ValueError as e:
        print "Parsing Error"
        print e
        exit(2)
