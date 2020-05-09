#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket

HOST = input("Enter IP address of server: ")

# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 65000         # The port used by the server.
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to {}...".format(ADDRESS))
    s.connect(ADDRESS)
    print("Connected.")

    while True:
        message = input("Enter message (blank input to end): ")
        if(not message):
            break
        
        s.sendall(message.encode())
        data = s.recv(4096)
        print("Received {} bytes of data decoded to: '{}'".format(
            len(data), data.decode()))
    
    print("Disconnecting from server.")
print("Done.")
