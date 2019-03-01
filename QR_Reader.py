import pyzbar.pyzbar as pyzbar

import numpy as np

import cv2
import subprocess

#take an image
subprocess.call(["raspistill", "-o", "Camera_QR_Code.jpg"])

# Read image.

im = cv2.imread('Camera_QR_Code.jpg')



#Find qr codes and barcodes in the image

decodedObjects = pyzbar.decode(im)



# Print results. #TODO remove print and send object data to the next thing. Maybe use obj.type for error checking

for obj in decodedObjects:

    print('Type : ', obj.type)

    print('Data : ', obj.data, '\n')
