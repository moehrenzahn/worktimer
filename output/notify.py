import os
import config


def notification(head, text):
    if config.notifications:
        script = "osascript -e 'display notification \"%s\" with title \"%s\"'" % (text, head)
        os.system(script)
    else:
        print head + ": " + text
