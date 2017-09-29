import json


def load(file):
    data = open(file, 'r')
    jsonData = json.load(data)
    data.close()
    return jsonData
