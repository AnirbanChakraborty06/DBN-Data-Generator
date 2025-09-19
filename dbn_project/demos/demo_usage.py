from dbn_simulator.node import Node, TemporalNode
from dbn_simulator.dbn import DBN
from dbn_simulator.evaluator.cpds.linear_gaussian import LinearGaussianCPD
from dbn_simulator.evaluator.time_features import DayOfWeek, MonthOfYear, PointOfPeriodicCycle
from dbn_simulator.samplers.sequential import Sampler
from datetime import datetime
from dbn_simulator.plotting.timeseries_plots import plot_timeseries_stacked

# --- Create non-temporal nodes ---
X = Node("X")  # Root node, no parents
Y = Node("Y")  # Depends on X
Z = Node("Z")  # Depends on X and T1 (DayOfWeek)
W = Node("W")  # Depends on Y and T2 (MonthOfYear)

# --- Create temporal nodes ---
T1 = TemporalNode("T1")  # Day of Week
# T1.set_time_feature(PointOfPeriodicCycle(periodic_cycle_length=7))
T1.set_time_feature(DayOfWeek())

T2 = TemporalNode("T2")  # Month of Year
# T2.set_time_feature(PointOfPeriodicCycle(periodic_cycle_length=12))
T2.set_time_feature(MonthOfYear())

# --- Define parent relationships ---
Y.add_parent("X", 1)              # Y depends on past X
Z.add_parent("X", 0)              # Z depends on current X
Z.add_parent("T1", 0)             # Z also depends on current T1
W.add_parent("Y", 1)              # W depends on past Y
W.add_parent("T2", 0)             # W also depends on current T2

# --- Define CPDs for regular nodes ---
X.set_cpd(LinearGaussianCPD(
    parent_weights={},  # No parents
    intrinsic_mean=5.0,
    noise_std=0.1
))

Y.set_cpd(LinearGaussianCPD(
    parent_weights={("X", 1): 0.8},
    intrinsic_mean=1.0,
    noise_std=0.1
))

Z.set_cpd(LinearGaussianCPD(
    parent_weights={
        ("X", 0): 0.5,
        ("T1", 0): 0.3
    },
    intrinsic_mean=0.0,
    noise_std=0.1
))

W.set_cpd(LinearGaussianCPD(
    parent_weights={
        ("Y", 1): 1.2,
        ("T2", 0): 0.2
    },
    intrinsic_mean=0.0,
    noise_std=0.1
))

# --- Build the DBN ---
dbn = DBN()
# Add all nodes to DBN
for node in [X, Y, Z, W, T1, T2]:
    dbn.add_node(node)

# --- Plot the DBN ---
fig1 = dbn.plot_network()
image_name = f'images\DBN_Structure - {datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'
fig1.savefig(image_name)

# --- Sample the DBN ---
sampler = Sampler(dbn)

# Optional initial values (only for nodes with temporal lag ≥1)
initial_values = {
    "X": [10.0],
    "Y": [5.0],
    "Z": [0.0],
    "W": [0.0],
}

# Generate the time series
df = sampler.generate(
    n_steps=40, 
    initial_values=initial_values,
    start_time="01-03-2025",
    frequency="D",
    start_time_format="%d-%m-%Y",
)

# Show result
print(df)

# --- Plot the timeseries ---
timeseries_plot = plot_timeseries_stacked(df)
image_name = f'images\Timeseries_Plot - {datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'
timeseries_plot.savefig(image_name)
