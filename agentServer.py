#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 65000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        while True:
            data = conn.recv(4096)
            
            print(data.decode())
            reply = data.decode()
            if reply == "1":
                username = conn.recv(4096)
                us = username.decode()
                print("username is: {}".format(us))
                
                password = conn.recv(4096)
                pa = password.decode()
                print("password is: {}".format(pa))
                if us == "user" and pa == "pass":
                    msg = "true"
                    #s.sendall = (msg.encode())
                    print("test 1")
                else:
                    msg = "false"
                    #s.sendall = (msg.encode())
                    print("test 2")
                    break
                
                conn.sendall(msg.encode())
                
                    
            
            
        
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
