import json
import shutil
from abc import ABC, abstractmethod
from threading import Thread, Lock
from typing import final

from numpy import fromfile

from const import *

mutex = Lock()

class DB(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read()
        # shutil.copyfile(filename, filename + 'copy')
        
    def write(self, data):
        mutex.acquire()
        try:
            with open(self.filename, 'w') as f:
                f.write(json.dumps(data))
        finally:
            mutex.release()

    def read(self):
        mutex.acquire()
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        finally:
            mutex.release()


class Date(DB):
    def __init__(self):
        self.data = {'now': 'current date'}
        super().__init__('../../data/date.json')

    def set(self, data):
        mutex.acquire()
        try:
            self.data['now'] = data
        finally:
            mutex.release()
    
    def get(self):
        mutex.acquire()
        try:
            return self.data
        finally:
            mutex.release()

    @property
    def now(self):
        return self.get()['now']

class User(DB):
    def __init__(self):
        super().__init__('../../data/user.json')
        self.data = {'buy': [], 'sell': []}

    def buy(self, data):
        self.data['buy'].append(data)
    
    def sell(self, data):
        self.data['sell'].append(data)

    @property
    def transactions(self):
        return self.data

if __name__ == "__main__":
    o = User()
    o.buy(INTRADAY, 100, "10:05", 102)
    print(o.data)
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.searchsorted.html