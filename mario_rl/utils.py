import time
import datetime
import numpy as np

def get_current_date_time_string():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")


class Timer():
    def __init__(self):
        self.times = []

    def start(self):
        self.t = time.time()

    def print(self, msg=''):
        print(f"Time taken: {msg}", time.time() - self.t)

    def get(self):
        return time.time() - self.t
    
    def store(self):
        self.times.append(time.time() - self.t)

    def average(self):
        return sum(self.times) / len(self.times)
    

def running_average(x, N):
    """ Function used to compute the running average
        of the last N elements of a vector x
    """
    if len(x) >= N:
        y = np.copy(x)
        y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
    else:
        y = np.zeros_like(x)
    return y