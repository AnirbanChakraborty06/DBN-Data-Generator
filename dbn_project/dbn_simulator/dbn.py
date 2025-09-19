from typing import List, Optional
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from .node import Node, TemporalNode

class DBN:
    """
    Represents a dynamic Bayesian network with arbitrary temporal depth.

    Attributes
    ----------
    nodes : Dict[str, Node]
        Dictionary of node names to Node objects.
    max_lag : int
        Maximum temporal lag in the entire network.
    """

    def __init__(self):
        """
        Initializes an empty dynamic Bayesian network (DBN).

        This constructor sets up internal structures to hold nodes and track
        the maximum temporal lag in the network.
        """
        self.nodes = {}  # Empty dictionary to store Node objects
        self.max_lag = 0  # Initialize max_lag to 0

    def add_node(self, node: Node):
        """
        Adds a node to the DBN.

        Parameters
        ----------
        node : Node
            The node to be added to the DBN.
        """
        # Add the node to the nodes dictionary
        self.nodes[node.name] = node
        
        for _, lag in node.parents:
            if lag > self.max_lag:
                self.max_lag = lag

    def get_node(self, name: str) -> Optional[Node]:
        """
        Retrieves a node by name.

        Parameters
        ----------
        name : str
            The name of the node to retrieve.

        Returns
        -------
        Optional[Node]
            The node if found, otherwise None.
        """
        return self.nodes.get(name, None)

    def validate_structure(self):
        """
        Validates that the graph is acyclic and all parent references exist.
        """
        pass

    def compute_max_lag(self):
        """
        Computes the maximum lag present in the network.
        """
        pass

    def get_topological_order(self) -> List[Node]:
        """
        Dummy placeholder for actual topological sorting method.
        For now, we return nodes in insertion order.
        """
        G = nx.DiGraph()

        # Add nodes
        for node_name in self.nodes:
            G.add_node(node_name)

        # Method to add edges to the graph:
        # ---------------------------------
        # Add directed edges for 0-lag dependencies only.
        # We only want a topological ordering for the graph that includes the 0-lag edges.

        # Justification for the logic:
        # ----------------------------
        # The reason for this is as follows. 
        # We use the topological ordering in method generate to ensure that we do not try to 
        # generate a sample for the node X, say, at time t, without having already generated 
        # all the necessary samples for its parent nodes. Now, the parents of X with lag 1 or more, 
        # have already been sampled at time step t-1 or earlier. Hence, we only need to worry 
        # about parents of X with 0 lag. We want those nodes to be appearing earlier in the loop 
        # than X. Hence, the topological ordering needs to be done by considering a graph that only 
        # includes the parent-child relations with 0 lag.
        for node in self.nodes.values():
            for parent_name, lag in node.parents:
                if lag == 0:
                    G.add_edge(parent_name, node.name)

        try:
            ordered_names = list(nx.topological_sort(G))
        except nx.NetworkXUnfeasible:
            raise ValueError("Cycle detected in 0-lag dependencies. DBN is not valid.")

        return [self.nodes[name] for name in ordered_names]
    
    def plot_network(self):
        """
        Generates a pictorial representation of the DBN with multiple copies
        of nodes for each time slice based on the max_lag and displays it.
        """
        # Create a directed graph using networkx
        G = nx.DiGraph()

        # Add nodes to the graph for each time slice
        node_positions = {}  # Store positions of nodes for layout
        for time in range(self.max_lag + 1):  # Iterate through time slices
            for node in self.nodes.values():
                node_copy = f"{node.name}({time})"
                G.add_node(node_copy)  # Add a node copy for the current time slice

                # Position nodes in the plot (vertically stacked by time slice)
                node_positions[node_copy] = (time, list(self.nodes.values()).index(node))

        # Add edges based on parent-child relationships (with time slices in mind)
        edges = []
        for node in self.nodes.values():
            for parent_name, lag in node.parents:
                for time in range(self.max_lag + 1):
                    child_copy = f"{node.name}({time})"
                    parent_copy = f"{parent_name}({time - lag})"
                    if time - lag >= 0:  # Only create edges to valid parent copies
                        G.add_edge(parent_copy, child_copy)
                        edges.append((parent_copy, child_copy))

        # # Draw the network with custom positions
        # plt.figure(figsize=(12, 8))
        # nx.draw(G, pos=node_positions, with_labels=True, node_color='lightblue', font_size=10, node_size=3000, font_weight='bold', edge_color='blue')

        # # Display the graph
        # plt.title("Dynamic Bayesian Network with Temporal Depth")
        # plt.show()
        # Begin plotting
        fig, ax = plt.subplots(figsize=(12, 8))

        # Draw nodes and labels
        nx.draw_networkx_nodes(G, pos=node_positions, ax=ax, node_color='lightblue', node_size=3000)
        nx.draw_networkx_labels(G, pos=node_positions, ax=ax, font_size=10, font_weight='bold')

        # Draw edges manually with optional curvature
        for (u, v) in edges:
            x1, y1 = node_positions[u]
            x2, y2 = node_positions[v]

            # Curve edges only if they are in the same time slice (horizontal overlap likely)
            if x1 == x2:
                # If edge is vertical because of same timestamps — we provide some curvature.
                # Also we have ensured that the curvature for adjacent nodes is smaller. For
                # nodes farther part vertically it's more. That ensures less overlap and makes
                # the picture cleaner.
                curvature = max(min(0.1, 0.15 * abs(y1 - y2)), 0.6)
                connectionstyle = f"arc3,rad={curvature}"
            else:
                # Edges that do not connect nodes in the same timestamp,
                # do not need curvature.
                connectionstyle = "arc3,rad=0.0"

            arrow = FancyArrowPatch(
                (x1, y1), (x2, y2),
                connectionstyle=connectionstyle,
                shrinkA=27,
                shrinkB=27,
                arrowstyle='Simple, tail_width=0.5, head_width=10, head_length=15',
                color='blue',
            )
            ax.add_patch(arrow)

        ax.set_title("Dynamic Bayesian Network with Temporal Depth", fontsize=14)
        ax.axis('off')
        
        return fig
