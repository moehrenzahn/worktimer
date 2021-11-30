#!/usr/bin/python

import sys
import config
import storage
import actions
import output
import importer


__version__ = "2.2.0"

def main():
    
    try:
        commands = []
        for argument in sys.argv[1:]:
            if argument.startswith('-'):
                keyAndValue = argument.split('=')
                key = keyAndValue[0].strip().lstrip('-')
                if key == 'help':
                    commands.insert(0, 'help')
                if len(keyAndValue) > 1:
                    value = keyAndValue[1].strip()
                    if value == 'false':
                        config.overrides[key] = False
                    elif value == 'true':
                        config.overrides[key] = True
                    else:
                        config.overrides[key] = value
            else:
                commands.append(argument.strip())
        
        daysData = storage.yaml.load(config.log_path())
        days = importer.getDays(daysData)

        if not commands:
            output.status(days)
        elif commands[0] == 'timer':
            if len(commands) > 1:
                actions.timer(days, commands[1])
            else:
                actions.timer(days)
        elif commands[0] == 'update':
            if len(commands) > 1:
                actions.change(days, commands[1])
        elif commands[0] == 'pause':
            actions.pause(days)
        elif commands[0] == 'log':
            actions.log()
        elif commands[0] == 'export':
                actions.export(days)
        elif commands[0] == 'report':
            if len(commands) > 1 and commands[1] == 'text':
                actions.export(days)
            elif len(commands) > 1 and commands[1] == 'ods':
                actions.report.export_ods(days)
            else:
                actions.report.export_excel(days)
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
            print("")
            print("Usage: run worktimer.py to display current timer stats.")
            print("   Use param 'timer [category]' to start or stop timer")
            print("   Use param 'update [category]' to change the currently tracked category")
            print("   Use param 'pause' to start or stop pause")
            print("   Use param 'sync' to attempt synchronisation with remote repository")
            print("   Use param 'log' to open the log file in default editor")
            print("   Use param 'export' to export your log to a human-readable text file")
            print("   Use param 'report' to create a work report spreadsheet")
            print("      'report excel --xlsx_template='template.xlsx'' for Excel")
            print("      'report ods --ods_template='template.ods'' for Open Document")
            print("   Use param 'import [file]' to import a log into your existing database")
            print("")
            print("Options (see config_default.json) for complete list:")
            print("   --hours_per_day=8")
            print("   --log=path/to/your/work/log")
            print("   --sync_automatically=false")
            return 2
        return 0
    except ValueError as e:
        output.notification('Critical Error', str(e))
        return 1
