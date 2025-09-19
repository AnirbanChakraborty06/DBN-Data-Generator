import matplotlib.pyplot as plt
import pandas as pd


def plot_timeseries_stacked(
    df: pd.DataFrame,
    time_column: str = "Time",
    height_per_plot: float = 2.0,
    width: float = 10.0,
    line_color: str = "tab:blue"
):
    """
    Plots vertically stacked time series line plots for each variable.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the time series data. Must include a time column.
    time_column : str, optional
        Name of the time axis column. Default is "Time-step".
    height_per_plot : float, optional
        Height of each subplot. Default is 2.0 inches.
    width : float, optional
        Total figure width. Default is 10.0 inches.
    line_color : str, optional
        Color to use for the line plots. Default is "tab:blue".
    """
    if time_column not in df.columns:
        raise ValueError(f"Time column '{time_column}' not found in DataFrame.")

    variable_columns = [col for col in df.columns if col != time_column]
    n_vars = len(variable_columns)

    fig, axes = plt.subplots(
        nrows=n_vars,
        ncols=1,
        figsize=(width, height_per_plot * n_vars),
        sharex=True
    )

    # If only one variable, axes is not a list — make it a list for consistency
    if n_vars == 1:
        axes = [axes]

    for ax, var in zip(axes, variable_columns):
        ax.plot(df[time_column], df[var], color=line_color)
        ax.set_ylabel(var, rotation=0, labelpad=40, fontsize=10, va='center')
        ax.grid(True)

    axes[-1].set_xlabel(time_column)

    fig.tight_layout()
    return fig
