import subprocess
import config


def log():
    subprocess.call(["open", config.log_path()])
