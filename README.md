# WorkTimer

**A python CLI script for monitoring and logging work and break times.**

*By Max Melzer ([moehrenzahn.de](https://moehrenzahn.de/))*

WorkTimer optionally integrates with macOS Notification Center, Message.app, and the [xBar app](https://github.com/matryer/xbar)

## Requirements

- Python 3
- Optional:
    - macOS with configured Messages app
    - [xBar](https://github.com/matryer/xbar)

## Installation and Usage

Clone the repo into a directory of your choosing and `cd` into the directory:

```bash
git clone https://github.com/moehrenzahn/worktimer.git
cd worktimer
```

You can start a new timer with `python worktimer.py timer [category]`. Then, monitor your progress with `python worktimer.py`. Use `python worktimer.py pause` to start and stop a break or `python worktimer.py timer` to stop a running timer.

Get a list of all available command line options with `python worktimer.py --help`.

Sample output:

```bash
python worktimer.py
6:08
Worked 1:51
Remaining: 6:08
Pause: 0:15
Start: 08:05
End: 16:20
Total Overtime: 1:21
```

## Testing

First, install test dependencies:

```bash
pip3 install freezegun
```

Run the suite of unit and integration tests using:

```bash
python3 -m unittest
```

## Configuration

Create a new file in the worktimer root directory named `config.json`. In this file you can override any setting found in `config_default.json` by mimicking the default json structure.

## iMessage integration

On macOS, you can configure WorkTimer to send a custom iMessage to someone whenever you stop a timer. You could use this feature to notify your spouse that you'll be home soon. :)

## Synchronization (experimental)

To sync your work times between machines, you will need a Git repository to store your yaml file and add it's path to your config file. If there is a problem with the repository, WorkTimer will output the Git info to the console.

When using automatic synching, don't start a session on two machines in parallel; and please have a backup in case anything bad happens.

## Usage with xBar

Create an alias to `WorkTimer.py` in your plugin folder and name it `worktimer.30s.py`

Make sure to set `textbar` to `true` in your `config.json` to make full use of xBar.

*Copyright 2017-2021 Max Melzer. Published under MIT License. See `LICENSE` file for details.*

## Credits

**berechnung_feiertage.py** von Stephan John und David (Pax90): https://github.com/Pax90/berechnung_feiertage/blob/master/berechnung_feiertage.py