#!/usr/bin/python

import subprocess
import os
import sys
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

if timerRunning :

	logType = "end"

	print "Checking for Timer"
	applescript = """
	display dialog "Willst du wirklich Feierabend machen? Lauft eventuell noch ein Timer?" with title "Beende Arbeitsprogramme" buttons {"Abbrechen", "Feierabend"} default button 1
	if button returned of result = "Abbrechen" then
	return 1
	else if button returned of result = "Feierabend" then
	return 2
	end if
	"""

	timer = subprocess.Popen("osascript -e '{0}'".format(applescript), shell=True, stdout=subprocess.PIPE)
	timer = timer.stdout.read().rstrip()
	if timer == "1":
		sys.exit()


	os.system("""
              osascript -e 'display notification "Beende Timer" with title "Feierabend"'
              """)
	print "Messaging ***REMOVED***"
	os.system("""
			  osascript -e 'tell application "Messages" to send "Mache jetzt Feierabend." to buddy "***REMOVED***" of (service 1 whose service type is iMessage)'
			  """)
else :
	logType = "start"
	os.system("""
              osascript -e 'display notification "Starte Arbeitszeit" with title "Auf Arbeit"'
              """)

print "Logging"
logDate = datetime.now().strftime("%Y-%m-%d")
logTime = datetime.now().strftime("%H:%M")

if logDate in jsonContents :
	jsonContents[logDate]["date"] = logDate
	jsonContents[logDate][logType] = logTime
else :
	jsonContents[logDate] = {logType : logTime}
jsonLog = open(logging, 'w')
json.dump(jsonContents, jsonLog, sort_keys=True, indent=4)
jsonLog.close()