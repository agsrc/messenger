# messenger

Single threaded server and a client

The server accepts 10 simultaneous connections and uses a global Python dictionary as a hash table. The server binds to all network interfaces on any machine it's run on. And it always runs on port 5555. This can be changed to another more suitable port number like 55000. In it's present state, the server supports the following operations as mentioned in the homework specifications:
1. set
2. get
3. stats

The client is simple. It accepts all command line arguments and combines them into a single message with fields separated by the newline character. No separate data structure has been created for this. All error checking is done by the server and none by the client.

It has been assumed that each ASCII character only occupies 1 byte of space. Thus the server has been designed to accept only 1067 bytes, at most, from any client:
