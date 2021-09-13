#!/usr/bin/python

import sys
import config
import storage
import actions
import output
import importer


__version__ = "2.1.0"


def main():
    
    try:
        commands = []
        for argument in sys.argv[1:]:
            if argument.startswith('-'):
                keyAndValue = argument.split('=')
                key = keyAndValue[0].strip().lstrip('-')
                value = keyAndValue[1].strip()
                if value == 'false':
                    config.overrides[key] = False
                elif value == 'true':
                    config.overrides[key] = True
                else:
                    config.overrides[key] = value
            else:
                commands.append(argument.strip())
        
        json = storage.load(config.log_path())
        days = importer.getDays(json)

        if not commands:
            output.status(days)
        elif commands[0] == 'timer':
            if len(commands) > 1:
                actions.timer(days, commands[1])
            else:
                actions.timer(days)
        elif commands[0] == 'pause':
            actions.pause(days)
        elif commands[0] == 'log':
            actions.log()
        elif commands[0] == 'export':
            actions.export(days)
        elif commands[0] == 'import':
            if len(commands) > 1:
                actions.add(commands[1], days)
            else:
                print("No file to import given.")
        elif commands[0] == 'sync':
            actions.syncDown()
            actions.syncUp()
        else:
            print("WorkTimer " + __version__ + " by Max Melzer (moehrenzahn.de)")
            print("Usage: run worktimer.py to display current timer stats.")
            print("   Use param 'timer [category]' to start or stop timer")
            print("   Use param 'pause' to start or stop pause")
            print("   Use param 'sync' to attempt synchronisation with remote repository")
            print("   Use param 'log' to open the log file in default editor")
            print("   Use param 'export' to export the log in a human-readable format")
            print("   Use param 'import [file]' to import a json log into your existing database")
            return 2
        return 0
    except ValueError as e:
        output.notification('Critical Error', str(e))
        return 1
