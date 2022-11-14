"""
Entry point into this project.
"""
import datetime
import os

import dotenv

import daily_tracker.actions
import daily_tracker.calendars.outlook_connector
import daily_tracker.database.database
import daily_tracker.form
import daily_tracker.scheduler


dotenv.load_dotenv(dotenv_path=r".env")
JIRA_CREDENTIALS = {
    "url": os.getenv("JIRA_URL"),
    "key": os.getenv("JIRA_KEY"),
    "secret": os.getenv("JIRA_SECRET"),
}
SLACK_CREDENTIALS = {
    "url": os.getenv("SLACK_URL"),
}


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


def main() -> None:
    """
    Entry point into this project.
    """
    # db_conn = daily_tracker.database.database.DatabaseConnector(filepath='tracker.db')
    # scheduler = daily_tracker.scheduler.IndefiniteScheduler(
    #     action=test_action,
    #     interval=1,
    # )
    # scheduler.schedule_first()
    # action_handler = daily_tracker.actions.ActionHandler(conn=db_conn)
    # items = action_handler.get_project_drop_down_list()
    # print(items)
    # jira_handler = daily_tracker.actions.JiraHandler(**JIRA_CREDENTIALS)
    # print(jira_handler.get_tickets_in_sprint())
    # outlook_conn = daily_tracker.calendars.outlook_connector.OutlookConnector()
    # appointments = outlook_conn.get_calendar_between_datetimes(
    #     start_datetime=datetime.datetime(2022, 11, 12, 0, 0, 0),
    #     end_datetime=datetime.datetime(2022, 11, 15, 0, 0, 0),
    # )
    # appointments = outlook_conn.get_calendar_at_datetime(
    #     date_time=datetime.datetime.now(),
    # )
    # [print(app) for app in appointments]
    slack_handler = daily_tracker.actions.SlackHandler(**SLACK_CREDENTIALS)
    slack_handler.post_to_channel(task="Something", detail="Some detail")


if __name__ == "__main__":
    main()
