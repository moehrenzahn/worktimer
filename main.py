#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import config
import storage
import actions
import output
import importer
import data
from datetime import datetime


json = storage.load(config.log_path)
days = importer.getDays(json)

args = sys.argv[1:]
if not args:
    output.status(days)
elif sys.argv[1] == 'timer':
    if days.isTimer():
        actions.timerStop(days)
        output.notification(
            "Work timer stopped",
            "Remember to stop any time tracking"
        )
    else:
        actions.timerStart(days)
        output.notification(
            "Work timer started",
            "You will have to work until %s" % data.formatter.format_time(days.getToday().getEndTime())
        )
elif sys.argv[1] == 'pause':
    if days.isPause():
        actions.pauseStop(days)
        output.notification(
            "Break ended",
            "Full break time: %s" % data.formatter.format_time(days.getToday().getPausetime())
        )
    else:
        actions.pauseStart(days)
        output.notification(
            "Break started",
            "Started break at %s" % data.formatter.format_time(days.getToday().getLastWork().end)
        )
else:
    print "WorkTimer by Max Melzer (moehrenzahn.de)"
    print "Usage: run main.py to display current stats."
    print "       Use param 'timer' to start or stop timer"
    print "       Use param 'pause' to start or stop pause"
    exit(2)
