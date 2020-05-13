#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
import datetime
import requests
import json
import os
import bluetooth
import time
from sense_hat import SenseHat


#HOST = input("Enter IP address of server: ")
def main():
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
                password = input("Password: ")
                s.sendall(password.encode())
                carID = input("Car ID:")
                s.sendall(carID.encode())
                #device_name = input("Enter the name of your phone: ")
                device_name = "Galaxy S9"
                print("test 4")
                reply = s.recv(4096)
                print("test 3")
                rep = reply.decode()
                print(rep)
                if rep == "true":
                    print("Welcome {}".format(username))
                    print("1. Unlock Car")
                    print("2. Return Car")
                    choice = input("Enter choice: ")
                    if choice == "1":                                     
                        #search(username, device_name)
                        #ip_address = os.popen('hostname -I').read()
                        #send_notification_via_pushbullet(ip_address, "Car Unlocked")
                        unl = "0"
                        s.sendall(unl.encode())
                        print("Car Unlocked")
                        location = getLoc()
                        s.sendall(location.encode())
                        break
                    elif choice == "2":
                        #search(username, device_name)
                        #ip_address = os.popen('hostname -I').read()
                        #send_notification_via_pushbullet(ip_address, "Car Returned")
                        ret = "1"
                        s.sendall(ret.encode())
                        print("Car Returned")
                        location = getLoc()
                        s.sendall(location.encode())                        
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





ACCESS_TOKEN="o.DKJYYAlco6vYNs09Crn7jdR1bRtyAo5k"

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')






def search(user_name, device_name):
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        nearby_devices = bluetooth.discover_devices()
        
        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        if device_address is not None:
            print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
            sense = SenseHat()
            temp = round(sense.get_temperature(), 1)
            sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.05)
            break
        else:
            print("Could not find target device nearby...")








def getLoc():
    r = requests.get('http://ipinfo.io/loc')   
    re = r.text
    ret = re.rstrip('\n')
    return ret
        
  
  
  
  
  
  
  
  
  
  
main()