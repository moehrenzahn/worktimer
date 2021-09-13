import os
import json
import io

def load(file):
    # return empty array if file is empty
    if os.stat(file).st_size == 0:
        os.remove(file)
        return []
    with io.open(file, 'r') as data:
        jsonData = json.load(data)
    return jsonData
