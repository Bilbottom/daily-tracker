"""
The actions for the pop-up box.
"""
import datetime
import json
import re
import warnings

import pandas as pd
import pprint

import daily_tracker.database.database
import daily_tracker.jira_connector.jira_connector


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


####################################################################################################
####################################################################################################

# Private Sub PostMessageToSlack()
#     '''
#     ' Execute the Python script which posts a message to a dedicated Slack channel
#     '''
#     Const sSlackPy As String = _
#         "C:\Users\bill.wallis\OneDrive - Allica\Documents\Repository\Python\REST-APIs\Slack\main.py"
#
#     If Trim(Me.tbxDetail) = "" Then
#         Call modPython.RunPython(sFile:=sSlackPy, vArg1:=Trim(Me.cbxProject))
#     Else
#         Call modPython.RunPython(sFile:=sSlackPy, vArg1:="*" & Trim(Me.cbxProject) & "*: " & Trim(Me.tbxDetail))
#     End If
# End Sub


def get_first_item_in_dict(dictionary: dict) -> tuple:
    """
    Return the first key and value in a dictionary as a tuple.
    """
    return next(iter(dictionary.items()))


class ActionHandler:
    """
    Handler for the actions that are triggered on the pop-up box.
    """

    def __init__(self, conn: daily_tracker.database.database.DatabaseConnector):
        self.conn = conn
        self.weeks_to_show = 2

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

    def get_default_task_and_detail(self) -> tuple[str, str]:
        """
        Get the default values for the input box.

        This takes the meeting details from the linked calendar (if one has been
        linked), or just uses the latest task.
        """
        def get_exception_detail(meeting: tuple) -> tuple:
            """
            Map exceptions to their standardised entries.

            For example, something like ("Meetings", "Catch-Up with JJ") could
            be mapped to ("Catch-Ups", "JJ").
            """
            return meeting

        current_meeting = ("task", "detail")  # Get from the linked calendar
        use_calendar_meetings = False  # Get from `configurations.yaml`
        meeting_is_exception = False  # Derive from the category of the meeting

        if use_calendar_meetings and current_meeting is not None:
            if meeting_is_exception:
                current_meeting = get_exception_detail(current_meeting)
            return current_meeting
        else:
            return get_first_item_in_dict(self.get_project_drop_down_list())


####################################################################################################
####################################################################################################


class MeetingHandler:
    """
    Handle the connection to the linked calendar.
    """
    def __init__(self):
        pass


# Private Function GetCurrentAppointment(ByVal sTime As String) As String
#     '''
#     ' Get the current meeting from Outlook, if one exists
#     '
#     ' Might experience performance drop-off when calendar gets bigger
#     ' Only returns something if exactly one appointment is found
#     ' Ignores all-day appointments and Planned Work category
#     '
#     ' https://stackoverflow.com/q/1927799/8213085
#     '''
#     Dim olCalItems As Outlook.Items
#     Dim olFiltered As Outlook.Items
#     Dim olItem     As Outlook.AppointmentItem
#     Dim sTimeFilt  As String
#     Dim sFilter    As String
#     Dim i          As Long
#
#     Let sTimeFilt = Format(Now, "yyyy-mm-dd") & " " & sTime
#     Let sFilter = "[Start] <= '" & sTimeFilt & "' AND [End] > '" & sTimeFilt & "'"
#
#     Set olCalItems = CreateObject("Outlook.Application").GetNamespace("MAPI").GetDefaultFolder(olFolderCalendar).Items
#     olCalItems.IncludeRecurrences = True
#     olCalItems.Sort "[Start]"
#     Set olFiltered = olCalItems.Restrict(sFilter)
#
#     For Each olItem In olFiltered
#         If i > 0 Then GoTo ExitEarly
#
#         If (Not olItem.AllDayEvent) And (InStr(1, olItem.Categories, "Planned Work") = 0) Then
#             Let GetCurrentAppointment = olItem.Subject
#             Let i = i + 1
#         End If
#     Next olItem
#
#     Exit Function
#
# ExitEarly:
#     Let GetCurrentAppointment = ""
# End Function


# Private Function IsAppointmentException(ByVal sSubject As String) As Boolean
#     '''
#     ' Exceptions list -- bad idea to do it this way
#     '''
#     Const sExceptions As String = "" _
#         & "Daily Jira Call," _
#         & "Jira Scrum," _
#         & "Jira Scrum / Team Meeting," _
#         & "Planning," _
#         & "Nik & Bill Catch Up," _
#         & "Nik & Bill Developmental Catch Up," _
#         & "1-2-1 Bill & Juliana," _
#         & "Manage Jira Tickets," _
#         & "Personal Development on Alteryx," _
#         & "Personal Development on Tableau"
#
#     Let IsAppointmentException = IsInArray(sSubject, Split(sExceptions, ","))
# End Function
# Private Function ConvertAppointmentException(ByVal sSubject As String) As String
#     '''
#     ' Exceptions list -- bad idea to do it this way
#     '''
#     Select Case sSubject
#         Case "Daily Jira Call"
#             Let ConvertAppointmentException = "Catch Ups,Daily Jira Call"
#         Case "Jira Scrum"
#             Let ConvertAppointmentException = "Catch Ups,Jira Scrum"
#         Case "Jira Scrum / Team Meeting"
#             Let ConvertAppointmentException = "Catch Ups,Jira Scrum"
#         Case "Planning"
#             Let ConvertAppointmentException = "Catch Ups,Planning"
#         Case "Nik & Bill Catch Up"
#             Let ConvertAppointmentException = "Catch Ups,Nik & Bill"
#         Case "Nik & Bill Developmental Catch Up"
#             Let ConvertAppointmentException = "Catch Ups,Nik & Bill"
#         Case "1-2-1 Bill & Juliana"
#             Let ConvertAppointmentException = "Catch Ups,Juliana & Bill"
#         Case "Manage Jira Tickets"
#             Let ConvertAppointmentException = "Housekeeping,Manage Jira Tickets"
#         Case "Personal Development on Alteryx"
#             Let ConvertAppointmentException = "Personal Development,Alteryx"
#         Case "Personal Development on Tableau"
#             Let ConvertAppointmentException = "Personal Development,Tableau"
#         Case Else
#             Err.Raise Number:=513, Description:="Unrecognised Appointment Exception"
#     End Select
# End Function


####################################################################################################
####################################################################################################


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
