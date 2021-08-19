#!python3

# React to TextBar action triggers
# https://github.com/richie5um/TextBar

import os
import actions
import config
import storage
import importer
import output

try:
    index = os.getenv('TEXTBAR_INDEX', '')
    action = os.getenv('TEXTBAR_TEXT', '').lower()

    json = storage.load(config.log_path)
    days = importer.getDays(json)

    if 'timer' in action:
        for key, description in config.categories.items():
            if description.lower() in action:
                actions.timer(days, key)
                exit(0)
        actions.timer(days)
    if 'pause' in action:
        actions.pause(days)
    if 'log' in action:
        actions.log()
    if 'export' in action:
        actions.export(days)
except ValueError as e:
        output.notification('Critical Error', str(e))
        exit(2)