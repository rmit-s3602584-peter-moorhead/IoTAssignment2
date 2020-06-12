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







def main():
    while True:

        print("Welcome to Car Hire")
        print("Choose type of Log In")
        print("1. Engineer QR Login")
        print("2. Enginer Login")
        
        sel = input("Enter Number: ")
        if sel == '1':
            print("Using Camera To Scan QR Code")
        if sel == '2':
            print("Engineer Login")
        
        else:
            print("ERROR Invalid Login")
            return
            