import numpy as np


def between_time(df, start, end):
    print(start, end)
    return df[(df.index >= start) & (df.index <= end)]


def get_change(final, starting):
    try:
        return ((final - starting) / starting) * 100.0
    except ZeroDivisionError:
        return 0
