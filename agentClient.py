#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
import datetime

#HOST = input("Enter IP address of server: ")

now = datetime.datetime.now()

HOST = "192.168.0.192" # The server's hostname or IP address.
PORT = 65000         # The port used by the server.
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to {}...".format(ADDRESS))
    s.connect(ADDRESS)
    print("Connected.")
    

    while True:
        time = (now.strftime("%Y-%m-%d %H:%M:%S"))
        print("Welcome to Car Hire")
        print("Choose type of Log In")
        print("1. Log In With Credentials")
        print("2. Log In With FaceID")
        sel = input("Enter Number: ")
        if sel == "1":
            dec = "1"
            s.sendall(dec.encode())
            print("Enter Credentials")
            username = input("Username: ")
            s.sendall(username.encode())
            password = input ("Password: ")
            s.sendall(password.encode())
            print("test 4")
            reply = s.recv(4096)
            print("test 3")
            rep = reply.decode()
            
            if rep == "true":
                print("Welcome {}".format(username))
                print("1. Unlock Car")
                print("2. Return Car")
                choice = input("Enter Choice: ")
                if choice == "1":
                    print("Car Unlocked")
                    break
                elif choice == "2":
                    print("Car Returned")
                    break
            elif rep == "false":
                print("Incorrect Login")
                break
            else:
                print("ERROR")
                break
            
        
        elif sel == "2":
            print("Functionality not Implemented")
            break
                
          
        else:
            print("Invalid Input")
            break
            
        
        
        
        s.sendall(time.encode())
        
        
    
    print("Disconnecting from server.")
print("Done.")
