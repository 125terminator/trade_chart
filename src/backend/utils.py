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
    return df[(df.index >= start) & (df.index <= end)]

def greater_equal_index(df, start):
    print('valak')
    a = np.argmax(df.index >= start)
    return a