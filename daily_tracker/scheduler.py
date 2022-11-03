"""
The tracker generates a pop-up box to record current work which updates local
files, as well as optionally integrates with other third-party tools.
"""
import datetime
import sched
import time
from typing import Callable


# def _decimal(round_to: int | None = None) -> Callable:
#     """
#     Decorator for the `_to_decimal` function with an optional precision to round
#     to.
#     """
#     def decorator(func: Callable) -> Callable:
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             if round_to is None:
#                 return _to_decimal(func(*args, **kwargs))
#             else:
#                 return _to_decimal(round(func(*args, **kwargs), round_to))
#         return wrapper
#     return decorator


def _to_time() -> None:
    """
    Not for usage!

    Reminder of how to get datetime.datetime.now() into time.time()
    """
    print(time.time())
    print(datetime.datetime.now().timestamp())


def get_next_interval(
    from_time: datetime.datetime,
    interval_in_minutes: int,
) -> datetime.datetime:
    """
    Derive the next schedule time from the input time and interval.

    Schedules will be defined assuming that the schedule starts on the hour.
    This means that interval values that divide 60 will function the best.

    :param from_time: The datetime from which the scheduled datetime should be
        calculated. The scheduled datetime will be greater than or equal to this
        value.
    :param interval_in_minutes: The interval, in minutes, between the scheduled
        events.
    :return: The next scheduled datetime.
    """
    return datetime.timedelta(minutes=interval_in_minutes) + datetime.datetime(
        year=from_time.year,
        month=from_time.month,
        day=from_time.day,
        hour=from_time.hour,
        minute=from_time.minute - (from_time.minute % interval_in_minutes),
        second=0,
    )


class IndefiniteScheduler:
    """
    A processor that schedules the pop-up boxes and passes the data around to
    various applications indefinitely.
    """

    def __init__(self, action: Callable, interval: int):  # TODO: Remove the action default argument
        """
        Create the scheduler.
        """
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._running = False
        self._next_schedule_time: datetime.datetime | None = None
        self._next_event: sched.Event | None = None
        self.action = action
        self._interval = interval

    def action_wrapper(self) -> None:
        """
        Wrap the action so that we can schedule the next event when it's called.
        """
        self.action()
        self._schedule_next()

    def schedule(self, cancel: bool = False) -> None:
        """
        Schedule (or cancel) the next event.
        """
        if cancel:
            self._scheduler.cancel(self._next_event)
            self._next_event = None
        else:
            self._next_event = self._scheduler.enterabs(
                time=self._next_schedule_time.timestamp(),
                priority=1,
                action=self.action_wrapper,
            )

    def schedule_first(
        self,
        schedule_at: datetime.datetime = datetime.datetime.now()
    ) -> None:
        """
        Schedule the first event.
        """
        if self._running:
            raise AssertionError("The `schedule_first` method was called while the scheduler is already running.")

        self._running = True
        self._next_schedule_time = schedule_at
        self._schedule_next()
        self._scheduler.run()

    def _schedule_next(self) -> None:
        """
        Schedule the next event.
        """
        assert self._running

        self._next_schedule_time = get_next_interval(
            from_time=self._next_schedule_time,
            interval_in_minutes=self._interval,
        )
        self.schedule()

    def _cancel_next(self) -> None:
        """
        Cancel the next event.
        """
        self.schedule(cancel=True)
        self._running = False
