"""
Connect the various subpackages throughout the project to couple up the objects.
"""
import datetime

import daily_tracker.form
import daily_tracker.scheduler


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
