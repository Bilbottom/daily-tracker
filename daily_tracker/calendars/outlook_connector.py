"""
Connect to and read events from an Outlook calendar.

This requires Outlook to be installed as a desktop application on the device
running this code.
"""
import dataclasses
import datetime
from typing import Any

import win32com.client


@dataclasses.dataclass
class OutlookEvent:
    """
    Events in Outlook, typically referred to as Meetings or Appointments.

    Note that categories are not available for IMAP accounts, see:
        * https://learn.microsoft.com/en-us/outlook/troubleshoot/user-interface/cannot-assign-color-categories-for-imap-accounts
    """
    _appointment: win32com.client.CDispatch = dataclasses.field(repr=False)
    subject: str = dataclasses.field(default=None)
    start: datetime.datetime = dataclasses.field(default=None)
    end: datetime.datetime = dataclasses.field(default=None)
    body: str = dataclasses.field(default=None)
    categories: list[str] = dataclasses.field(default=list)

    def __post_init__(self):
        """
        Pull out the appointment details into fields.
        """
        self.subject = self._appointment.subject
        self.start = self._appointment.start
        self.end = self._appointment.end
        self.body = self._appointment.body
        self.categories = self._appointment.categories


class OutlookConnector:
    """
    Naive implementation of a connector to Outlook.
    """
    def __init__(self):
        outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
        self.calendar = outlook.getDefaultFolder(9).Items
        self.calendar.IncludeRecurrences = True
        self.calendar.Sort('[Start]')

    def get_calendar_between_dates(self, start_date: datetime.date, end_date: datetime.date) -> Any:
        """
        Return the events in the calendar between the start_date and end_date.
        """
        restricted_calendar = self.calendar.Restrict(
            " AND ".join([
                f"[Start] >= '{start_date.strftime('%Y-%m-%d')}'",
                f"[END] >= '{end_date.strftime('%Y-%m-%d')}'",
            ])
        )
        return [OutlookEvent(app) for app in restricted_calendar]

    def main(self):
        appointments = self.get_calendar_between_dates(datetime.date(2022, 11, 12), datetime.date(2022, 11, 14))
        [print(app) for app in appointments]
