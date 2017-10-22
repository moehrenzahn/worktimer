import os
import json


def load(file):
    # make sure file exists
    open(file, 'a')
    # return empty array if file is empty
    if os.stat(file).st_size == 0:
        return []
    data = open(file, 'r')
    jsonData = json.load(data)
    data.close()
    return jsonData
