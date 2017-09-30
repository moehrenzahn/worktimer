#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import json
import os


def format_timedelta(td):
    if td < timedelta(0):
        return '-' + format_timedelta(-td)
    else:
        s = td.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        minutes = str(minutes).zfill(2)
        return '' + '%s:%s' % (hours, minutes)


dir_path = os.path.dirname(os.path.realpath(__file__))
jsonLog = open(dir_path + "/work.json", 'r')
json = json.load(jsonLog)
jsonLog.close()
ueberstundenTotal = timedelta(seconds=0)
timerRunning = 0
pauseRunning = 0
isPauseEnd = 0
isPauseStart = 0

for day in json:

    # calc ÜbestundenTotal
    starttime = datetime.strptime(json[day]["start"], '%H:%M')
    if "halbtags" in json[day]:
        soll = timedelta(minutes=240)
    elif "zusatz" in json[day]:
        soll = timedelta(minutes=0)
    else:
        soll = timedelta(minutes=480)
    # calc pause
    if "pause" in json[day]:
        pause = timedelta(minutes=0)
        for item in json[day]["pause"]:
            if "start" in item and "end" in item:
                pauseStart = datetime.strptime(item["start"], '%H:%M')
                pauseEnd = datetime.strptime(item["end"], '%H:%M')
                pause += pauseEnd - pauseStart
    else:
        pause = timedelta(minutes=30)
    if "end" in json[day]:
        endtime = datetime.strptime(json[day]["end"], '%H:%M')
        delta = endtime - starttime
        ueberstunden = delta - pause - soll
        ueberstundenTotal += ueberstunden

    # calc timeRemaining

    if datetime.strptime(day, '%Y-%m-%d').date() == datetime.now().date():
        if "end" not in json[day]:
            timerRunning = 1
            todaySoll = soll
            todayStartTime = starttime
            todayPause = pause
            if "pause" in json[day]:
                if "start" in json[day]["pause"][-1]:
                    isPauseStart = 1
                if "end" in json[day]["pause"][-1]:
                    isPauseEnd = 1
                if isPauseStart and not isPauseEnd:
                    pauseRunning = 1
                    runningPauseTime = datetime.now() -  datetime.strptime(item["start"], '%H:%M')

            # todayUeberstunden = ueberstundenTotal
            todayStartDate = datetime.combine(datetime.strptime(day, '%Y-%m-%d').date(), todayStartTime.time())

            currentWorkTime = datetime.now() - todayStartDate
            remainingWorkTime = (todaySoll + todayPause) - currentWorkTime

if timerRunning:
    if pauseRunning:
        print "Pause: " + format_timedelta(runningPauseTime)
    else:
        print format_timedelta(remainingWorkTime)
    print "Arbeitszeit " + format_timedelta(currentWorkTime)
    print "Noch " + format_timedelta(remainingWorkTime)
    if not pauseRunning:
        print "Pause: " + format_timedelta(todayPause)
    print "Beginn: " + todayStartTime.strftime("%H:%M") + " Uhr"
    print "Ende: " + (todayStartTime + todayPause + todaySoll).strftime("%H:%M") + " Uhr"
    print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
else:
    print "Frei"


print "Akt. Überstunden: " + format_timedelta(ueberstundenTotal)
print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
if pauseRunning:
    print "<html><span style='font-size:11pt'>Pause beenden</span></html>"
else:
    if timerRunning:
        print "<html><span style='font-size:11pt'>Pause starten</span></html>"
if timerRunning:
    print "<html><span style='font-size:11pt'>Timer beenden</span></html>"
else:
    print "<html><span style='font-size:11pt'>Timer starten</span></html>"
print "<html><span style='font-size:11pt'>Log anzeigen</span></html>"
print "<html><span style='font-size:11pt'>Exportieren</span></html>"
