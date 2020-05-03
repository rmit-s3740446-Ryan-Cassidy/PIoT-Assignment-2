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
    # Send user credential authentication attempt to Master
        sioc.emit('usercredauth', [email, password], callback = loginresp)
    else :
        exit("Other options NYI")

def loginresp(auth, cars) :
    global carList
    carList = cars
    if auth == 'Success' :
        print('Login Successful')
        time.sleep(1)
        selectCar()
    else : 
        print('Incorrect username or password')
        time.sleep(1)
        login()

def selectCar() :
    try :
        for index, car in enumerate(carList, start=1):
            print(index, ". " + car["Make"] + ' | ' + car["Type"])
        val = input("Please select a booked car: ")
        option = int(val) - 1
        if len(carList[option]) > 0:
            car = carList[option]
            print("Selected: " + car["Make"] + ' | ' + car["Type"])
        else:
            raise ValueError
    except ValueError:
        print("Not a valid selection")
        selectCar()
# Facial Recognition Login
# If true, sign in, else ask user again
# On sign in, send new car status to Master
# Google map check every 30 seconds
# Prompt user to do something to logout
# Send car status to Master on logout

if __name__ == "__main__":
    loadconfig()
    connect()
    login()
