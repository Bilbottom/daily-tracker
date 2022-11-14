"""
The actions for the pop-up box.
"""
import datetime
import json
import re
import warnings

import pandas as pd

import daily_tracker.calendars.outlook_connector
import daily_tracker.calendars.calendar_types
import daily_tracker.database.database
import daily_tracker.jira_connector.jira_connector
import daily_tracker.slack_connector.slack_connector
import daily_tracker.utils.utils


# Private Sub UserForm_Initialize()
#     '''
#     ' Create the pop-up box and add the defaults to the boxes
#     '''
# '    On Error Resume Next
# '        Me.Left = GetSetting("Userform Positioning", ThisWorkbook.FullName & "-" & Me.Name, "Left", 0)
# '        Me.Top = GetSetting("Userform Positioning", ThisWorkbook.FullName & "-" & Me.Name, "Top", 0)
# '    On Error GoTo 0
#
#     Dim sDefaults As String
#     Let pCounter = 0
#
#     With Me
#         Let sDefaults = GetDefaultTaskAndDetail(sTime:=.ScheduleTime)
#
#         ' Position and size
#         .Left = 0: .Top = 0: .Height = 144: .Width = 240
#
#         ' Caption
#         .Caption = "Interval Tracker at " & Me.ScheduleTime & " (" & Me.Interval & ")"
#
#         ' Update the drop-down
#         Call ManageUpcomingTicketsInDropDown
#
#         ' Input boxes
#         .tbxDetail.Value = Mid(sDefaults, 1 + InStr(sDefaults, ","))
#         With Me.cbxProject
#             .List = Split(Me.ProjectDropDownList, ",")
#             .Value = Split(sDefaults, ",")(0)
#
#             ' Select the text within the Project box upon loading
#             .SelStart = 0
#             .SelLength = Len(.text)
#         End With
#     End With
# End Sub


# Private Sub btnOK_Click()
#     '''
#     ' Clicking OK prompts a number of actions
#     '''
#     Dim lRow As Long
#     Let pClicks = pClicks + 1
#     If pClicks <> 1 Then
#         Debug.Print "Too many clicks"
#         Exit Sub
#     End If
#
#     ' Write to tracker
#     With wsData
#         Let lRow = .Cells(.Rows.Count, 3).End(xlUp).Row + 1
#
#         .Cells(lRow, 3).Value = Date
#         With .Cells(lRow, 4)
#             .Value = TimeValue(Me.ScheduleTime)
#             .NumberFormat = "hh:mm"
#         End With
#         .Cells(lRow, 5).Value = Trim(Me.cbxProject)
#         .Cells(lRow, 6).Value = Trim(Me.tbxDetail)
#         .Cells(lRow, 7).Value = Me.Interval
#     End With
#
#     ' External actions
#     If Me.PostToSlack Then Call PostMessageToSlack
#     If Me.PostToJira Then Call PostLogToJira
#
#     ' Export data on the hour
#     If Right(Me.ScheduleTime, 2) = "00" Then Call Me.WriteTrackerDataToCSV
#
# '    ' Update the drop-down
# '    Call ManageUpcomingTicketsInDropDown
#
#     ' Close the form
#     Let pClicks = 0
#     Call UserForm_Terminate
# End Sub


# Private Sub cbxProject_Change()
#     '''
#     ' Set the Detail to the last Detail for the selected Project
#     '''
#     If pCounter <> 0 Then Me.tbxDetail = Me.LatestProjectDetail
#     Let pCounter = pCounter + 1
# End Sub


# Public Sub WriteTrackerDataToCSV()
#     '''
#     ' Write the tracker data to a CSV file
#     '''
#     Const sOutFile As String = _
#         "C:\Users\bill.wallis\OneDrive - Allica\Documents\Repository\Excel\Daily-Tracker-Data\daily-tracker-data.csv"
#
#     Call WriteToCSV( _
#         wsData:=wsExport, _
#         sOutFile:=sOutFile _
#     )
# End Sub


