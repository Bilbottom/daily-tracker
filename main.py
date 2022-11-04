"""
Entry point into this project.
"""
import datetime

import daily_tracker.scheduler
import daily_tracker.database.database
import daily_tracker.form


def test_action() -> None:
    """
    Dummy action for the scheduler.
    """
    print(datetime.datetime.now())


def main() -> None:
    """
    Entry point into this project.
    """
    # db_conn = daily_tracker.database.database.DatabaseConnector(filepath='tracker.db')
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(
    #     action=test_action,
    #     interval=1
    # )
    # scheduler.schedule_first()
    daily_tracker.form.main()


if __name__ == "__main__":
    main()
