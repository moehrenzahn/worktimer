from datetime import timedelta


def format_timedelta(td):
    if td < timedelta(0):
        return '-' + format_timedelta(-td)
    else:
        s = td.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        minutes = str(minutes).zfill(2)
        return '' + '%s:%s' % (hours, minutes)
