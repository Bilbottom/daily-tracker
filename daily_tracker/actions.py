"""
The actions for the pop-up box.
"""
import datetime
import os.path

import dotenv

import daily_tracker.calendars
import daily_tracker.configuration
import daily_tracker.connectors
import daily_tracker.database
import daily_tracker.handlers
import daily_tracker.utils


dotenv.load_dotenv(dotenv_path=r".env")
JIRA_CREDENTIALS = {
    "url": os.getenv("JIRA_URL"),
    "key": os.getenv("JIRA_KEY"),
    "secret": os.getenv("JIRA_SECRET"),
}
SLACK_CREDENTIALS = {
    "url": os.getenv("SLACK_URL"),
}


class ActionHandler:
    """
    Handler for the actions that are triggered on the pop-up box.
    """

    def __init__(self, form: daily_tracker.handlers.Form):
        """
        Initialise the main handler and the various handlers to other systems.
        """
        self.configuration = daily_tracker.configuration.get_configuration()
        self.form = form

        self.calendar_handler = daily_tracker.handlers.CalendarHandler(self.configuration.linked_calendar)
        self.database_handler = daily_tracker.handlers.DatabaseHandler("tracker.db")
        self.jira_handler = daily_tracker.handlers.JiraHandler(**JIRA_CREDENTIALS)
        self.slack_handler = daily_tracker.handlers.SlackHandler(**SLACK_CREDENTIALS)

    def ok_actions(self) -> None:
        """
        The actions that need to happen according to the configuration.
        """
        for handler in [
            self.database_handler,  # This needs to be done first
            self.calendar_handler,
            self.slack_handler,
            self.jira_handler,
        ]:
            handler.ok_actions(self.configuration, self.form)

    def get_default_task_and_detail(self, at_datetime: datetime.datetime) -> tuple[str, str]:
        """
        Get the default values for the input box.

        This takes the meeting details from the linked calendar (if one has been
        linked), or just uses the latest task.
        """
        current_meeting = self.calendar_handler.get_appointment_at_datetime(
            at_datetime=at_datetime,
            categories_to_exclude=self.configuration.appointment_category_exclusions,
        )

        if not self.configuration.use_calendar_appointments or current_meeting is None:
            return self.database_handler.get_last_task_and_detail()
        return self.configuration.appointment_exceptions.get(
            current_meeting,
            ("Meeting", current_meeting)
        )

    def get_dropdown_options(self) -> dict:
        """
        Return the latest tasks and their most recent detail as a dictionary.

        This is always the most recent tasks, and optionally the tickets in the
        active sprint if a Jira connection has been configured.
        """
        recent_tasks = self.database_handler.get_recent_tasks(self.configuration.show_last_n_weeks)
        return recent_tasks | dict.fromkeys(
            [
                ticket
                for ticket in self.jira_handler.get_tickets_in_sprint()
                if ticket not in recent_tasks.keys()
            ],
            ""
        )
