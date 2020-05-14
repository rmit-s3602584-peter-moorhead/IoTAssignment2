#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
#from flask import Flask, render_template, request, url_for, session, redirect
#from flask_mysqldb import MySQL
import MySQLdb.cursors
#import re
def main():
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
                print(reply)
                if reply == "1":
                    username = conn.recv(4096)
                    us = username.decode()
                    print("username is: {}".format(us))
                    
                    password = conn.recv(4096)
                    pa = password.decode()
                    print("password is: {}".format(pa))
                    carIdent = conn.recv(4096)
                    carID = carIdent.decode()
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (us, pa,))
            
                    account = cursor.fetchone()
            
                    if account:
                        msg = "true"
                        print("test 1")
                    else:
                        msg = "false"
                        print("test 2")
                        break
                    conn.sendall(msg.encode())
                    
                    carStatus = conn.recv(4096)
                    carState = carStatus.decode()
                    if carState == "0":
                        cursor.execute('UPDATE cars SET Returned=%s WHERE id=%s', (carState, carID))
                        tbl = cursor.execute("SELECT * from cars")
                        print(cursor.fetchall())
                        #print("state changed to 0")
                    elif carState == "1":
                        cursor.execute('UPDATE cars SET Returned=%s WHERE id=%s', (carState, carID))
                        tbl = cursor.execute("SELECT * from cars")
                        print(cursor.fetchall())
                        #print("changed to 1")
                    loc = conn.recv(4096)
                    print(loc.decode())
                    cursor.execute('UPDATE cars SET Location=%s WHERE id=%s', (loc, carID))
                    input("I Exist To Stop Server From Crashing")
                if reply == "2":
                    carIdent = conn.recv(4096)
                    carID = carIdent.decode()
                    print(carID)
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    carStatus = conn.recv(4096)
                    carState = carStatus.decode()
                    if carState == "0":
                        cursor.execute('UPDATE cars SET Returned=%s WHERE id=%s', (carState, carID))
                        #tbl = cursor.execute("SELECT * from cars")
                        #print(cursor.fetchall())
                        #print("state changed to 0")
                    elif carState == "1":
                        cursor.execute('UPDATE cars SET Returned=%s WHERE id=%s', (carState, carID))

                    loc = conn.recv(4096)
                    print(loc.decode())
                    tbl = cursor.execute("SELECT * from cars")
                    print(cursor.fetchall())
                    input("I Exist To Stop Server From Crashing") 
                
                
            
            print("Disconnecting from client.")
        print("Closing listening socket.")
    print("Done.")
    main()




main()

