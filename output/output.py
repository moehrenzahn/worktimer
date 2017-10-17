# -*- coding: utf-8 -*-
from data import formatter


def status(days):
    today = days.getToday()
    if days.isTimer():
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
    print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    if days.isTimer():
        if days.isPause():
            print "<html><span style='font-size:11pt'>Pause beenden</span></html>"
        else:
            print "<html><span style='font-size:11pt'>Pause starten</span></html>"
            print "<html><span style='font-size:11pt'>Timer beenden</span></html>"
    else:
        print "<html><span style='font-size:11pt'>Timer starten</span></html>"
    print "<html><span style='font-size:11pt'>Log anzeigen</span></html>"
    print "<html><span style='font-size:11pt'>Exportieren</span></html>"
