import socket
import json
import sys
import threading
import time
import requests
import threading as th
import os.path
import base64
from os import system, name
from pil import Image
from socketioClient import sioc, auth, carList

ip = None
car = None
looping = True
geolocateURL = None
login_type = True

# Load json configuration
def load_config() :
    try:
        with open("config.json") as f:
            global ip
            global geolocateURL
            data = json.load(f)
            ip = "http://" + data["host"] + ":" + data["port"]
            geolocateURL = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + data['apikey']
    except Exception as e:
        print(str(e))
        sys.exit("Error when reading from Json.")

# Clear console
def clear() :
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux
    else: 
        _ = system('clear') 

# Socket to Master
def connect() : 
    sioc.connect(ip)

# Convert image to base64 string
def image_to_str() :
    with open("image.jpg", "rb") as image:
        b64str = base64.b64encode(image.read())
        return b64str


# Prompt user for login type
def login() :
    global login_type
    clear()
    print("Welcome to Agent Car Login")
    print("1. User Credential Login")
    print("2. Facial Recognition Login")
    print("3. Exit")
    option = input("Select an option: ")
    # User Credential Login
    if option == '1' :
        username = input('Please enter username: ')
        password = input('Please enter password: ')
    # Send user credential authentication attempt to Master
        login_type = True 
        sioc.emit('usercredauth', [username, password], callback = loginresp)
    # Facial Recognition Login
    elif option == "2":
        # Detect image
        if os.path.exists("image.jpg"):
            image = image_to_str()
            login_type = False
            sioc.emit('facerecauth', image, callback = loginresp)
        else :
            print("No image found. Please place a selfie image labeled image.jpg in the directory")
            time.sleep(1)
            sioc.emit('reset', callback = login)
    elif option == "3":
        sioc.disconnect()
        sys.exit()
    else :
        print("Incorrect input, please choose an option")
        time.sleep(1)
        sioc.emit('reset', callback = login)

def loginresp(auth, username, cars) :
    car_list = cars
    # If true, sign in, else redirect back to login
    if auth == 'Success' :
        print('Login Successful. Hello ' + username)
        time.sleep(1)
        # If no cars booked, redirect back to login
        if not car_list:
            print("No cars booked, please book a car on our site")
            time.sleep(2)
            sioc.emit('reset', callback = login)
        else:
            select_car(car_list)
    else : 
        if login_type :
            print('Incorrect username or password')
        else:
            print('Facial Recognition failed')
        time.sleep(2)
        sioc.emit('reset', callback = login)

def select_car(car_list) :
    global car
    # User selects booked car from list
    try :
        for index, car in enumerate(car_list, start=1):
            print(index, ". " + car["Make"] + ' | ' + car["Type"])
        val = input("Please select a booked car: ")
        option = int(val) - 1
        if len(car_list[option]) > 0:
            car = car_list[option]
            print("Selected: " + car["Make"] + ' | ' + car["Type"])
            time.sleep(2)
            print("Car unlocked")
            sioc.emit('carupdatestatus', [car['CarID'], 'Rented'], callback = location_update)
            # Send selected car status to Master
        else:
            raise ValueError
    except ValueError:
        print("Not a valid selection")
        select_car(car_list)

def wait_for_user_input() :
    global looping
    input()
    looping = False

def location_update() :
    # Prompt user to do something to logout
    print("Press enter to return car")
    th.Thread(target=wait_for_user_input, args=(), name='wait_for_user_input', daemon=True).start()
    while looping:
        # Google map check every 30 seconds
        response = requests.post(geolocateURL)
        data = json.loads(response.text)
        sioc.emit('carupdatelocation', [car['CarID'], data])
        time.sleep(30)
        # Send car status to Master on return, reset back to login
    print("Car returned, returning to login")
    sioc.emit('carupdatestatus', [car['CarID'], 'Available'], callback = login)

if __name__ == "__main__":
    load_config()
    connect()
    login()
