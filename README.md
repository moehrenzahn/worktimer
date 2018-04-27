# WorkTimer

**A python CLI script for monitoring and logging work and break times.**

*By Max Melzer ([moehrenzahn.de](https://moehrenzahn.de/))*

WorkTimer optionally integrates with macOS Notification Center, Message.app, and the [TextBar app by Rich Somerfield](http://richsomerfield.com/apps/textbar/)

## Requirements

- Python 2.7.10 or newer
- Optional:
    + macOS with configured Messages app
    + [TextBar](http://richsomerfield.com/apps/textbar/)

## Installation and Usage

Clone the repo into a directory of your choosing and `cd` into the directory:

```bash
git clone https://github.com/moehrenzahn/worktimer.git
cd worktimer
```

You can start a new timer with `python worktimer.py timer`. Then, monitor your progress with `python worktimer.py`. Use `python worktimer.py pause` to start a break or `python worktimer.py timer` to stop the timer.

Get a list of all avaliable command line options with `python worktimer.py --help`.

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


## Configuration

Create a new file in the worktimer root directory named `config.json`. In this file you can override any setting found in `config_default.json` by mimicing the default json structure.

## iMessage integration

On macOS, you can configure WorkTimer to send a custom iMessage to someone whenever you stop a timer. You could use this feature to nofify your spouse that you'll be home soon. :)

## Syncronization (experimental)

To sync your work times between machines, you will need a Git repository to store your json file and add it's path to your config file. If there is a problem with the repository, WorkTimer will output the Git info to the console. Please have a backup in case anything bad happens.

## Usage with TextBar

Configure `python ~/worktimer/worktimer.py` as script and `python ~/worktimer/textBarAction.py` as action script in the TextBar preferences. A refresh rate of 15 seconds is recommended.

Make sure to set `textbar` to `true` in your `config.json` to make full use of TextBar:

```bash
python worktimer.py
6:08
Worked 1:51
Remaining: 6:08
Pause: 0:15
Start: 08:05
End: 16:20
Total Overtime: 1:21
<html><span style='font-size:3pt'>&nbsp;</span></html>
Total Overtime: -5:21
<html><span style='font-size:3pt'>&nbsp;</span></html>
<html><span style='font-size:11pt'>Stop Timer</span></html>
<html><span style='font-size:11pt'>Start Pause</span></html>
<html><span style='font-size:3pt'>&nbsp;</span></html>
<html><span style='font-size:11pt'>Open Log</span></html>
<html><span style='font-size:11pt'>Export</span></html>
```

*Copyright 2017 Max Melzer. Published under MIT License. See `LICENSE` file for details.*