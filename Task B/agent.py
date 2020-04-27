import socket
import json
import sys
import threading
import time
from socketioClient import sioc

host = None
port = None

def loadconfig(self) :
    try:
        with open("config.json") as f:
            data = json.load(f)
            self.host = data["HOST"]
            self.port = data["PORT"]
    except Exception as e:
        print(str(e))
        sys.exit("Error when reading from Json.")
loadconfig
# Socket to Master
sioc.connect('http://192.168.1.225:5000')
print('my sid is', sioc.sid)

while True:
    sioc.emit('message', 'hello there')
    time.sleep(5)

# Prompt user for login type
    # print("1. User Credentials")
    # print("2. Facial Recognition")
    # print("Select authentication method: ")
# User Credential Login
# Facial Recognition Login
# Send authentication attempt to Master
# If true, sign in, else ask user again
# On sign in, send new car status to Master
# Google map check every 30 seconds
# Prompt user to do something to logout
# Send car status to Master on logout