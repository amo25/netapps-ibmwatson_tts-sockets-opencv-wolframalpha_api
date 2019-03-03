import socket
import sys
import pickle
from cryptography.fernet import Fernet
import hashlib
import wolframalpha
import ServerKeys
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from pydub.playback import play

text_to_speech = TextToSpeechV1(
    iam_apikey=ServerKeys.watson_api,
    url=ServerKeys.watson_url
)

host = ''
port = 50000
backlog = 5
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((host,port))
    myIP = socket.gethostbyname(socket.gethostname())
    print("[Checkpoint 01] Created socket at " + myIP + " on port " + str(port))
    s.listen(backlog)
    print("[Checkpoint 02] Listening for client connections")
except socket.error as message:
    if s:
        s.close()
    print("Could not open socket: " + str(message))
    sys.exit(1)
while 1:
    client, address = s.accept()    # blocks until message received
    print("[Checkpoint 03] Accepted client connection from " + str(address[0]) + " on port " + str(address[1]))
    data = client.recv(size)
    data = pickle.loads(data)
    print("[Checkpoint 04] Received data: " + str(data))

    #Question payload tuple: Encrypt/Decrypt key , Encrypted question text ,  MD5 hash of encrypted question text
    key = data[0]
    encrypted_question = data[1]
    checksum = data[2]

    #TODO: Check that hash matches recieved?

    #decrypt
    cipher_suite = Fernet(key)
    question = cipher_suite.decrypt(encrypted_question)
    print("[Checkpoint 05] Decrypt: Key: " + str(key) + " | Plain text: " + str(question))

    #TODO speak question
    print("[Checkpoint 06] Speaking Question: " + str(question))
    with open('question.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                str(question),
                'audio/wav',
                'en-US_AllisonVoice'
            ).get_result().content)

    song = AudioSegment.from_wav("question.wav")
    play(song)

    #TODO send question to Wolframalpha
    print("[Checkpoint 07] Sending question to Wolframalpha: " + str(question))
    appID = "3RRU62-VJHTLXYQ85"
    WAClient = wolframalpha.Client(appID)
    results = WAClient.query(question)

    #Receive answer from Wolframalpha
    answer = next(results.results).text
    answer = bytes(answer, 'utf-8')
    print("[Checkpoint 08] Recieved answer from Wolframalpha: " + str(answer))

    #Encrypt. I believe it's the same key, because we don't resend it
    cipher_text = cipher_suite.encrypt(answer)
    print("[Checkpoint 09] Encrypt: Key: " + str(key) + " | Ciphertext: " + str(cipher_text))

    #checksum
    hash = hashlib.md5(cipher_text).hexdigest()
    print("[Checkpoint 10] Generated MD5 Checksum: " + str(hash))

    #form data and pickle it. TODO do we have to pickle it?
    data = (cipher_text, hash)
    data = pickle.dumps(data)
    print("[Checkpoint 11] Sending answer: " + str(data))

    if data:
        client.send(data)
    client.close()