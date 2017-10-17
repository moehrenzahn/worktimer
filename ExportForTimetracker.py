#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import json
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
jsonLog = open(dir_path + "/work.json", 'r')
json = json.load(jsonLog)
jsonLog.close()

# sort json
# print(json[dict.itervalues().next()]['date'])
# sorted(json, key=lambda day: day['date'])

exportString = ""
for day in json:

    starttime = json[day]["start"]
    dayDate = datetime.strptime(day, '%Y-%m-%d')
    # dayString = dayDate.strftime("%d.%m.%Y")
    dayString = dayDate.strftime("%Y-%m-%d")
    if "end" in json[day]:
        endtime = json[day]["end"]

    if "pause" not in json[day]:
        exportString += dayString + "   " + starttime   + "   Keine Pause   " + endtime + "\n\n"
        continue

    for (i, item) in enumerate(json[day]["pause"]):
        if i == 0:
            exportString += dayString + "   " + starttime   + "   " + json[day]["pause"][i]["start"] + "\n"
        else:
            exportString += dayString + "   " + json[day]["pause"][i-1]["end"] + "   " + json[day]["pause"][i]["start"] + "\n"

    exportString += dayString + "   " + json[day]["pause"][-1]["end"] + "   " + endtime + "\n\n"


dir_path = os.path.dirname(os.path.realpath(__file__))
exportLog = open(dir_path + "/exportLog.txt", 'w')
exportLog.write(exportString)
exportLog.close()
