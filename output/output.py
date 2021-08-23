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
    else:
        print("Free")
    
    if config.textbar:
        print('---')

    if days.isTimer():
        print("Worked %s" % formatter.format_delta(today.getCurrentWork()))
        print("Remaining: %s" % formatter.format_delta(today.getRemainingWork()))
        print("Pause: %s" % formatter.format_delta(today.getPausetime()))
        print("Start: %s" % today.getStartTime().strftime("%H:%M"))
        print("End: %s" % (today.getEndTime()).strftime("%H:%M"))
        if config.textbar:
            print(elements.spacer())
    
    print("Total Overtime: %s" % formatter.format_delta(days.getOvertime()))


def __actions(days):
    if days.isPause():
        print(elements.button("☕️ Stop Pause", 'pause'))
    elif days.isTimer():
        print(elements.button("☕️ Start Pause", 'pause'))
        print(elements.button("⏰ Stop Timer", 'timer'))
    else:
        print(elements.button("⏰ Start Timer", 'timer'))
    print(elements.spacer())
    if not days.isPause():
        menuItems = []
        if days.isTimer():
            menuTitle = 'Switch Category'
        else:
            menuTitle = "Start Category"
        for key, description in config.categories.items():
            menuItems.append(
                elements.button(
                    "⏰ %s" % description,
                    'timer ' + key
                )
            )

        print(elements.menu(menuTitle, menuItems))
        print(elements.spacer())
    print(elements.button('Open Log', 'log'))
    print(elements.button('Export', 'export'))
