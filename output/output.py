# -*- coding: utf-8 -*-
from data import formatter
import elements


def status(days):
    __info(days)
    print elements.spacer()
    __actions(days)


def __info(days):
    if days.isTimer():
        today = days.getToday()
        if days.isPause():
            print "Pause: " + formatter.format_delta(today.getPausetime())
        else:
            print formatter.format_delta(today.getRemainingWork())
        print "Worked " + formatter.format_delta(today.getCurrentWork())
        print "Remaining: " + formatter.format_delta(today.getRemainingWork())
        print "Pause: " + formatter.format_delta(today.getPausetime())
        print "Start: " + today.getStartTime().strftime("%H:%M")
        print "End: " + (today.getEndTime()).strftime("%H:%M")
        print elements.spacer()
    else:
        print "Free"
    print "Total Overtime: " + formatter.format_delta(days.getOvertime())


def __actions(days):
    if days.isPause():
        print elements.button("Stop Pause")
    elif days.isTimer():
        print elements.button("Stop Timer")
        print elements.button("Start Pause")
    else:
        print elements.button("Start Timer")
    print elements.spacer()
    print elements.button("Open Log")
    print elements.button("Export")
