"""
Calendar types available to use for linking.
"""
import enum
import datetime
from typing import Protocol

import daily_tracker.calendars.outlook_connector


class Calendar(Protocol):
    """
    Abstraction of the various calendar types that can be synced with the daily
    tracker.
    """
    def get_calendar_between_datetimes(
        self,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime,
    ) -> list:
        """
        Return the events in the calendar between the start datetime (inclusive)
        and end datetime exclusive.
        """
        ...

    def get_calendar_at_datetime(
        self,
        at_datetime: datetime.datetime
    ) -> list:
        """
        Return the events in the calendar that are scheduled to on or over the
        supplied datetime.
        """
        ...


# noinspection PyArgumentList
class CalendarTypes(enum.Enum):
    """
    Calendar types available to use for linking.
    """
    OUTLOOK = daily_tracker.calendars.outlook_connector.OutlookConnector
    # GOOGLE = enum.auto()
