import config
from data import formatter
from output.ask import ask
import storage
import output
import sys
import subprocess

def change(days, category, summary = ""):
    today = days.getToday()
    if today:
        lastWork = today.getLastWork()
        if not category and not summary:
            output.notification(
                "Nothing updated",
                "No category and no summary specified"
            )
        elif lastWork:
            updatedCategory = False
            if category:
                updatedCategory = category != lastWork.category
                lastWork.category = category

            updatedSummary = False
            if summary:
                if summary == "ASK" and config.textbar():
                    try:
                        summary = ask(title="Update Task",
                                      message=f"Update task summary ({formatter.format_category(lastWork.category)})", 
                                      default=lastWork.summary)
                    except subprocess.CalledProcessError:
                        output.notification(
                            "Nothing updated",
                            "Cancelled by user"
                        )
                        return
                updatedSummary = summary != lastWork.summary
                lastWork.summary = summary

            if updatedCategory:
                storage.yaml.save(days)
                if updatedSummary:
                    output.notification(
                        "Summary and Category updated",
                        "Summary retroactively set to %s, category to %s" % (summary, output.formatter.format_category(category))
                    )
                else:
                    output.notification(
                        "Category updated",
                        "Work category retroactively changed to %s" % output.formatter.format_category(category)
                    )
            elif updatedSummary:
                storage.yaml.save(days)
                output.notification(
                    "Summary updated",
                    "Summary retroactively set to %s" % summary
                )
            else:
                output.notification(
                    "Category/Summary not updated",
                    "Last category already set to %s" % output.formatter.format_category(category)
                )

            return

    output.notification(
        "Category/Summary not updated",
        "There is no logged work to update today"
    )
