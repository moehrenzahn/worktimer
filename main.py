#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import config
import storage
import actions
import output
import importer

__version__ = "1.0.0"


def main():
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
        elif sys.argv[1] == 'log':
            actions.log(days)
        else:
            print "WorkTimer " + __version__ + " by Max Melzer (moehrenzahn.de)"
            print "Usage: run worktimer.py to display current timer stats."
            print "   Use param 'timer' to start or stop timer"
            print "   Use param 'pause' to start or stop pause"
            print "   åUse param 'log' to open the log file in default editor"
            exit(2)
    except ValueError as e:
        output.notification('Critical Error', str(e))
        exit(2)
