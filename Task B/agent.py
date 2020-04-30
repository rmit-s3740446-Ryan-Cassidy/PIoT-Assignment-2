import socket
import json
import sys
import threading
import time
from socketioClient import sioc

ip = None

def loadconfig(self) :
    try:
        with open("config.json") as f:
            data = json.load(f)
            self.ip = "http://" + data["HOST"] + ":" + data["PORT"]
    except Exception as e:
        print(str(e))
        sys.exit("Error when reading from Json.")
loadconfig
# Socket to Master
sioc.connect(ip)
print('my sid is', sioc.sid)

while True :
# Prompt user for login type
    print("1. User Credentials")
    print("2. Facial Recognition")
    option = input("Select authentication method: ")
    if option == '1' :
        email = input('Please enter email: ')
        password = input('Please enter password: ')
    else :
        exit("Other options NYI")
    
# User Credential Login
# Facial Recognition Login
# Send authentication attempt to Master
# If true, sign in, else ask user again
# On sign in, send new car status to Master
# Google map check every 30 seconds
# Prompt user to do something to logout
# Send car status to Master on logout