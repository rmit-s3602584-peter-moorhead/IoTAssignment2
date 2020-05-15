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
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import cv2



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
    



def getLoc():
    r = requests.get('http://ipinfo.io/loc')   
    re = r.text
    ret = re.rstrip('\n')
    return ret
        
  

## Reference
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages


def faceID():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", default="encodings.pickle",
    help="path to serialized db of facial encodings")
    ap.add_argument("-r", "--resolution", type=int, default=240,
        help="Resolution of the video feed")
    ap.add_argument("-d", "--detection-method", type=str, default="hog",
        help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())

    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(args["encodings"], "rb").read())

    # initialize the video stream and then allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream
        frame = vs.read()

        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width = args["resolution"])

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb, model = args["detection_method"])
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    break

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key = counts.get)
                

            # update the list of names
            names.append(name)
       # loop over the recognized faces
        for name in names:
            # print to console, identified person
            print("Person found: {}".format(name))
            # Set a flag to sleep the cam for fixed time
            return name
            
        break
    # do a bit of cleanup
    vs.stop()
    
    
  
  
  
  
  
  
  
  
main()