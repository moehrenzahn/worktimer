#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import config
import storage
import actions
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
        output.notification(
            "Timer not stopped",
            "Please end pause before ending timer"
        )
        exit(2)
    if timer:
        actions.timerStop(days)
        output.notification(
            "Work timer stopped",
            "Remember to stop any time tracking"
        )
    else:
        actions.timerStart(days)
        output.notification(
            "Work timer started",
            "You will have to work for %s." % days.today.goal
        )
elif sys.argv[1] == 'pause':
    if not timer:
        output.notification("Not paused", "Please start timer before pausing")
        exit(2)
    if state.isPause:
        actions.pauseStop(days)
        output.notification(
            "Break ended",
            "Full break time: %s." % days.today.pauses[-1].duration
        )
    else:
        actions.pauseStart(days)
        output.notification(
            "Break started",
            "Started break at %s." % days.today.pauses[-1].start
        )
else:
    print "WorkTimer by Max Melzer (moehrenzahn.de)"
    print "Usage: run main.py to display current stats."
    print "       Use param 'timer' to start or stop timer"
    print "       Use param 'pause' to start or stop pause"
    exit(2)
