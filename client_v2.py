#!/usr/bin/env python3

# 1 char for opcode - 0 = set, 1 = get, 2 = stats
# 64 chars keys
# 1000 chars value
# 2 newline char
BUFSIZE = 1067

import socket
import sys

def c_conn(server, port, data):
    '''
    This function connects to the server and sends a operation and a opcode
    '''
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c.connect((server, port))
    except socket.gaierror:
        print("bad server name")
        sys.exit()
    except ConnectionRefusedError:
        print("server not available")
        sys.exit()
    try:
        c.send(data)
    except:
        print("failed to send request")
        sys.exit()
    try:
        msg = c.recv(BUFSIZE)
    except:
        print("failed to receive message")
    '''if msg:
        print("the return code from the server is: ", msg.decode('utf-8'))'''
    c.close()
    return msg

if __name__ == "__main__":
    server = sys.argv[1]
    port = 5555
    data = ""
    op = sys.argv[2]
    if op == "set":
        op = str(0)
        key = sys.argv[3]
        val = sys.argv[4]
        data = op + "\n" + key + "\n" + val
    elif op == "get":
        op = str(1)
        key = sys.argv[3]
        data = op + "\n" + key
    else:
        op = str(2)
        data = op

    c_conn(server, port, bytes(data, 'utf-8'))