# Private Sub ManageUpcomingTicketsInDropDown()
#     '''
#     '
#     '''
#     Const sJiraKey = "^([A-Z][\w\d]{1,9}-\d+).*"
#     Dim sTicket As Variant
#     Dim sKey    As String
#     Dim iCell   As Range
#     Dim bMatch  As Boolean
#
#     ' Clear the 'pending' tickets
#     With wsVariables.Range("rUpcomingProjects")
#         If .Offset(1, 0) = "" Then
#             ' Skip this part
#         ElseIf .Offset(2, 0) = "" Then
#             .Offset(1, 0).Clear
#         Else
#             .Parent.Range(.Offset(1, 0), .Offset(1, 0).End(xlDown)).Clear
#         End If
#     End With
#
#     ' Add the 'pending' tickets
#     For Each sTicket In Split(GetTicketsInSprint, ";")
#         Let sKey = RegexpReplace(sTicket, sJiraKey, "$1")
# '        Debug.Print sKey, sTicket
#
#         ' If the rRecentProjects list is empty, don't loop through it
#         Let bMatch = (wsVariables.Range("rRecentProjects").Offset(1, 0) = "")
#
#         With wsVariables
#             Let bMatch = False
#
#             ' Only add it to the rUpcomingProjects list if it isn't in the rRecentProjects list
#             For Each iCell In .Range(.Range("rRecentProjects"), .Range("rRecentProjects").End(xlDown))
#                 If Not bMatch Then bMatch = (sKey = RegexpReplace(iCell.Value, sJiraKey, "$1"))
#             Next iCell
#
#             If Not bMatch Then .Range("rUpcomingProjects").Offset(-1, 0).End(xlDown).Offset(1, 0).Value = sTicket
#         End With
#     Next sTicket
# End Sub


# Private Sub ThisWorkbook_AddTicketsToDropDown()
#     Const sJiraKey = "^([A-Z][\w\d]{1,9}-\d+).*"
#     Dim sTicket As Variant
#     Dim sKey    As String
#     Dim iCell   As Range
#     Dim bMatch  As Boolean
#
#     For Each sTicket In Split(GetTicketsInSprint, ";")
#         Let sKey = RegexpReplace(sTicket, sJiraKey, "$1")
#         Debug.Print sKey, sTicket
#
#         With wsVariables
#             Let bMatch = False
#             For Each iCell In .Range(.Range("rRecentProjects"), .Range("rRecentProjects").End(xlDown))
#                 If Not bMatch Then bMatch = (sKey = RegexpReplace(iCell.Value, sJiraKey, "$1"))
#             Next iCell
#             If Not bMatch Then .Range("rRecentProjects").End(xlDown).Offset(1, 0).Value = sTicket
#         End With
#     Next sTicket
# End Sub
# """


