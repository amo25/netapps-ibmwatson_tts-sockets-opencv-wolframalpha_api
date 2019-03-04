# Intializations 
# For IBMWatson 
watson_api = '29jbifcTEgGCn7RqC5RNcKjSHn1QiK2USY6Fi8R9uk_c'
watson_url = 'https://stream.watsonplatform.net/text-to-speech/api'

# Extra libraries used 
socket, sys, pickle,cryptography.fernet, Fernet, hashlib, 
watson_developer_cloud import TextToSpeechV1, pydub, AudioSegment
pydub.playback,pyzbar.pyzbar as pyzbar, cv2, subprocess

This project works as follows. The client reads a QR code using OpenCV and pyzbar.
From this QR code, it extracts a questions. It encrypts the message, generates 
a hash, and then creates a tuple with the encryption key, the encrypted message,
and the hash. It then pickles this tuple and sends it to the server. The server 
un-encapsulates all of this, speaks the question using IBM watson, and sends the question to Wolfram alpha. Wolfram alpha answers the question, and question is reencapsulated and sent back to the client (the other element of the encapsulation is the hash).
The client unencapsulates the message, and reads the answer using IBM Watson. 

