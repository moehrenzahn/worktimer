import config
import os


def notification(head, text):
    print(head + ": " + text)
    if config.notifications():
        head = head.replace("'", "").replace("\"", "")
        script = "osascript -e \'display notification \"%s\" with title \"%s\"\'" % (text, head)
        result = os.system(script)
        if result > 0:
            print("Warning: Could not send system notification")
