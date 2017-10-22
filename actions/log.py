import subprocess
import config


def openLog():
    subprocess.call(["open", config.log_path])
