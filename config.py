import os


# name of data storage file
log = "work.json"
# name of export file
export = 'work.txt'
# Print notices to macOS notification center as well as shell
notifications = 1
dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = dir_path + "/" + log
export_path = dir_path + '/' + export
