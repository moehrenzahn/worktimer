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

*Copyright 2017 Max Melzer*

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.