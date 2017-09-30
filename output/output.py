# -*- coding: utf-8 -*-
from data import formatter


def status(state):
    if state.isTimer:
        if state.isPause:
            print "Pause: " + formatter.format_delta(state.isPause)
        else:
            print formatter.format_delta(state.remainingWork)
        print "Arbeitszeit " + formatter.format_delta(state.currentWork)
        print "Noch " + formatter.format_delta(state.remainingWork)
        if not state.isPause:
            print "Pause: " + formatter.format_delta(state.pause)
        print "Beginn: " + state.start.strftime("%H:%M") + " Uhr"
        print "Ende: " + (
            state.start + state.pause + state.goal
        ).strftime("%H:%M") + " Uhr"
        print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    else:
        print "Frei"

    print "Akt. Überstunden: " + formatter.format_delta(state.overtime)
    print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    if state.isTimer:
        if state.isPause:
            print "<html><span style='font-size:11pt'>Pause beenden</span></html>"
        else:
            print "<html><span style='font-size:11pt'>Pause starten</span></html>"
            print "<html><span style='font-size:11pt'>Timer beenden</span></html>"
    else:
        print "<html><span style='font-size:11pt'>Timer starten</span></html>"
    print "<html><span style='font-size:11pt'>Log anzeigen</span></html>"
    print "<html><span style='font-size:11pt'>Exportieren</span></html>"
