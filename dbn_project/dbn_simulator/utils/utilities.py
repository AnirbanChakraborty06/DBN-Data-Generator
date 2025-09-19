import pandas as pd

def generate_datetime_series(
        length_of_series: int,
        start_time: str,
        frequency: str,
        start_time_format: str = None
) -> list[pd.Timestamp]:
    """
    Generate an array of datetime values of specified length, starting from a specified time.

    Parameters:
    ----------
    length_of_series : int
        The number of datetime entries to generate.

    start_time : str
        The starting timestamp as a string. This will be parsed into a datetime object.

    frequency : str
        Frequency of datetime entries, following pandas offset aliases
        (e.g., 'D' for daily, 'H' for hourly, '15min', 'W', 'M', etc.).

    start_time_format : str, optional
        A strftime-compatible format string to explicitly parse `start_time`.
        If None (default value), pandas will attempt to infer the format automatically.

        This helps in cases where the starting date string is ambiguous on its own.
        Example - "01/03/2025". It can be 01 March or 03 January, 2025.


    Returns:
    -------
    list[pd.Timestamp]
        A list array of pandas `Timestamp` objects representing the datetime series.
    """

    if start_time_format is not None:
        start_time = pd.to_datetime(start_time, format=start_time_format)
    
    return list(pd.date_range(start=start_time, periods=length_of_series, freq=frequency))
