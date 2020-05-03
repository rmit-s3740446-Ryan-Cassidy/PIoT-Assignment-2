import socket
import json
import sys
import threading
import time
from socketioClient import sioc, auth, carList

ip = None
carList = None

def loadconfig() :
    try:
        with open("config.json") as f:
            global ip
            data = json.load(f)
            print(data['host'])
            ip = "http://" + data["host"] + ":" + data["port"]
    except Exception as e:
        print(str(e))
        sys.exit("Error when reading from Json.")


# Socket to Master
def connect() : 
    sioc.connect(ip)
    print('my sid is', sioc.sid)


# Prompt user for login type
def login() :
    print("1. User Credentials")
    print("2. Facial Recognition")
    option = input("Select authentication method: ")
    # User Credential Login
    if option == '1' :
        email = input('Please enter email: ')
        password = input('Please enter password: ')
    # Emit authentication event
        sioc.emit('usercredauth', [email, password], callback = loginresp)
    else :
        exit("Other options NYI")

def loginresp(data) :
    global carList
    print(data[0])
    carList = data[1]
    if data[0] == 'Success' :
        print('Login Successful')
    else : 
        print('Incorrect username or password')
        time.sleep(1)
        login()
# Facial Recognition Login
# Send authentication attempt to Master
# If true, sign in, else ask user again
# On sign in, send new car status to Master
# Google map check every 30 seconds
# Prompt user to do something to logout
# Send car status to Master on logout

if __name__ == "__main__":
    loadconfig()
    connect()
    login()
