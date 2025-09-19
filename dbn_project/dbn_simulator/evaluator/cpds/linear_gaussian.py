import numpy as np
from typing import Dict, Tuple
from .base import CPD

class LinearGaussianCPD(CPD):
    """
    A simple CPD representing a linear Gaussian model:
        Y_t = intrinsic_mean + sum(w_i * X_{t-k}) + noise
    """

    def __init__(self, parent_weights: Dict[Tuple[str, int], float], intrinsic_mean: float, noise_std: float):
        """
        Initializes a linear Gaussian conditional probability distribution.

        Parameters
        ----------
        parent_weights : Dict[Tuple[str, int], float]
            Dictionary mapping (parent_name, lag) tuples to their respective weights.
        intrinsic_mean : float
            The base mean added to the linear combination of parent values.
        noise_std : float
            The standard deviation of the Gaussian noise added during sampling.
        """
        self.parent_weights = parent_weights
        self.noise_std = noise_std
        self.intrinsic_mean = intrinsic_mean


    def evaluate(self, parent_values: Dict[Tuple[str, int], float]) -> float:
        """
        Computes the output based on linear combination + Gaussian noise.

        Parameters
        ----------
        parent_values : Dict[Tuple[str, int], float]
            A dictionary containing the values of the parent nodes.

        Returns
        -------
        float
            The computed value for the node, including noise.
        """
        linear_sum = sum(
            [self.intrinsic_mean]
            + [
                self.parent_weights.get(key, 0.0) * val 
                for key, val 
                in parent_values.items()
            ]
        )
        return np.random.default_rng().normal(loc=linear_sum, scale=self.noise_std)
