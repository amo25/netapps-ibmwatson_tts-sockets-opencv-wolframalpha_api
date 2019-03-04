import socket
import sys
import pickle
from cryptography.fernet import Fernet
import hashlib
import ClientKeys
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from pydub.playback import play
import pyzbar.pyzbar as pyzbar
import cv2
import subprocess

#print(str(len(sys.argv)))

#arguments
if len(sys.argv) == 7:
    host = sys.argv[2]
    port = int(sys.argv[4])
    size = int(sys.argv[6])
else:
    print("Argument format error. Use: python3 client.py -sip <SERVER_IP> -sp <SERVER_PORT> -z <SOCKET_SIZE>")

text_to_speech = TextToSpeechV1(
    iam_apikey=ClientKeys.watson_api,
    url=ClientKeys.watson_url
)

#host = '172.30.90.27'   #todo modify. Set to server IP
#port = 50000    #todo modify?
#size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
#except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open the socket: " + str(message))
    sys.exit(1)

print("[Checkpoint 01] Connecting to " + str(host) + " on port " + str(port))

#read the qr code
#TODO may need to modify the QR code stuff to happen live and have some logic
#todo paste stuff here
#check that it's a question by seeing if last character is a question mark
print("[Checkpoint 02] Listening for QR codes from RPi Camera that contain questions")
#prob a while loop with a break when a question is encountered
#take an image
subprocess.call(["raspistill", "-o", "Camera_QR_Code.jpg"])
#read image
im = cv2.imread('Camera_QR_Code.jpg')
#Find qr codes and barcodes in the image
decodedObjects = pyzbar.decode(im)
for obj in decodedObjects:
    question = obj.data

#question = b"Who is the president of the US?"     #todo replace
print("[Checkpoint 03] New Question: " + str(question))

#encrypt the question
key = Fernet.generate_key() #generate and arbitrary key
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(question)
print("[Checkpoint 04] Encrypt: Generated Key: " + str(key) + " | Cipher text: " + str(cipher_text))

#create hash
hash = hashlib.md5(cipher_text).hexdigest()

#create and pickle the tuple
data = (key, cipher_text, hash)
data = pickle.dumps(data)

#send the data
print("[Checkpoint 05] Sending data: " + str(data))
s.send(data)

#recieve data
data = s.recv(size)
print("[Checkpoint 06] Received data: " + str(data))

#depickle and decrypt. TODO do we have to depickle?
#todo do we have to check the hash?
data = pickle.loads(data)
answer = data[0]
hash = data[1]
answer = cipher_suite.decrypt(answer)
print("[Checkpoint 07] Decrypt: Using Key: " + str(key) + " | Plain text: " + str(answer))


#TODO speak answer
print("[Checkpoint 08] Speaking Answer: " + str(answer))
with open('answer.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            str(answer),
            'audio/wav',
            'en-US_AllisonVoice'
        ).get_result().content)

song = AudioSegment.from_wav("answer.wav")
play(song)


s.close()
#print ('Received:', str(data))