import os


def message(recipient, text):
    script = 'tell application "Messages" to send "{0}" to buddy "{1}" of (service 1 whose service type is iMessage)'.format(text, recipient)
    os.system("osascript -e '%s'" % script)
