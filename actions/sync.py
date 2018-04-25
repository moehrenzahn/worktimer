import subprocess
import config
import os


def syncUp():
    init()
    parts = config.log_path.split('/')
    file = parts.pop()
    path = '/'.join(parts)
    commands = [
        'cd ' + path,
        'git add ' + file,
        'git commit -m "Update WorkTimer data" >> /dev/null',
        'git push origin ' + config.syncRepoBranch + ' --quiet >> /dev/null',
    ]
    doCommands(commands)


def syncDown():
    init()
    parts = config.log_path.split('/')
    parts.pop()
    path = '/'.join(parts)
    commands = [
        'cd ' + path,
        'git pull origin ' + config.syncRepoBranch + ' --quiet >> /dev/null',
    ]
    doCommands(commands)


def init():
    if not config.syncRepoUrl:
        print "No sync_reop_url set. Aborting."
        exit(2)
    parts = config.log_path.split('/')
    filename = parts.pop()
    directory = '/'.join(parts)

    if not hasRepo(directory):
        createRepo(
            directory,
            filename,
            config.syncRepoUrl,
            config.syncRepoBranch
        )


def hasRepo(path):
    return ('.git' in os.listdir(path))


def createRepo(path, file, repo, branch):
    commands = [
        'cd ' + path,
        'git init',
        'git add ' + file,
        'git commit -m "Create WorkTimer data repository" >> /dev/null',
        'git remote add origin ' + repo + ' >> /dev/null',
        'git push -u origin ' + branch + ' >> /dev/null',
    ]
    doCommands(commands)


def doCommands(commands):
    try:
        subprocess.call(' && '.join(commands), shell=True)
    except:
        print "Could not sync with remote repository."
