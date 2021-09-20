import os
import storage

def _readConfig(f):
    try:
        return storage.load(f)
    except IOError:
        return []

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultConfig = _readConfig(dir_path + '/config_default.json')
userConfig = _readConfig(dir_path + '/config.json')
overrides = {}

# File name of main json data store
def log():
    return _getConfigValue('log') + ".json"

# File name of txt for exporting
def export():
    return _getConfigValue('export')

# Repository to sync worktimes to
def syncRepoUrl():
    return _getConfigValue('sync_repo_url')
def syncRepoBranch():
    return _getConfigValue('sync_repo_branch')
def autoSync():
    return _getConfigValue("sync_automatically")

# Print notices to macOS notification center as well as shell
def notifications():
    return _getConfigValue('notifications')

def hoursPerDay():
    return _getConfigValue('hours_per_day')

# Send an iMessage to a contact when ending a timer
def imessage():
    return _getConfigValue('imessage')
def imessage_address():
    return _getConfigValue('imessage_address')
def imessage_text():
    return _getConfigValue('imessage_text')

# TextBar mode (http://richsomerfield.com/apps/textbar/)
def textbar():
    return _getConfigValue('textbar')
def default_category():
    return _getConfigValue('default_category')
def categories():
    return _getConfigValue('categories')
def log_path():
    return dir_path + "/" + log()
def export_path():
    return dir_path + '/' + export()
def xlsx_template():
    return _getConfigValue('xlsx_template')
def ods_template():
    return _getConfigValue('ods_template')


def _getConfigValue(s):
    if s in overrides:
        return overrides[s]
    if s in userConfig:
        return userConfig[s]
    elif s in defaultConfig:
        return defaultConfig[s]
    else:
        raise ValueError('Config value %s missing' % s)