class ActionHandler:
    """
    Handler for the actions that are triggered on the pop-up box.
    """

    def __init__(self, conn: daily_tracker.database.database.DatabaseConnector):
        self.conn = conn
        self.weeks_to_show = 2
        self.use_calendar_meetings = False  # Get from `configurations.yaml`
        self.calendar_handler = MeetingHandler(
            calendar_type=daily_tracker.calendars.calendar_types.CalendarTypes.OUTLOOK
        )

    def get_project_drop_down_list(self) -> dict:
        """
        Return the drop-down list of recent tasks.

        This takes the result of a query into a dataframe, and then converts the
        dataframe into a dictionary whose keys are the tasks and the values are the
        task's latest detail.
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
                con=self.conn.engine,
                params={"date_modifier": f"-{self.weeks_to_show * 7} days"},
            ).to_dict("split")["data"]
        )

    def get_default_task_and_detail(self, at_datetime: datetime.datetime) -> tuple[str, str]:
        """
        Get the default values for the input box.

        This takes the meeting details from the linked calendar (if one has been
        linked), or just uses the latest task.
        """
        current_meeting = self.calendar_handler.get_appointment_at_datetime(
            at_datetime=at_datetime,
            categories_to_exclude=["Planned Work"],
        )

        if not self.use_calendar_meetings or current_meeting is None:
            return daily_tracker.utils.utils.get_first_item_in_dict(
                self.get_project_drop_down_list()
            )
        return MEETING_EXCEPTIONS.get(current_meeting[0], current_meeting)


class MeetingHandler:
    """
    Handle the connection to the linked calendar.
    """
    def __init__(self, calendar_type: daily_tracker.calendars.calendar_types.CalendarTypes):
        self.connection: daily_tracker.calendars.calendar_types.Calendar = calendar_type.value()

    def get_appointment_at_datetime(
        self,
        at_datetime: datetime.datetime,
        categories_to_exclude: list[str],
    ) -> str | None:
        """
        Get the current meeting from Outlook, if one exists.

        This excludes meetings that are daily meetings and meetings whose
        categories are in the supplied list.
        """
        events = self.connection.get_calendar_at_datetime(at_datetime=at_datetime)
        if len(events) != 0 or any(i in events[0].categories for i in categories_to_exclude):
            return None  # Don't take any of them

        return events[0].subject


# This should be altered to be managed outside of code
MEETING_EXCEPTIONS = {  # Exception: Replacement
    "Daily Jira Call": ("Catch Ups", "Daily Jira Call"),
    "Jira Scrum": ("Catch Ups", "Jira Scrum"),
    "Jira Scrum / Team Meeting": ("Catch Ups", "Jira Scrum"),
    "Planning": ("Catch Ups", "Planning"),
    "Nik & Bill Catch Up": ("Catch Ups", "Nik & Bill"),
    "Nik & Bill Developmental Catch Up": ("Catch Ups", "Nik & Bill"),
    "1-2-1 Bill & Juliana": ("Catch Ups", "Juliana & Bill"),
    "Manage Jira Tickets": ("Housekeeping", "Manage Jira Tickets"),
    "Personal Development on Alteryx": ("Personal Development", "Alteryx"),
    "Personal Development on Tableau": ("Personal Development", "Tableau"),
}


class JiraHandler:
    """
    Handle the connection to the linked Jira project.
    """
    def __init__(self, url: str, key: str, secret: str):
        self.connector = daily_tracker.jira_connector.jira_connector.JiraConnector(
            url=url,
            key=key,
            secret=secret,
        )
        self.project_key_pattern = re.compile(r"^[A-Z][\w\d]{1,9}-\d+")

    def post_log_to_jira(
        self,
        task: str,
        detail: str,
        interval: int,
        at_datetime: datetime.datetime
    ) -> None:
        """
        Post the task, detail, and time to the corresponding ticket's worklog.
        """
        if (issue_key := re.search(self.project_key_pattern, task)) is None:
            return None  # TODO: Create a Task object that has properties like `is_meeting` and `is_jira_ticket`

        self.connector.add_worklog(
            issue_key=issue_key[0],
            detail=detail,
            interval=interval,
            at_datetime=at_datetime.isoformat()
        )

    def get_tickets_in_sprint(self) -> list[str]:
        """
        Get the list of tickets in the active sprint for the current user.
        """
        jql = {
            "fields": "summary,duedate,assignee",
            "jql": "project = DATA AND sprint IN openSprints() AND assignee = currentUser()",
        }
        response = json.loads(self.connector.search_for_issues_using_jql(search_params=jql).text)
        if response["maxResults"] < response["total"]:
            # Should add some recursive looping to get all tickets in the future
            warnings.warn(f"Only using the first {response['maxResults']} tickets returned from the JQL.")

        return [f"{issue['key']} {issue['fields']['summary']}" for issue in response["issues"]]


class SlackHandler:
    """
    Handle the connection to the linked Slack workspace.
    """
    def __init__(self, url: str, token: str):
        self.connector = daily_tracker.slack_connector.slack_connector.SlackConnector(
            url=url,
            token=token,
        )

    def post_to_channel(self, task: str, detail: str) -> None:
        """
        Post the task details to a channel.
        """
        self.connector.post_to_channel(message=f"*{task}*: {detail}")
