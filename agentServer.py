#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
#from flask import Flask, render_template, request, url_for, session, redirect
#from flask_mysqldb import MySQL
import MySQLdb.cursors
#import re

#app = Flask(__name__)

MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

#mysql = MySQL(app)
connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


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
                cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (us, pa,))
        
                account = cursor.fetchone()
        
                if account:
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
