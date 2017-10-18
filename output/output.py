# -*- coding: utf-8 -*-
from data import formatter
import elements


def status(days):
    if days.isTimer():
        today = days.getToday()
        if days.isPause():
            print "Pause: " + formatter.format_delta(days.isPause())
        else:
            print formatter.format_delta(today.getRemainingWork())
        print "Work time " + formatter.format_delta(today.getCurrentWork())
        print "Remaining " + formatter.format_delta(today.getRemainingWork())
        if not days.isPause():
            print "Pause: " + formatter.format_delta(today.getPausetime())
        print "Start: " + today.getStartTime().strftime("%H:%M") + " Uhr"
        print "End: " + (today.getEndtime()).strftime("%H:%M") + " Uhr"
        print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    else:
        print "Free"

    print "Current Overtime: " + formatter.format_delta(days.getOvertime())
    print elements.spacer()
    if days.isTimer():
        if days.isPause():
            print elements.button("Pause beenden")
        else:
            print elements.button("Pause starten")
            print elements.button("Timer beenden")
    else:
        print elements.button("Timer starten")
    print elements.button("Log anzeigen")
    print elements.button("Exportieren")
