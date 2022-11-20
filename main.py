"""
Entry point into this project.
"""
import datetime

import daily_tracker.form
import daily_tracker.scheduler


def create_form(at_datetime: datetime.datetime) -> None:
    """
    Launch the tracker.
    """
    # TODO: Instead of `datetime.now()`, this should use the next scheduled time
    daily_tracker.form.TrackerForm(at_datetime)


def main() -> None:
    """
    Entry point into this project.
    """
    scheduler = daily_tracker.scheduler.IndefiniteScheduler(create_form)
    scheduler.schedule_first()

    # create_form()


if __name__ == "__main__":
    main()
