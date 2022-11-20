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
    scheduler = daily_tracker.scheduler.IndefiniteScheduler(create_form)
    scheduler.schedule_first()


if __name__ == "__main__":
    main()
