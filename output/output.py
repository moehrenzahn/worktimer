# -*- coding: utf-8 -*-
from data import formatter
import elements


def status(days):
    if days.isTimer():
        today = days.getToday()
        print formatter.format_delta(today.getRemainingWork())
        print "Work Time " + formatter.format_delta(today.getCurrentWork())
        print "Remaining " + formatter.format_delta(today.getRemainingWork())
        print "Pause: " + formatter.format_delta(today.getPausetime())
        print "Start: " + today.getStartTime().strftime("%H:%M")
        print "End: " + (today.getEndTime()).strftime("%H:%M")
        print elements.spacer()
    else:
        print "Free"

    print "Current Overtime: " + formatter.format_delta(days.getOvertime())
    print elements.spacer()
    if days.isTimer():
        print elements.button("Stop Timer")
        if days.isPause():
            print elements.button("Stop Pause")
        else:
            print elements.button("Stop Pause")
    else:
        print elements.button("Start Timer")
    print elements.spacer()
    print elements.button("Show Log")
    print elements.button("Export")
