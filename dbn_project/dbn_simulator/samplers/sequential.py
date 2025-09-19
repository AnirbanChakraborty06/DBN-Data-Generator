from typing import Dict, List, Any
import pandas as pd
from ..dbn import DBN
from ..node import Node, TemporalNode
from ..utils.utilities import generate_datetime_series

class Sampler:
    """
    Responsible for generating samples from the DBN over time.

    Attributes
    ----------
    dbn : DBN
        The DBN object to sample from.
    """

    def __init__(self, dbn: DBN):
        """
        Initializes the sampler with a reference to a DBN.

        Parameters
        ----------
        dbn : DBN
            The dynamic Bayesian network to sample from.
        """
        self.dbn = dbn

    def generate(
        self, 
        n_steps: int, 
        initial_values: Dict[str, List[float]] = None,
        replacement_value_for_non_existing_parents: float = 0.0,
        time_column_name: str = "Time",
        start_time: str = None,
        frequency: str = None,
        start_time_format: str = None,
        exclude_temporal_nodes_from_output: bool = False,
    ) -> pd.DataFrame:
        """
        Generates a multivariate time series from the DBN in the form of a pandas DataFrame.

        Parameters
        ----------
        n_steps : int
            The number of time steps to simulate.
        initial_values : Dict[str, List[float]], optional
            An optional dictionary of initial values for each node
            (up to the max_lag length).
        replacement_value_for_non_existing_parents : float, optional
            Value to use when a parent value at required lag is unavailable.
            Defaults to 0.0.
        time_column_name : str, optional
            Name of the column indicating the time steps.
            "Time" by default.
        start_time : str, optional
            If the time-steps are to be generated as datetime-type objects, 
            then the start-time needs to be provided.
            None by default.
        frequency : str, optional
            If start_time is provided, then the frequency of the time-steps 
            needs to be provided as well. It can be one of the pandas offset 
            aliases (e.g., 'D' for daily, 'H' for hourly, 'W', 'M', etc.).
            None, by default.
        start_time_format : str, optional
            A strftime-compatible format string to explicitly parse `start_time`.
            If None (default value), pandas will attempt to infer the format automatically.

            This helps in cases where the starting date string is ambiguous on its own.
            Example - "01/03/2025". It can be 01 March or 03 January, 2025.
        exclude_temporal_nodes_from_output : bool, optional
            If True, the temporal nodes would be excluded from the output dataframe.
            False by default.

        Returns
        -------
        pd.DataFrame
            A DataFrame for the timeseries against each of the nodes.
        """
        # This dictionary would contain the timeseries of values against each node.
        # It would also contain the series of time-steps against the key `Time-step`.
        timeseries: Dict[str, List[float]] = {
            node_name: [0.0] * n_steps
            for node_name
            in self.dbn.nodes.keys()
        }
        
        if (start_time is not None) and (frequency is None):
            raise ValueError("If start_time is provided, frequency should be provided as well.")
        elif (start_time is None) and (frequency is not None):
            raise ValueError("If frequeny is provided, start_time should be provided as well.")
        elif (start_time is not None) and (frequency is not None):
            timeseries[time_column_name] = generate_datetime_series(
                length_of_series = n_steps,
                start_time = start_time,
                frequency = frequency,
                start_time_format = start_time_format
            )
        else:
            timeseries[time_column_name] = list(range(n_steps))

        nodes_in_topological_order = self.dbn.get_topological_order()

        if initial_values:
            # Temporal nodes do not need initial values to be provided in the dictionary.
            # These can be automatically derived.
            for node in self.dbn.nodes.values():
                if isinstance(node, TemporalNode):
                    initial_values[node.name] = [
                        node.time_feature.evaluate(timestep)
                        for timestep in timeseries[time_column_name][:self.dbn.max_lag]
                    ]
            # If initial_values are provided it should be provided
            # for all nodes.
            set_of_nodes_in_initial_values = set(initial_values.keys())
            all_nodes = set(self.dbn.nodes.keys())
            if all_nodes != set_of_nodes_in_initial_values:
                missing_nodes_for_initial_values = all_nodes - set_of_nodes_in_initial_values
                raise ValueError(f"Node(s) {list(missing_nodes_for_initial_values)} are not provided in `initial_values`")
            
            for current_node_name in all_nodes:
                # If initial values are provided it should be of length `max_lag`.
                if (x:=len(initial_values[current_node_name])) != self.dbn.max_lag:
                    raise ValueError(f"Expected {self.dbn.max_lag} value(s) for {current_node_name} in `initial_values`. But found {x} value(s).")
                else:    
                    timeseries[current_node_name][:self.dbn.max_lag] = initial_values[current_node_name]

        # If initial_values was provided then we need to generate samples from time step 
        # `max_lag` onwards. Else, we need to generate samples from time step 0.
        starting_timestep_for_evaluation = (0 if initial_values is None else self.dbn.max_lag)
        for (current_time, current_timestep) in zip(
            timeseries[time_column_name][starting_timestep_for_evaluation:],
            range(starting_timestep_for_evaluation, n_steps),
        ):  # Looping through the timesteps.
            for current_node in nodes_in_topological_order:
                if not isinstance(current_node, TemporalNode):  # If it's not a temporal node, derive its values from its parents
                    parentwise_values: Dict[str, Any] = dict() # Captures the parent-wise values
                    for parent_node_name, lag in current_node.parents:
                        lagged_timestep = current_timestep - lag
                        if lagged_timestep >= 0:  # If the lagged value for the parent is available as of current time-step.
                            parentwise_values[(parent_node_name, lag)] = timeseries[parent_node_name][lagged_timestep]
                        else:
                            parentwise_values[(parent_node_name, lag)] = replacement_value_for_non_existing_parents

                    # Evaluate the value of current_node in current_timestep.
                    # Then assign this value against the current_node for the current_timestep.
                    current_node_current_timestep_value = current_node.cpd.evaluate(parent_values = parentwise_values)
                else: 
                    # If current node is a temporal node, then its value can be derived through the 
                    # the respective node's time_feature attribute.
                    current_node_current_timestep_value = current_node.time_feature.evaluate(current_time)
                
                timeseries[current_node.name][current_timestep] = current_node_current_timestep_value
        
        # Generate the output dataframe
        timeseries_dataset = pd.DataFrame(
            data=timeseries
        )
        
        if exclude_temporal_nodes_from_output:
            # Exclude the temporal nodes from the list of output columns.
            nodes_in_output_dataframe = [
                node.name
                for node in nodes_in_topological_order
                if not isinstance(node, TemporalNode)
            ]

            return timeseries_dataset.loc[: [*nodes_in_output_dataframe, time_column_name]]
        
        return timeseries_dataset
