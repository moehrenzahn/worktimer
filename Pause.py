#!/usr/bin/python

import subprocess
import os
import webbrowser
import datetime
from datetime import datetime
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
logging = dir_path + "/work.json"

# timer running?
timerRunning = 0
jsonLog = open(logging, 'r')
jsonContents = json.load(jsonLog)
jsonLog.close()
for day in jsonContents :
	if ( datetime.strptime(day, '%Y-%m-%d').date() == datetime.now().date() and
	"end" not in jsonContents[day] ) :
			timerRunning = 1

if not timerRunning :
	print "No Timer running!"
	exit()


logDate = datetime.now().strftime("%Y-%m-%d")
logTime = datetime.now().strftime("%H:%M")

if "pause" not in jsonContents[logDate]:
	# first break today
	jsonContents[logDate]["pause"] = []

print len(jsonContents[logDate]["pause"])

if  len(jsonContents[logDate]["pause"]) and "end" not in jsonContents[logDate]["pause"][-1] :
	# finishing break
	logType = "end"
	jsonContents[logDate]["pause"][-1][logType] = logTime
else :
	# starting second break
	logType = "start"
	jsonContents[logDate]["pause"].append( {logType : logTime} )
	
	


if logType == "end" :
	os.system("""
          osascript -e 'display notification "Pause" with title "Pause beendet"'
          """)
if logType == "start" :
	os.system("""
          osascript -e 'display notification "Pause" with title "Pause begonnen"'
          """)

print "Logging Break"
jsonLog = open(logging, 'w')
json.dump(jsonContents, jsonLog, sort_keys=True, indent=4)
jsonLog.close()


