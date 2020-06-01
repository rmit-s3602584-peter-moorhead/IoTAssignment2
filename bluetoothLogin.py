import socket
import datetime
import requests
import json
import os
import bluetooth
import time
from sense_hat import SenseHat
from dbEngineer import engineer




def search():
    while True:
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        nearby = bluetooth.discover_devices()

        for mac_address in nearby:
            while bluetooth.lookup_name(mac_address, timeout=5):
                if engineer.matchMac(mac_address) == True:
                    
                    print("Unlocking Vehicle")
                    engineer.unlockCars()
                    print(mac_address)
                    return True
                else:
                    print("No Engineer Nearby")
            
            
        else:
            print("Could not find target device nearby...")
            

search()