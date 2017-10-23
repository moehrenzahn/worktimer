import os
import storage


dir_path = os.path.dirname(os.path.realpath(__file__))


def getConfigValue(s):
    if s in userConfig:
        return userConfig[s]
    elif s in defaultConfig:
        return defaultConfig[s]
    else:
        raise ValueError('Config value %s missing' % s)


def readConfig(f):
    try:
        return storage.load(f)
    except IOError:
        return []


defaultConfig = readConfig(dir_path + '/config_default.json')
userConfig = readConfig(dir_path + '/config.json')

# File name of main json data store
log = getConfigValue('log')
# File name of txt for exporting
export = getConfigValue('export')
# Print notices to macOS notification center as well as shell
notifications = getConfigValue('notifications')
# Send an iMessage to a contact when ending a timer
imessage = getConfigValue('imessage')
imessage_address = getConfigValue('imessage_address')
imessage_text = getConfigValue('imessage_text')

log_path = dir_path + "/" + log
export_path = dir_path + '/' + export
