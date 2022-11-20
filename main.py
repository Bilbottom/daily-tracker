"""
Entry point into this project.
"""
import datetime

import daily_tracker.form
import daily_tracker.scheduler
import daily_tracker.handlers


def create_form(at_datetime: datetime.datetime) -> None:
    """
    Launch the tracker.
    """
    daily_tracker.form.TrackerForm(at_datetime)


def main() -> None:
    """
    Entry point into this project.
    """
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(create_form)
    # scheduler.schedule_first()

    db_handler = daily_tracker.handlers.DatabaseHandler("tracker.db")
    db_handler.import_history("daily-tracker-data.csv")


if __name__ == "__main__":
    main()
