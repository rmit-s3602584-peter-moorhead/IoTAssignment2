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
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import cv2



#HOST = input("Enter IP address of server: ")
def main():
    #Intialize time variable
    now = datetime.datetime.now()
    
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
                s.sendall(password.encode())
                carID = input("Car ID:")
                s.sendall(carID.encode())
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
                    print("ERROR")
                    break
                
            #FaceID section 
            elif sel == "2":
                dec = "2"
                s.sendall(dec.encode())
                name = faceID()
                s.sendall(name.encode())
                carID = input("Car ID:")
                s.sendall(carID.encode())
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
                    break
                s.sendall(time.encode())    
                break
                    
              
            else:
                print("Invalid Input")
                break
            break 
        print("Disconnecting from server.")
        msg = s.recv(4096)
        print(msg.decode())
    print("Done.")
    


#Gets current location of AgentPi
def getLoc():
    r = requests.get('http://ipinfo.io/loc')   
    re = r.text
    ret = re.rstrip('\n')
    return ret
        
  

#Reference
#https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
#Facial Recognition Function
def faceID():
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", default="encodings.pickle",
    help="path to serialized db of facial encodings")
    ap.add_argument("-r", "--resolution", type=int, default=240,
        help="Resolution of the video feed")
    ap.add_argument("-d", "--detection-method", type=str, default="hog",
        help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())

    # Load taken photos encodings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(args["encodings"], "rb").read())

    # Initialize and Turn on Web Cam
    print("[INFO] starting video stream...")
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)

    # Loop over video frames
    while True:
        # Grab frame from video stream
        frame = vs.read()

        # Convert from BGR to RGB and resize
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width = args["resolution"])

        # Detect the (x, y)-coordinates then compute facial embeddings
        boxes = face_recognition.face_locations(rgb, model = args["detection_method"])
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
    
main()
