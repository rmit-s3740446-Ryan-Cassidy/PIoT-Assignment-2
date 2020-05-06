import socket
import json
import sys
import threading
import time
import threading as th
from socketioClient import sioc, auth, carList

ip = None
carList = None
car = None
looping = True

def load_config() :
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
    # Facial Recognition Login
    else :
        exit("Other options NYI")

def loginresp(auth, cars) :
    global carList
    carList = cars
    # If true, sign in, else ask user again
    if auth == 'Success' :
        print('Login Successful')
        time.sleep(1)
        selectCar()
    else : 
        print('Incorrect username or password')
        time.sleep(1)
        login()

def select_car() :
    global car
    # User selects booked car from list
    try :
        for index, car in enumerate(carList, start=1):
            print(index, ". " + car["Make"] + ' | ' + car["Type"])
        val = input("Please select a booked car: ")
        option = int(val) - 1
        if len(carList[option]) > 0:
            car = carList[option]
            print("Selected: " + car["Make"] + ' | ' + car["Type"])
            time.sleep(1)
            print("Car unlocked")
            # Send selected car status to Master
        else:
            raise ValueError
    except ValueError:
        print("Not a valid selection")
        selectCar()

def wait_for_user_input() :
    global looping
    input()
    looping = False

def location_update() :
    # Prompt user to do something to logout
    print("Press enter to lock car")
    th.Thread(target=wait_for_user_input, args=(), name='wait_for_user_input', daemon=True).start()
    while loop:
        # Google map check every 30 seconds

    # Send car status to Master on logout

if __name__ == "__main__":
    load_config()
    connect()
    login()
