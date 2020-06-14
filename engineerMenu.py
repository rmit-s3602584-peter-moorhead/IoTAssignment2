#References
#RMIT Programming Internet of Things Tutorial code achive

import hashlib
from qrReader import scan
from bluetoothLogin import search
import MySQLdb.cursors


MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

    
connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


def searchLogin():
    """
    Function Searches for Phone,
    If known Phone Found, then displays menu,
    Allows Engineer to login to unlock car
    """
    while True:
        if search() == True:
            
            print("Engineer Logged In")
            
            print("Select Input")
            print("1. QR Login")
            
            sel = input("Enter Number: ")
            
            if sel == '1':
                menu()    
                return
            
            else:
                print("Invalid Login")
                return
            
            
            
        else:    
            print("Welcome to Car Hire - Engineers Login")
            print("Choose type of Log In")
            print("1. Engineer QR Login")
            print("2. Engineer Login")
            
            sel = input("Enter Number: ")
            if sel == '1':
                menu()
                return
                
            elif sel == '2':
                print("Engineer Login")
                val = cred()
                if val == True:
                    print("Account Verified")
                    pass
                elif val == False:
                    print("Account Invalid")
                    return
                else:
                    print("Error")
                menu()
                return
                    
            
            else:
                print("ERROR Invalid Login")
                return


def cred():
    """
    Function accepts input and verifies user login with database.
    If user enters correct data, function returns true. 
    """
    print("Enter Login Credentials")
    us = input("Enter Username: ")
    pa = input("Enter Password: ")
    salt = "lcyysk2NAQOJCHxkM1fA"
    saltPass = pa+salt
    hashPass = hashlib.sha256(saltPass.encode())
    enPa = hashPass.hexdigest()
    
    utype = "Engineer"
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)          
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s AND typeOfUser=%s', (us, enPa, utype, ))
    
                    
    account = cursor.fetchone()
            
    if account:
        return True
    else:
        return False

def menu():
    """
    Function displays menu that appears after user logs in.
    """
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    
    print("Using Camera To Scan QR Code")
    acc = scan()
    print("{} has Logged In".format(acc))
    
    
    cursor.execute('SELECT * FROM users WHERE username=%s', (acc, ))
    profile = cursor.fetchone()
    
    print()
    print("Engineers Profile")
    print(profile)
    print()
    
    
    print()
    carID = input("Enter Car ID: ")
    print()
    

    carStr = "Repairing"
                    
    cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
    connection.commit()
    
    print()
    print("Select Choice")
    print("1. Car Fixed - Return Car")
    print("2. Log Out")
    print()
    
    sel = input("Enter Number: ")
    
    if sel == '1':
        carStr = "Returned"
        rep = acc
        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
        cursor.execute('UPDATE cars SET broken=%s WHERE id=%s', (rep, carID))
        connection.commit()
        print("Car Updated - Logging Out")
        return
    
    if sel == '2':
        print("User has logged out")
        return
    else:
        print("Invalid Input - Logging Out")
        return



searchLogin()       
