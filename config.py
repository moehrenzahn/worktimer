import os


# name of data storage file 
log = "work.json"
# Print notices to macOS notification center instead of shell
notifications = 1
dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = dir_path + "/" + log
