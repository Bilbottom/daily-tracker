"""
Connect the various subpackages throughout the project to couple up the objects.
"""
import datetime
import pathlib

import daily_tracker.core.form
import daily_tracker.core.scheduler
import daily_tracker.core.handlers


APPLICATION_CREATED = True


def create_env() -> None:
    """
    Create the .env file.
    """
    filepath = ".env"
    if pathlib.Path(filepath).exists():
        return None

    with open(filepath, "w+") as f:
        keys = ["JIRA_URL", "JIRA_KEY", "JIRA_SECRET", "SLACK_URL"]
        f.write("\n".join([f"{key}=" for key in keys]))


def create_form(at_datetime: datetime.datetime) -> None:
    """
    Launch the tracker.
    """
    daily_tracker.core.form.TrackerForm(at_datetime)


def main() -> None:
    """
    Entry point into this project.
    """
    if APPLICATION_CREATED:
        scheduler = daily_tracker.core.scheduler.IndefiniteScheduler(create_form)
        scheduler.schedule_first()
    else:
        create_env()
        db_handler = daily_tracker.core.handlers.DatabaseHandler("tracker.db")
        db_handler.import_history("daily-tracker-data.csv")
