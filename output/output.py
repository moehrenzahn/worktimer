# -*- coding: utf-8 -*-
from data import formatter
import elements


def status(days):
    if days.isTimer():
        today = days.getToday()
        print formatter.format_delta(today.getRemainingWork())
        print "Work time " + formatter.format_delta(today.getCurrentWork())
        print "Remaining " + formatter.format_delta(today.getRemainingWork())
        print "Pause: " + formatter.format_delta(today.getPausetime())
        print "Start: " + today.getStartTime().strftime("%H:%M") + " Uhr"
        print "End: " + (today.getEndTime()).strftime("%H:%M") + " Uhr"
        print elements.spacer()
    else:
        print "Free"

    print "Current Overtime: " + formatter.format_delta(days.getOvertime())
    print elements.spacer()
    if days.isTimer():
        print elements.button("Timer beenden")
    else:
        print elements.button("Timer starten")
    print elements.button("Log anzeigen")
    print elements.button("Exportieren")
