#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import config
import storage
import actions
import output
import importer


try:
    json = storage.load(config.log_path)
    days = importer.getDays(json)

    args = sys.argv[1:]
    if not args:
        output.status(days)
    elif sys.argv[1] == 'timer':
        actions.timer(days)
    elif sys.argv[1] == 'pause':
        actions.pause(days)
    else:
        print "WorkTimer by Max Melzer (moehrenzahn.de)"
        print "Usage: run main.py to display current stats."
        print "       Use param 'timer' to start or stop timer"
        print "       Use param 'pause' to start or stop pause"
        exit(2)
except ValueError as e:
    output.notification('Critical Error', str(e))
    exit(2)
