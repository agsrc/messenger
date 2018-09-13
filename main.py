#!/usr/bin/env python3

from multiprocessing import Process

from evaluate import throughput, latency
from multithreaded_server_v4 import *

def main():
    s = Process(target=Server)
    s.start()
    t = Process(target=throughput)
    t.start()
    t.join()
    l = Process(target=latency)
    l.start()
    l.join()

if __name__ == "__main__":
    main()
