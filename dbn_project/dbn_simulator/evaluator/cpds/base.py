from typing import Dict
from ..evaluator_base import Evaluable


class CPD(Evaluable):
    """
    Base class for all Conditional Probability Distributions (CPDs).

    CPDs define how a node's value is computed based on its parents' values.

    Methods
    -------
    evaluate(parent_values)
        Compute the value of the node given its parent values.
    """

    def evaluate(self, parent_values: Dict) -> float:
        """
        Abstract method to evaluate the CPD.

        Parameters
        ----------
        parent_values : Dict
            A dictionary with keys as (parent_name, lag) and values as the corresponding values.

        Returns
        -------
        float
            The evaluated value for the current node.
        """
        raise NotImplementedError("CPD subclasses must implement 'evaluate'")
