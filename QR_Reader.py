import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

# Read image. TODO link to camera
im = cv2.imread('Alex_QR_Code.png')

#Find qr codes and barcodes in the image
decodedObjects = pyzbar.decode(im)

# Print results. #TODO remove print and send object data to the next thing. Maybe use obj.type for error checking
for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data, '\n')