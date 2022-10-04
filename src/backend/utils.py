import json
import numpy as np

statePath = '../../data/date.json'
def get_state():
    return json.load(open(statePath, 'r'))

def push_state(state):
    a = json.dumps(state)
    f = open(statePath, 'w')
    f.write(a)
    f.close()

def between_time(df, start, end):
    print(start, end)
    return df[(df.index >= start) & (df.index <= end)]

def get_change(current, previous):
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

# def ge_index(df, start):
#     # TODO: use binary search of pandas for faster access
#     # a = np.argmax(df.index >= start)
#     # return a
#     return df.index.searchsorted(start)