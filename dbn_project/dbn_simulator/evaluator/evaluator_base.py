from abc import ABC, abstractmethod
from typing import Any


class Evaluable(ABC):
    """
    Abstract base class for any object that can be evaluated to produce a value.

    This generalizes both CPDs and time-based deterministic features,
    ensuring they expose a consistent interface.
    """

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Any:
        """
        Computes the value based on given inputs.

        Returns
        -------
        Any
            A computed value.
        """
        pass
