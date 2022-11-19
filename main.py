"""
Entry point into this project.
"""
import datetime

import daily_tracker.actions
import daily_tracker.form
import daily_tracker.scheduler


def create_form() -> None:
    """
    Launch the tracker.
    """
    # TODO: Instead of `datetime.now()`, this should use the next scheduled time
    daily_tracker.form.TrackerForm(datetime.datetime.now())


def main() -> None:
    """
    Entry point into this project.
    """
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(  # OneAtATimeScheduler
    #     action=create_form,
    #     interval=1,  # Tie this to the `configuration.yaml` file
    # )
    # scheduler.schedule_first()

    create_form()


if __name__ == "__main__":
    main()
