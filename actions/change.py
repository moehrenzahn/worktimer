import storage
import output

def change(days, category):
    today = days.getToday()
    if today:
        lastWork = today.getLastWork()
        if lastWork:
            if lastWork.category == category:
                output.notification(
                    "Category not updated",
                    "Last category already set to %s" % output.formatter.format_category(category)
                )
            else:
                lastWork.category = category;
                storage.yaml.save(days)
                output.notification(
                    "Category updated",
                    "Work category retroactively changed to %s" % output.formatter.format_category(category)
                )
            return

    output.notification(
        "Category not updated",
        "There is no logged work to update today"
    )
