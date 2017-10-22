#!/usr/bin/python
# -*- coding: utf-8 -*-

# React to TextBar action triggers
# https://github.com/richie5um/TextBar

import os
import subprocess
import actions
import config
import storage
import data
import importer

index = os.getenv('TEXTBAR_INDEX', '')
action = os.getenv('TEXTBAR_TEXT', '').lower()


if 'timer' in action:
    json = storage.load(config.log_path)
    days = importer.getDays(json)
    actions.timer(days)
if 'pause' in action:
    json = storage.load(config.log_path)
    days = importer.getDays(json)
    actions.pause(days)
if 'log' in action:
    subprocess.call(["open", config.log_path])
if 'export' in action:
    data.export()
    subprocess.call(["open", config.export_path])
