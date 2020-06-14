# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
import MySQLdb.cursors
import hashlib
def serverAgent():
    """
    Function Hosts Server for Agent Pi,
    Connects to MySQL Database to update location and car state
    Verifies Users Credentials, 
    """
    
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
    #Create INET socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind to public host and port
        s.bind(ADDRESS)
        #Create Server
        s.listen()
        #define connection variables
        print("Listening on {}...".format(ADDRESS))
        conn, addr = s.accept()
        with conn:
            print("Connected to {}".format(addr))
            
            while True:
                data = conn.recv(4096)
                if not data:
                    print("Invalid Input Received")
                    break
                print(data.decode())
                reply = data.decode()
                print(reply)
                #If user enters credentials
                if reply == "1":
                    #Receive username and password to verify user 
                    username = conn.recv(4096)
                    if not username:
                        print("Invalid Input Received")
                        break
                    us = username.decode()
                    print("username is: {}".format(us))
                    
                    password = conn.recv(4096)
                    if not password:
                        print("Invalid Input Received")
                        break
                    pa = password.decode()
                    print("password is: {}".format(pa))
                    
                    carIdent = conn.recv(4096)
                    if not carIdent:
                        print("Invalid Input Received")
                        break
                    
                    carID = carIdent.decode()
                    print("Car ID is: {}".format(carID))
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (us, pa,))
                    
                    account = cursor.fetchone()
            
                    if account:
                        msg = "true"
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                        return
                        
                    cursor.execute('SELECT * FROM cars WHERE id = %s' , (carID, ))
                    carVerify = cursor.fetchone()
                    if carVerify:
                        msg = "true"
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                        return
                        
                    print("{} has logged in".format(us))
                    conn.sendall(msg.encode())
                    
                    carStatus = conn.recv(4096)
                    if not carStatus:
                        print("Invalid Input Received")
                        break
                    
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
                    else:
                        print("User entered Invalid Input - Disconnecting")
                        break
                    
                    location = conn.recv(4096)
                    if not location:
                        print("Invalid Input Received")
                        break
                    
                    loc = (location.decode())
                    print(loc)
                    cursor.execute('UPDATE cars SET longlat=%s WHERE id=%s', (loc, carID))
                    connection.commit()
                    cursor.execute("SELECT * from cars") 
                    print(cursor.fetchall())
                    
                    
                    
                    
                #If user uses faceID    
                elif reply == "2":
                    user = conn.recv(4096)
                    if not user:
                        print("Invalid Input Received")
                        break
                    
                    us = user.decode()
                    if us == "Invalid":
                        print("Invalid User - Disconecting")
                        return
                    
                    print("{} has logged in".format(us))
                    carIdent = conn.recv(4096)
                    if not carIdent:
                        print("Invalid Input Received")
                        break
                    
                    carID = carIdent.decode()
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM cars WHERE id = %s' , (carID, ))
                    carVerify = cursor.fetchone()
                    if carVerify:
                        msg = "true"
                        conn.sendall(msg.encode())
                    else:
                        msg = "false"
                        conn.sendall(msg.encode())
                        print("Car Id Invalid = Disconnecting")
                        return
                    
                    print("Car ID is: {}".format(carID))
                    
                    carStatus = conn.recv(4096)
                    if not carStatus:
                        print("Invalid Input Received")
                        break
                    
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
                    else:
                        print("User entered Invalid Input - Disconnecting")
                        break
                    
                    #Get and Update location of AgentPi
                    location = conn.recv(4096)
                    if not location:
                        print("Invalid Input Received")
                        break
                    
                    loc = (location.decode())
                    print(loc)
                    cursor.execute('UPDATE cars SET longlat=%s WHERE id=%s', (loc, carID))
                    connection.commit()
                    cursor.execute("SELECT * from cars") 
                    print(cursor.fetchall())
                else:
                    print("User entered Invalid Input - Disconnecting")
                    break
                
                time = conn.recv(4096)
                if not time:
                        print("Invalid Input Received")
                        break
                    
                print(time.decode())
                break
                    
            #Send log out message to User
            msg = "You Have Been Logged Out"
            conn.sendall(msg.encode())
            print("User has disconnected")
            #conn.shutdown(socket.SHUT_WR)
            #conn.close()
        print("Closing listening socket.")
        s.shutdown(socket.SHUT_WR)
        s.close()
    print("Done.")
    




serverAgent()

