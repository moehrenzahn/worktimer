#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import config
import storage
import output
import data


json = storage.load(config.log_path)
days = data.Days(json)

if hasattr(days, "today") and not hasattr(days.today, "end"):
    timer = 1
    state = data.State(
        timer,
        days.overtime,
        days.today
    )
else:
    timer = 0
    state = data.State(
        timer,
        days.overtime
    )

args = sys.argv[1:]
if not args:
    output.status(state)
elif sys.argv[1] == 'timer':
    if timer and state.isPause:
        print("Please stop pause before ending timer")
        exit(2)
    if timer:
        days.getDay(datetime.now().date()).end = datetime.now().time()
        storage.save(days)
    else:
        today = data.newDay()
        days.days.append(today)
        storage.save(days)
elif sys.argv[1] == 'pause':
    print "toggling pause"
else:
    print "WorkTimer by Max Melzer (moehrenzahn.de)"
    print "Usage: run main.py to display current stats."
    print "       Use param 'timer' to start or stop timer"
    print "       Use param 'pause' to start or stop pause"
    exit(2)
