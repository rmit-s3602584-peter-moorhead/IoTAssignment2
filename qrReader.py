## References
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/


from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2


def scan():
    """
    Function uses webcam to scan for barcodes,
    if found, converts to string and returns value. 
    """
    #initialize camera feed
    print("[INFO] starting video stream...")
    vs = VideoStream(src = 0).start()
    time.sleep(2.0)

    found = set()

    #loop over camera feed frames
    while True:
            #resize video frame to 400px width
            frame = vs.read()
            frame = imutils.resize(frame, width = 400)

            #find and decode barcodes
            barcodes = pyzbar.decode(frame)

            #loops through detected barcodes
            for barcode in barcodes:
                    #converts barcode into string
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    #returns string
                    return barcodeData



