#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
from storage import load
import output
from data import Days


json = load.load(config.log_path)
days = Days(json)

if days.today:
    timer = 1
else:
    timer = 0

state = State(
    timer,
    days.today.pause,
    days.today.startTime,
    days.today.remainingTime,
    days.today.currentTime,
    days.today.pauseTime,
    days.overtime)

output.status(state)
