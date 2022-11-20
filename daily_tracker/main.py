"""
Connect the various subpackages throughout the project to couple up the objects.
"""
import datetime
import pathlib

import daily_tracker.form
import daily_tracker.scheduler
import daily_tracker.handlers


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
    daily_tracker.form.TrackerForm(at_datetime)


def main() -> None:
    """
    Entry point into this project.
    """
    if APPLICATION_CREATED:
        scheduler = daily_tracker.scheduler.IndefiniteScheduler(create_form)
        scheduler.schedule_first()
    else:
        create_env()
        db_handler = daily_tracker.handlers.DatabaseHandler("tracker.db")
        db_handler.import_history("daily-tracker-data.csv")
