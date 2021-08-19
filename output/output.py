from data import formatter
import config
import output.elements as elements


def status(days):
    __info(days)
    if config.textbar:
        print(elements.spacer())
        __actions(days)


def __info(days):
    if days.isTimer():
        today = days.getToday()
        if days.isPause():
            print("Pause: %s" % formatter.format_delta(today.getPausetime()))
        else:
            print("%s %s" % (formatter.format_delta(today.getRemainingWork()), formatter.format_category(today.getLastCategory())))

        print("Worked %s" % formatter.format_delta(today.getCurrentWork()))
        print("Remaining: %s" % formatter.format_delta(today.getRemainingWork()))
        print("Pause: %s" % formatter.format_delta(today.getPausetime()))
        print("Start: %s" % today.getStartTime().strftime("%H:%M"))
        print("End: %s" % (today.getEndTime()).strftime("%H:%M"))
        if config.textbar:
            print(elements.spacer())
    else:
        print("Free")
    print("Total Overtime: %s" % formatter.format_delta(days.getOvertime()))


def __actions(days):
    if days.isPause():
        print(elements.button("☕️ Stop Pause"))
    elif days.isTimer():
        print(elements.button("☕️ Start Pause"))
        print(elements.button("⏰ Stop Timer"))
    else:
        print(elements.button("⏰ Start Timer"))
    print(elements.spacer())
    if not days.isPause():
        if days.isTimer():
            print("Switch Category:")
        else:
            print("Start Category:")
        for key, description in config.categories.items():
            print(elements.button("⏰ %s Timer" % formatter.format_category(key)))
        print(elements.spacer())
    print(elements.button("Open Log"))
    print(elements.button("Export"))
