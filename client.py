#!/usr/bin/env python3
import socket
import sys

def c_conn(server, port, data):
    '''
    This function connects to the server and sends a operation and a opcode
    '''
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((server, port))
    c.send(bytes(data, 'utf-8'))
    if data.split("\n")[0] == '0':
        print("sent the following message to the server")
        print(data)
    c.close()

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

    c_conn(server, port, data)
