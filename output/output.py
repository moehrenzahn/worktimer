from data import formatter
import config
from data.days import Days
import output.elements as elements


def status(days: Days):
    __info(days)
    if config.textbar():
        print(elements.spacer())
        __actions(days)


def __info(days: Days):
    if days.isTimer():
        today = days.getToday()
        if days.isPause():
            print("Pause: %s" % formatter.format_delta(today.getPausetime()))
        else:
            print('%s – %s %s %s' % (formatter.format_delta(today.getRemainingWork()),
                                formatter.format_category(today.getLastWork().category),
                                today.getLastWork().summary,
                                formatter.format_delta(today.getLastWork().getDuration())
            ))
    else:
        print("Free")
    
    if config.textbar():
        print('---')

    if days.isTimer():
        if config.textbar():
            print(elements.menu(
                "Worked %s" % formatter.format_delta(today.getCurrentWork()),
                map(
                    lambda x: "%s %s: %s" % (
                        formatter.format_delta(x.getDuration()),
                        formatter.format_category(x.category),
                        x.summary if x.summary else "No summary"
                    ),
                    today.work
                )
            ))
        else:
            print("Worked %s" % formatter.format_delta(today.getCurrentWork()))

        print("Remaining: %s" % formatter.format_delta(today.getRemainingWork()))
        print("Pause: %s" % formatter.format_delta(today.getPausetime()))
        print("Start: %s" % today.getStartTime().strftime("%H:%M"))
        print("End: %s" % (today.getEndTime()).strftime("%H:%M"))
        if config.textbar():
            print(elements.spacer())
    
    print("Total Overtime: %s" % formatter.format_delta(days.getOvertime()))


def __actions(days: Days):
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
        for key, description in config.categories().items():
            menuItems.append(
                elements.button(
                    description,
                    'timer %s' % key
                )
            )
        print(elements.menu("🚀 Start Category", menuItems))

        if days.getToday():

            menuItems = []
            for key, description in config.categories().items():
                menuItems.append(
                    elements.button(
                        description,
                        'update ' + key
                    )
                )
            print(elements.menu("⚙️ Update Category", menuItems))
            
            # Collect recently used summaries for the current category
            menuItems = []
            for summary in days.getRecentSummaries(category=days.getToday().getLastCategory()):
                menuItems.append(
                    elements.button("\""+summary+"\"", 'update %s %s' % (days.getToday().getLastCategory(), summary))
                ) 
            menuItems.append(
                elements.button("New …", 'update %s ASK' % days.getToday().getLastCategory())
            )
            print(elements.menu("💬 Update Summary", menuItems))
            
        print(elements.spacer())
    print(elements.button('Open Log', 'log'))
    print(elements.menu('Create Report', [
        elements.button('Excel', 'report excel'),
        elements.button('OpenDocument', 'report ods'),
        elements.button('Text', 'report text'),
    ]))
