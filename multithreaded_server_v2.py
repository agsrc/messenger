#!/usr/bin/env python3

import queue
import threading
import socket
import sys

# the global hashtable
hashtable = {}
# bing to all network interfaces on this server
HOST = ""
# bind to this port
PORT = 5555

# 1 char for opcode - 0 = set, 1 = get, 2 = stats
# 64 chars keys
# 1000 chars value
# 2 newline char
BUFSIZE = 1067

# we will work with 10 threads and 10 simultaneous requests
MAX_CONCURRENCY = 10
threads = []
# this is a deque that will hold the arguments passed by the clients
# a deque is being used because it is thread safe. So separate locking is not
# required

lock = threading.Lock()

class Consumer(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self._q = q

    def run(self):
        while True:
            args = self._q.get().split("\n")
            # this is for the set functions
            if args[0] == '0' and len(args) == 3:
                kv = [args[1], args[2]]
                lock.acquire()
                set(kv)
                lock.release()
            # the get function
            elif args[0] == '1' and len(args) == 2:
                lock.acquire()
                get(args[1])
                lock.release()
            # finally the stats function
            elif args[0] == '2' and len(args) == 1:
                lock.acquire()
                stats()
                lock.release()
            else:
                print("Unsupported operation")

def Producer():
    q = queue.Queue()
    worker_threads = build_worker_pool(q, MAX_CONCURRENCY)
    # create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind to socket
    s.bind((HOST, PORT))
    # listen for clients
    s.listen(MAX_CONCURRENCY)

    while True:
        # accept connections
        conn, addr = s.accept()
        # recieve data
        data = conn.recv(BUFSIZE)
        # decode data to string
        data = data.decode('utf-8')
        # put in the queue
        q.put(data)

    s.close()  # close socket
    # wait for threads to join
    for worker in worker_threads:
        worker.join()

def build_worker_pool(q, sz):
    workers = []
    for _ in range(sz):
        worker = Consumer(q)
        worker.start()
        workers.append(worker)
    return workers

def set(kv):
    '''
    This function adds a key, value pair to the server
    @Input:
        kv: A list or tuple whose first entry is the key and the second
        entry is the associated value
    @Output:
        -1 on error and 0 on success
    '''
    # We are expecting a tuple or a list data structure
    # to begin with
    if isinstance(kv, tuple) or isinstance(kv, list):
        pass
    else:
        print("failing the type test")
        return -1

    # The first value is the key
    key = kv[0]
    # check if the key is 64 chars or less
    if len(key) > 64:
        print("Not the proper key size")
        return -1

    # remove all spaces from the key
    tmp_key = key.replace(" ", "")
    # the key needs to be alphanumeric
    if not tmp_key.isalnum() or tmp_key.find("\n") != -1:
        print("Not a valid argument")
        return -1

    # the second element is the value
    val = kv[1]
    # remove all spaces from the string
    tmp_val = val.replace(" ", "")
    # the value needs to be alphabetical
    #if not tmp_val.isalnum() or tmp_val.find("\n") != -1:
    if tmp_val.find("\n") != -1:
        print("Not a valid argument")
        return -1

    # the value cannot be more than 1KB in size
    # assuming 1 byte = 1 character
    if len(val) > 1000:
        print("Not proper value size")
        return -1

    # if all the above goes well then the data structure is put into the dictionary
    hashtable[key] = val
    print("added key value pair")
    print(key + ": " + val)
    return 0

def get(key):
    '''
    This function returns the value corresponding to a key
    @Input:
        The key for which the associated value needs to be returned
    @Output:
        The associated value for the key or -1 on failure to find the key
    '''
    # initial assumption is that the key is not found
    val = -1
    for k in hashtable.keys():
        if k == key:
            val = hashtable[key]
            break  # we already found the required value

    # if the key was not found then val is already set to -1
    print("The related value is: ", val)

def stats():
    '''
    This function simply returns the size of the key store
    @Output:
        Prints an integer that is the size of the key store
    '''
    print("There are " + str(len(hashtable.keys())) + " items in the store")

if __name__ == "__main__":
    Producer()
