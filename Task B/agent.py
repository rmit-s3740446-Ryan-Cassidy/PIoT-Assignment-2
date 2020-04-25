import socket
import json
import sys
import threading
import socketio

host = None
port = None
sio = socketio.Client()

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
sio.connect('localhost:65432')
print('my sid is', sio.sid)
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

@sio.event
def message(data) :
    print("I received a message!")

@sio.event
def connect() :
    print("Connection Successful")

@sio.event
def connect_error() :
    print("Connection error")

@sio.event
def disconnect() :
    print("Disconnected from server")