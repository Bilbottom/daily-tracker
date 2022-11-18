"""
Entry point into this project.
"""
import datetime

import daily_tracker.actions
import daily_tracker.form
import daily_tracker.scheduler


def main() -> None:
    """
    Entry point into this project.
    """
    # ? Form testing
    form = daily_tracker.form.TrackerForm(
        at_datetime=datetime.datetime.now(),
        interval=15,
    )
    form.generate_form()

    # ? Scheduler testing
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(
    #     action=test_action,
    #     interval=1,
    # )
    # scheduler.schedule_first()


if __name__ == "__main__":
    main()
