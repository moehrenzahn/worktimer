import os
import shutil
import subprocess
import sys


def ask(title, message, default=""):
    if sys.platform != "darwin" or shutil.which("osascript") is None:
        print("osascript not available")
        return default
    result = subprocess.run(
        [
            "osascript",
            "-e",
            f'text returned of (display dialog "{message}" with title "{title}" default answer "{default}")'
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()