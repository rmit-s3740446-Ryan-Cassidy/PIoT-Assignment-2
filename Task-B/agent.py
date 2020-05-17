import socket
import json
import sys
import threading
import time
import requests
import threading as th
import os.path
import base64
from threading import Event
from os import system, name
from PIL import Image
import socketio

class agentClient:
    def __init__(self):
        self.exit_loop = Event()
        self.sioc = socketio.Client()
    
    ip = None
    car = None
    username = None
    exit_loop = None
    geolocateURL = None
    login_type = True
    sioc = None

    # Load json configuration
    def load_config(self) :
        try:
            with open("config.json") as f:
                data = json.load(f)
                self.ip = "http://" + data["host"] + ":" + data["port"]
                self.geolocateURL = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + data['apikey']
        except Exception as e:
            print(str(e))
            sys.exit("Error when reading from Json.")

    # Clear console
    def clear(self) :
        # for windows 
        if name == 'nt': 
            _ = system('cls') 

        # for mac and linux
        else: 
            _ = system('clear') 

    # Socket to Master
    def connect(self) : 
        self.sioc.connect(self.ip)

    # Convert image to base64 string
    def image_to_str(self) :
        with open("image.jpg", "rb") as image:
            b64str = base64.b64encode(image.read())
            return b64str


    # Prompt user for login type
    def login(self) :
        self.clear()
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
            self.login_type = True 
            self.sioc.emit('usercredauth', [username, password], callback = self.loginresp)
        # Facial Recognition Login
        elif option == "2":
            # Detect image
            if os.path.exists("image.jpg"):
                image = self.image_to_str()
                self.login_type = False
                self.sioc.emit('facerecauth', image, callback = self.loginresp)
            else :
                print("No image found. Please place a selfie image labeled image.jpg in the directory")
                time.sleep(1)
                self.sioc.emit('reset', callback = self.login)
        #Close connection, close program
        elif option == "3":
            self.sioc.disconnect()
            sys.exit()
        else :
            #Bad user input, redirect back to login
            print("Incorrect input, please choose an option")
            time.sleep(1)
            self.sioc.emit('reset', callback = self.login)

    def loginresp(self, auth, username, cars) :
        car_list = cars
        # If true, sign in, else redirect back to login
        if auth == 'Success' :
            print('Login Successful. Hello ' + username)
            self.username = username
            time.sleep(1)
            # If no cars booked, redirect back to login
            if not car_list:
                print("No cars booked, please book a car on our site")
                time.sleep(2)
                self.sioc.emit('reset', callback = self.login)
            else:
                self.select_car(car_list)
        else :
            #Failed login. Redirect back to login 
            if self.login_type :
                print('Incorrect username or password')
            else:
                print('Facial Recognition failed')
            time.sleep(2)
            self.sioc.emit('reset', callback = self.login)

    def select_car(self, car_list) :
        # User selects booked car from list
        try :
            for index, car in enumerate(car_list, start=1):
                print(index, ". " + car["Make"] + ' | ' + car["Type"])
            val = input("Please select a booked car: ")
            option = int(val) - 1
            if len(car_list[option]) > 0:
                self.car = car_list[option]
                print("Selected: " + car["Make"] + ' | ' + car["Type"])
                time.sleep(2)
                print("Car unlocked")
                # Send selected car status to Master
                self.sioc.emit('carupdatestatus', [car['CarID'], 'Rented'], callback = self.location_update)
            else:
                raise ValueError
        except ValueError:
            print("Not a valid selection")
            self.select_car(car_list)

    #Method for looping until user presses enter
    def wait_for_user_input(self) :
        input()
        self.exit_loop.set()

    def location_update(self) :
        # Prompt user to do something to logout
        print("Press enter to return car")
        th.Thread(target=self.wait_for_user_input, args=(), name='wait_for_user_input', daemon=True).start()
        while not self.exit_loop.is_set():
            # Google map check every 30 seconds
            response = requests.post(self.geolocateURL)
            data = json.loads(response.text)
            self.sioc.emit('carupdatelocation', [self.car['CarID'], data])
            self.exit_loop.wait(30)
        # Send car status to Master on return, reset back to login
        print("Car returned, returning to login")
        self.exit_loop.clear()
        self.sioc.emit('carupdatestatus', [self.car['CarID'], 'Available'], callback = self.login)

if __name__ == "__main__":
    agent = agentClient()
    agent.load_config()
    agent.connect()
    agent.login()
