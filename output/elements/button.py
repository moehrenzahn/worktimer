import sys

def button(text, action):
    params = list(action.split())
    paramsString = ''
    for idx, param in enumerate(params):
        paramsString += ' param%i=%s' % (idx + 1, param)
    return '%s | refresh=true | shell="%s"%s' % (text, sys.argv[0], paramsString)
