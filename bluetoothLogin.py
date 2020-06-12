import socket
import datetime
import requests
import json
import os
import bluetooth
import time
from sense_hat import SenseHat
from dbEngineer import engineer
import MySQLdb.cursors
import hashlib

MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

    
connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


def search():
    while True:
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        nearby = bluetooth.discover_devices()
        print("hi")

        for mac_address in nearby:
            print("ff")
            while bluetooth.lookup_name(mac_address, timeout=5):
                mac = mac_address
            
                
                #cursor.execute('SELECT * FROM users WHERE MAC= %s', (mac,)):
                #account = cursor.fetchone()
                
                #if engineer.matchMac(mac) == True:
                if account:
                    print("Found Engineer")
                    
                    print("Unlocking Vehicle")
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    carStr = "Repairing"
                    carID = "3"
                    cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                    connection.commit()
                    print(mac_address)
                    return True
                else:
                    print("No Engineer Nearby")
                    return False
            
            
        else:
            print("Could not find target device nearby...")
            return False
            

search()