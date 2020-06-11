import socket
import datetime
import requests
import json
import os
#import bluetooth
import time
#from sense_hat import SenseHat

#ACCESS_TOKEN="o.DKJYYAlco6vYNs09Crn7jdR1bRtyAo5k"

ACCESS_TOKEN = "o.GAWSGwtueYnZUAUCnkolGM3u7qg8iGmC"

def pushBullet():
    
    title = "Hello Fren"
    body = "Goodbye Fren"
    
    send(title, body)
    

    







def send(title, body):
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
            
            
            
pushBullet()