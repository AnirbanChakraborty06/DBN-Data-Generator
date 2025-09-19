from typing import List, Tuple

from .evaluator.cpds.base import CPD
from .evaluator.time_features import TimeFeature

class Node:
    """
    Represents a variable in the DBN with temporal dependencies.

    Attributes
    ----------
    name : str
        Unique identifier for the node.
    parents : List[Tuple[str, int]]
        List of (parent_name, lag) pairs.
    cpd : "CPD"
        Function defining how to compute the value of this node
        based on parent values.
    """

    def __init__(
            self, 
            name: str,
    ):
        """
        Initializes a Node object representing a variable in the DBN.

        Parameters
        ----------
        name : str
            The unique identifier for the node.
        """
        self.name = name
        self.parents:List[Tuple[str, int]] = []  # Empty list of parents initially
        self.cpd = None  # CPD is None initially

    def add_parent(
            self, 
            parent_name: str, 
            lag: int, 
    ):
        """
        Adds a parent node with a specified temporal lag.

        Parameters
        ----------
        parent_name : str
            The name of the parent node.
        lag : int
            The temporal lag from the parent node.
        """
        self.parents.append((parent_name, lag))

    def set_cpd(self, cpd: CPD):
        """
        Sets the conditional probability distribution (CPD) for the node.

        Parameters
        ----------
        cpd : CPD
            A CPD object (must implement an `evaluate(parent_values)` method).
        """
        if not callable(getattr(cpd, "evaluate", None)):
            raise ValueError("The CPD must implement an 'evaluate' method.")
        self.cpd = cpd


class TemporalNode:
    """
    Represents a time-aware deterministic node in the DBN.

    These nodes derive their values purely from the current timestep,
    not from other parent nodes.

    Attributes
    ----------
    name : str
        Unique identifier for the node.
    time_feature : object
        A deterministic function-like object with an `evaluate(timestep)` method.
    """

    def __init__(self, name: str):
        """
        Initializes a TemporalNode object representing a time-based feature.

        Parameters
        ----------
        name : str
            The unique identifier for the node.
        """
        self.name = name
        self.parents = []  # Although temporal nodes would not have any parents, 
                           # this has been introduced to ensure that calls to
                           # `node.parents` do not error. There would not be
                           # any `add_parent` method.
        self.time_feature = None  # Must be set via `set_time_feature`.

    def set_time_feature(self, time_feature: TimeFeature):
        """
        Sets the deterministic time function (e.g., day of week generator).

        Parameters
        ----------
        time_feature : TimeFeature
            A callable TimeFeature object with an `evaluate` method.
        """
        if not issubclass(type(time_feature), TimeFeature):
            raise TypeError("`time_feature` must be an instance of type `TimeFeature`, or a subclass of it.")
        if not callable(getattr(time_feature, "evaluate", None)):
            raise ValueError("The time feature must implement an 'evaluate' method.")
        self.time_feature = time_feature
