# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
import MySQLdb.cursors
import hashlib
def main():
    
    #Database connection
    MYSQL_HOST = "35.244.72.137"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_DB = "Peopl"

    
    connection = None
    if(connection == None):
        connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


    HOST = ""    # Empty means it accepts any IP
    PORT = 65000 # Port to listen on
    ADDRESS = (HOST, PORT)
    #open socket for connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()
        #define connection variables
        print("Listening on {}...".format(ADDRESS))
        conn, addr = s.accept()
        with conn:
            print("Connected to {}".format(addr))
            
            while True:
                data = conn.recv(4096)
                
                print(data.decode())
                reply = data.decode()
                print(reply)
                #If user enters credentials
                if reply == "1":
                    #Receive username and password to verify user 
                    username = conn.recv(4096)
                    us = username.decode()
                    print("username is: {}".format(us))
                    password = conn.recv(4096)
                    pa = password.decode()
                    print("password is: {}".format(pa))
                    carIdent = conn.recv(4096)
                    carID = carIdent.decode()
                    print("Car ID is: {}".format(carID))
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (us, pa,))
                    
                    account = cursor.fetchone()
            
                    if account:
                        msg = "true"
                    else:
                        msg = "false"
                        break
                    print("{} has logged in".format(us))
                    conn.sendall(msg.encode())
                    
                    carStatus = conn.recv(4096)
                    carState = carStatus.decode()
                    #Change car state to 0
                    if carState == "0":
                        carStr = "In Use"
                        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                        connection.commit()
                        #print("state changed to 0")
                    #Change car state to 1
                    elif carState == "1":
                        carStr = "Returned"
                        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                        connection.commit()
                        #print("changed to 1")
                    #Get and Update location of AgentPi
                    location = conn.recv(4096)
                    loc = (location.decode())
                    print(loc)
                    cursor.execute('UPDATE cars SET longlat=%s WHERE id=%s', (loc, carID))
                    connection.commit()
                    cursor.execute("SELECT * from cars") 
                    print(cursor.fetchall())
                #If user uses faceID    
                elif reply == "2":
                    user = conn.recv(4096)
                    us = user.decode()
                    print("{} has logged in".format(us))
                    carIdent = conn.recv(4096)
                    carID = carIdent.decode()
                    print("Car ID is: {}".format(carID))
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    carStatus = conn.recv(4096)
                    carState = carStatus.decode()
                    #Change car state to 0
                    if carState == "0":
                        carStr = "In Use"
                        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                        connection.commit()
                    #Change car state to 1
                    elif carState == "1":
                        carStr = "Returned"
                        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                        connection.commit()
                    #Get and Update location of AgentPi
                    location = conn.recv(4096)
                    loc = (location.decode())
                    print(loc)
                    cursor.execute('UPDATE cars SET longlat=%s WHERE id=%s', (loc, carID))
                    connection.commit()
                    cursor.execute("SELECT * from cars") 
                    print(cursor.fetchall())
                time = conn.recv(4096)
                print(time.decode())
                break
            #Send log out message to User
            msg = "You Have Been Logged Out"
            conn.sendall(msg.encode())
            print("User has disconnected")
        print("Closing listening socket.")
    print("Done.")
    




main()

