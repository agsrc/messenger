#!/usr/bin/env python3

import time
import sys
import random

from client_v2 import c_conn

# number of times the experiment will be repeated
ITERATIONS = 10
# attempts in each iteration (in seconds)
ATTEMPTS = 1000

# test parameters
HOST = "localhost"
PORT = 5555

# opcodes
# set - 0
# get - 1
# stats - 2
g_random_requests = [
    bytes("0\nthis is binary\nthis is \\040rward\0", 'utf-8'),
    bytes("1\nthis is binary", 'utf-8'),
    bytes("2", 'utf-8'),
    bytes("1\nbinary", 'utf-8')  # set up the get to fail
]

def throughput():
    '''
    Run the client for a number of time and get the average throughput of the
    system. Run this for a few times and get the number of seconds per op
    as an average.
    This approach is chosen to prevent against a divide by zero exception
    '''
    # hold the return values
    # does not matter what they are
    # we will just count to check throughput
    responses = []
    # hold the avg response time for one iteration
    response_times = []
    #n = ATTEMPTS
    for i in range(ITERATIONS):
        s_time = time.time()
        for n in range(ATTEMPTS):
            data = random.choice(g_random_requests)
            responses.append(c_conn(HOST, PORT, data))
        e_time = time.time()
        response_times.append(int(e_time - s_time) / ATTEMPTS)
    sum = 0
    for t in response_times:
        sum += t
    print("the average throughput of the server is {} seconds per connection".format(sum / ITERATIONS))

def latency():
    '''
    Run the client for a number of time and get the average latency of the
    system. Run this for a few times and get the latency per op as an average.
    '''
    s_time = time.time()
    for i in range(ITERATIONS * ATTEMPTS):
        data = random.choice(g_random_requests)
        _ = c_conn(HOST, PORT, data)
    e_time = time.time()
    print("the average latency of the server is {}".format(int(e_time - s_time) / (ITERATIONS * ATTEMPTS)))

if __name__ == "__main__":
    throughput()
    latency()
