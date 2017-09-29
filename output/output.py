import formatter


def status(state):
    if state.timer:
        if state.pause:
            print "Pause: " + format_timedelta(state.runningPauseTime)
        else:
            print format_timedelta(state.remainingWorkTime)
        print "Arbeitszeit " + format_timedelta(state.currentWorkTime)
        print "Noch " + format_timedelta(state.remainingWorkTime)
        if not state.pause:
            print "Pause: " + format_timedelta(state.todayPause)
        print "Beginn: " + state.todayStartTime.strftime("%H:%M") + " Uhr"
        print "Ende: " + (state.todayStartTime + state.todayPause + state.todaySoll).strftime("%H:%M") + " Uhr"
        print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    else:
        print "Frei"

    print "Akt. Überstunden: " + format_timedelta(state.overtime)
    print "<html><span style='font-size:3pt'>&nbsp;</span></html>"
    if state.pause:
        print "<html><span style='font-size:11pt'>Pause beenden</span></html>"
    else:
        if state.timer:
            print "<html><span style='font-size:11pt'>Pause starten</span></html>"
    if state.timer:
        print "<html><span style='font-size:11pt'>Timer beenden</span></html>"
    else:
        print "<html><span style='font-size:11pt'>Timer starten</span></html>"
    print "<html><span style='font-size:11pt'>Log anzeigen</span></html>"
    print "<html><span style='font-size:11pt'>Exportieren</span></html>"

def format_timedelta():
