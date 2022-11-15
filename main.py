"""
Entry point into this project.
"""
import datetime

import daily_tracker.actions
import daily_tracker.form
import daily_tracker.scheduler


def ok_action() -> None:
    """
    Dummy action for the pop-up.
    """
    print(datetime.datetime.now())


def test_action() -> None:
    """
    Dummy action for the scheduler.
    """
    pop_up = daily_tracker.form.TrackerForm(
        date_time=datetime.datetime.now(),
        interval=15,
        action=ok_action,
    )
    pop_up.generate_form()


class TestForm:
    """
    Dummy form for testing.
    """
    def __init__(self):
        self.task = "DATA-123 This is a ticket"
        self.detail = "This is some detail on the ticket"
        self.at_datetime = datetime.datetime.now()
        self.interval = 15


def main() -> None:
    """
    Entry point into this project.
    """
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(
    #     action=test_action,
    #     interval=1,
    # )
    # scheduler.schedule_first()

    action_handler = daily_tracker.actions.ActionHandler(TestForm())
    # print(action_handler.database_handler.get_recent_tasks(2))
    # print(action_handler.jira_handler.get_tickets_in_sprint())
    print(action_handler.calendar_handler.get_appointment_at_datetime(
        datetime.datetime.now(),
        action_handler.configuration.appointment_category_exclusions
    ))
    # print(action_handler.configuration.__dict__)
    # print(action_handler.configuration.appointment_exceptions)


if __name__ == "__main__":
    main()
