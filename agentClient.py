# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket
import datetime
import requests
import json
import os
import time
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import cv2
import hashlib


#HOST = input("Enter IP address of server: ")
def clientAgent():
    """
    Function connects to host server through IP and Port.
    User enters credentials and waits for server to verify.
    Once verified user can unlock or lock car.
    """
    #Intialize time variable
    now = datetime.datetime.now()
    #HOST = input("Enter IP address of server: ")
    #HOST = "110.144.55.243"
    HOST = "192.168.0.192" # The server's hostname or IP address.
    PORT = 65000         # The port used by the server.
    ADDRESS = (HOST, PORT)
    #Opens socket for connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.") 
        #print menu
        while True:
            time = (now.strftime("%Y-%m-%d %H:%M:%S"))
            print("Welcome to Car Hire")
            print("Choose type of Log In")
            print("1. Log In With Credentials")
            print("2. Log In With FaceID")
            sel = input("Enter Number: ")
            #Credentials Section
            if sel == "1":
                dec = "1"
                s.sendall(dec.encode())
                print("Enter Credentials")
                username = input("Username: ")
                s.sendall(username.encode())
                password = input("Password: ")
                salt = "lcyysk2NAQOJCHxkM1fA"
                saltPass = password+salt
                hashPass = hashlib.sha256(saltPass.encode())
                enPa = hashPass.hexdigest()
                s.sendall(enPa.encode())
                carID = input("Car ID:")
                s.sendall(carID.encode())
                device_name = "Galaxy S9"
                reply = s.recv(4096)
                if not reply:
                    print("Invalid Input Received")
                    break
                rep = reply.decode()
                print(rep)
                if rep == "true":
                    print("Welcome {}".format(username))
                    print("1. Unlock Car")
                    print("2. Return Car")
                    choice = input("Enter choice: ")
                    if choice == "1":                                     
                        unl = "0"
                        s.sendall(unl.encode())
                        print("Car Unlocked")
                        location = getLoc()
                        s.sendall(location.encode())
                        
                    elif choice == "2":
                        ret = "1"
                        s.sendall(ret.encode())
                        print("Car Returned")
                        location = getLoc()
                        s.sendall(location.encode())                        
                    s.sendall(time.encode())
                    break    
                elif rep == "false":
                    print("Incorrect Login")
                    break
                else:
                    print("ERROR - Invalid Input - ERROR")
                    break
                
            #FaceID section 
            elif sel == "2":
                dec = "2"
                s.sendall(dec.encode())
                name = None
                name = faceID()
                if name == None:
                    name = "Invalid"
                    print("Invalid User - Disconnecting")
                    s.sendall(name.encode())
                    return
                s.sendall(name.encode())
                carID = input("Car ID:")
                s.sendall(carID.encode())
                msg = s.recv(4096)
                m = msg.decode()
                if m == "false":
                    print("Invalid Car Id - Disconnecting")
                    return
                elif m == "true":
                    pass
                print("1. Unlock Car")
                print("2. Return Car")
                choice = input("Enter choice: ")
                if choice == "1":                                     
                    unl = "0"
                    s.sendall(unl.encode())
                    print("Car Unlocked")
                    location = getLoc()
                    s.sendall(location.encode())
                    
                elif choice == "2":
                    ret = "1"
                    s.sendall(ret.encode())
                    print("Car Returned")
                    location = getLoc()
                    s.sendall(location.encode())  
                else:
                    print("Invalid Input")
                    return
                s.sendall(time.encode())    
                break
                    
              
            else:
                print("Invalid Input")
                return
             
        print("Disconnecting from server.")
        msg = s.recv(4096)
        if not msg:
            print("Invalid Input Received")
            
        print(msg.decode())
        s.shutdown(socket.SHUT_WR)
        s.close()
    print("Done.")
    


#Gets current location of AgentPi
def getLoc():
    """
    Function returns location of AgentPi
    """
    r = requests.get('http://ipinfo.io/loc')   
    re = r.text
    ret = re.rstrip('\n')
    return ret
        
  

#Reference
#https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
#Facial Recognition Function
def faceID():
    """
    Function uses webcam to take images of face,
    then encodes and matches data to dataset
    returns name of recognized faces
    """

    # Load taken photos encoding
    print("Preparing encodings...")
    data = pickle.loads(open("encodings.pickle", "rb").read())

    # Initialize and Turn on Web Cam
    print("Video Stream On")
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)

    # Loop over video frames
    while True:
        # Grab frame from video stream
        frame = vs.read()

        # Convert from BGR to RGB and resize
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width = 240)

        # Detect the (x, y)-coordinates then compute facial embeddings
        boxes = face_recognition.face_locations(rgb, model = "hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # Loop facial embeddings
        for encoding in encodings:
            # Try to match face with encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"

            # Check for matches
            if True in matches:
                # Count number of face matches
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    break

                # Determine most likely recognized faced based on number of votes
                name = max(counts, key = counts.get)
                

            # Update matched face to names
            names.append(name)
       # Print all matches
        for name in names:
            # return name of Matched user
            print("Person found: {}".format(name))
            return name
            
        break
    # Stop Video Stream
    vs.stop()
    
clientAgent()
