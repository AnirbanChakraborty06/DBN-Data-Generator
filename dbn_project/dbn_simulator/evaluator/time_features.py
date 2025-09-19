from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from .evaluator_base import Evaluable


class TimeFeature(Evaluable, ABC):
    """
    Abstract base class for deterministic time-based feature generators.

    These are used by TemporalNodes to produce values that depend only on time.
    Supports both integer-based timesteps and real datetime objects.
    """

    @abstractmethod
    def evaluate(self, time: Union[int, datetime]):
        """
        Computes the value of the feature for the given time input.

        Parameters
        ----------
        time : Union[int, datetime]
            The current timestep (as integer or datetime).

        Returns
        -------
        Any
            A deterministic feature value derived from time.
        """
        pass


class DayOfWeek(TimeFeature):
    """
    Returns the day of the week.
    Monday=1, ..., Sunday=7 (ISO weekday)
    """

    def evaluate(self, time: datetime) -> int:
        return time.isoweekday()  # Monday=1, Sunday=7


class DayOfMonth(TimeFeature):
    """
    Returns the calendar day of the month.
    """

    def evaluate(self, time: datetime) -> int:
        return time.day


class MonthOfYear(TimeFeature):
    """
    Returns the calendar month of the year.
    1 (January) to 12 (December).
    """

    def evaluate(self, time: datetime) -> int:
        return time.month


class PointOfPeriodicCycle(TimeFeature):
    """
    For the input time-step, returns the point in the periodic cycle.
    The output numbers range from 1, 2, ..., 10 for a periodic cycle of length 10.
    """
    def __init__(self, periodic_cycle_length: int):
        self.periodic_cycle_length = periodic_cycle_length

    def evaluate(self, timestep: int) -> int:
        return (timestep % self.periodic_cycle_length) + 1
