"""
Handlers to work as the bridge between the form and the connectors.

This is specifically for the Form defined in this project so is purposefully
coupled to it.
"""
import abc
import datetime
import json
import os
import re

import pandas as pd

import daily_tracker.calendars
import daily_tracker.configuration
import daily_tracker.connectors
import daily_tracker.database
import daily_tracker.form


class Handler(abc.ABC):
    """
    Handles the actions to execute on the form for a given connector to another
    tool/software.
    """
    # def __init__(self):
    #     self.connection = None

    @abc.abstractmethod
    def ok_actions(self, *args, **kwargs) -> None:
        """
        Actions to execute when the OK button is pressed on the form.
        """
        pass


class DatabaseHandler(Handler):
    """
    Handle the connection to the backend database.
    """
    def __init__(self, database_filepath):
        self.connection = daily_tracker.database.DatabaseConnector(database_filepath)

    def ok_actions(
        self,
        configuration: daily_tracker.configuration.Configuration,
        form: daily_tracker.form.TrackerForm,
    ) -> None:
        """
        The database actions that need to be executed when the OK button on the
        form is clicked.
        """
        self.write_to_database(
            task=form.task,
            detail=form.detail,
            at_datetime=form.at_datetime,
            interval=form.interval,
        )

        # Only extract data on the hour -- consider making this more flexible
        if form.at_datetime.minute == 0:
            self.write_to_csv(filepath=configuration.csv_filepath)

    def get_recent_tasks(self, show_last_n_weeks: int) -> dict:
        """
        Return the drop-down list of recent tasks.

        This takes the result of a query into a dataframe, and then converts the
        dataframe into a dictionary whose keys are the tasks and the values are
        the task's latest detail.
        """
        latest_tasks = """
            SELECT
                task,
                detail
            FROM task_last_detail
            WHERE last_date_time >= DATETIME('now', :date_modifier)
               OR last_date_time = ''  /* The default tasks */
            ORDER BY last_date_time DESC
        """
        return dict(
            pd.read_sql(
                sql=latest_tasks,
                con=self.connection.engine,
                params={"date_modifier": f"-{show_last_n_weeks * 7} days"},
            ).to_dict("split")["data"]
        )

    def write_to_database(
        self,
        task: str,
        detail: str,
        at_datetime: datetime.datetime,
        interval: int,
    ) -> None:
        """
        Write the form values to the database.
        """
        self.connection.execute(
            """
            INSERT INTO tracker(date_time, task, detail, interval)
            VALUES (:at_datetime, :task, :detail, :interval)
            """,
            {
                "at_datetime": at_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "detail": detail,
                "interval": interval,
            }
        )

    def write_to_csv(self, filepath: str, previous_days: int = None) -> None:
        """
        Write the tracker history to a CSV file.

        By default, this will download the entire history. To limit this, set
        the number of days to limit this to with the `previous_days` parameter.
        """
        tracker_history = """
            SELECT
                date_time,
                task,
                detail,
                interval
            FROM tracker
            WHERE date_time >= DATE('now', :date_modifier)
            ORDER BY date_time
        """
        pd.read_sql(
            sql=tracker_history,
            con=self.connection.engine,
            params={"date_modifier": f"-{previous_days} days"},
        ).to_csv(
            os.path.join(
                filepath,
                f"daily-tracker-{datetime.datetime.now().isoformat()}.csv"
            )
        )


class CalendarHandler:
    """
    Handle the connection to the linked calendar.
    """
    def __init__(self, calendar_type: str):
        self.connection = daily_tracker.calendars.get_linked_calendar(calendar_type)

    def form_actions(
        self,
        configuration: daily_tracker.configuration.Configuration,
        form: daily_tracker.form.TrackerForm,
    ) -> None:
        """
        The calendar actions that need to be executed when the OK button on the
        form is clicked.
        """
        # Set status?
        pass

    def get_appointment_at_datetime(
        self,
        at_datetime: datetime.datetime,
        categories_to_exclude: list[str],
    ) -> str | None:
        """
        Get the current meeting from Outlook, if one exists.

        This excludes meetings that are daily meetings and meetings whose
        categories are in the supplied list of exclusions.
        """
        if categories_to_exclude is None:
            categories_to_exclude = []

        events = [
            event
            for event in self.connection.get_appointments_at_datetime(at_datetime=at_datetime)
            if all(i not in event.categories for i in categories_to_exclude)
        ]

        return None if len(events) != 1 else events[0].subject


class JiraHandler:
    """
    Handle the connection to the linked Jira project.
    """
    def __init__(self, url: str, key: str, secret: str):
        self.connector = daily_tracker.connectors.JiraConnector(
            url=url,
            key=key,
            secret=secret,
        )
        self.project_key_pattern = re.compile(r"^[A-Z][\w\d]{1,9}-\d+")

    def form_actions(
        self,
        configuration: daily_tracker.configuration.Configuration,
        form: daily_tracker.form.TrackerForm,
    ) -> None:
        """
        The Jira actions that need to be executed when the OK button on the form
        is clicked.
        """
        if configuration.post_to_jira:
            self.post_log_to_jira(
                task=form.task,
                detail=form.detail,
                at_datetime=form.at_datetime,
                interval=form.interval
            )

    def post_log_to_jira(
        self,
        task: str,
        detail: str,
        at_datetime: datetime.datetime,
        interval: int
    ) -> None:
        """
        Post the task, detail, and time to the corresponding ticket's worklog.
        """
        if (issue_key := re.search(self.project_key_pattern, task)) is None:
            return None

        self.connector.add_worklog(
            issue_key=issue_key[0],
            detail=detail,
            at_datetime=at_datetime.isoformat(),
            interval=interval
        )

    def get_tickets_in_sprint(self) -> list[str]:
        """
        Get the list of tickets in the active sprint for the current user.
        """
        jql = "project = DATA AND sprint IN openSprints() AND assignee = currentUser()"
        fields = ["summary", "duedate", "assignee"]

        def get_batch_of_tickets(start_at: int) -> dict:
            """
            Inner function to loop over until all tickets have been retrieved.
            """
            return json.loads(self.connector.search_for_issues_using_jql(
                jql=jql,
                fields=fields,
                start_at=start_at,
            ).text)

        results = []
        total = 999
        while len(results) < total:
            response = get_batch_of_tickets(start_at=len(results))
            total = response["total"]
            results += [f"{issue['key']} {issue['fields']['summary']}" for issue in response["issues"]]

        return results


class SlackHandler:
    """
    Handle the connection to the linked Slack workspace.
    """
    def __init__(self, url: str):
        self.connector = daily_tracker.connectors.SlackConnector(url)

    def form_actions(
        self,
        configuration: daily_tracker.configuration.Configuration,
        form: daily_tracker.form.TrackerForm,
    ) -> None:
        """
        The Slack actions that need to be executed when the OK button on the
        form is clicked.
        """
        if configuration.post_to_slack:
            self._post_to_channel(
                task=form.task,
                detail=form.detail
            )
        # Set status?

    def _post_to_channel(self, task: str, detail: str) -> None:
        """
        Post the task details to a channel.
        """
        self.connector.post_to_channel(message=f"*{task}*: {detail}")
