"""
agent.py
=====================
This script is run on agent raspberry pi.
"""
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
    """The agentClient class.

    Attributes:
        ip(str): IP address of master pi to connect to.
        car(Car): The car selected by user.
        username(str): Username of logged in user.
        geolocateURL(str): Google maps geolocation api url.
        sioc(obj): socketio object used for communication.
    """
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


    def load_config(self) :
        """ Loads json config from config.json
        """
        try:
            with open("config.json") as f:
                data = json.load(f)
                self.ip = "http://" + data["host"] + ":" + data["port"]
                self.geolocateURL = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + data['apikey']
        except Exception as e:
            print(str(e))
            sys.exit("Error when reading from Json.")


    def clear(self) :
        """Clears console so that console is clean initially.
        """
        # for windows 
        if name == 'nt': 
            _ = system('cls') 

        # for mac and linux
        else: 
            _ = system('clear') 


    def connect(self) : 
        """Initialize socket connection to master pi.
        """
        self.sioc.connect(self.ip)

    # Convert image to base64 string
    def image_to_str(self) :
        """Convert image to base64 encoded string.

        Returns:
            str: base64 encoded image
        """
        with open("image.jpg", "rb") as image:
            b64str = base64.b64encode(image.read())
            return b64str


    # Prompt user for login type
    def login(self) :
        """Display user menu on console.
        """
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
        """Process login response

        Args:
            auth (str): Authorization message returned.
            username (str): username of user who logged in.
            cars (list): list of cars booked by the user.
        """
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
        """Display car list from booking history to unlock a car.

        Args:
            car_list (list): list of cars in bookings by user

        Raises:
            ValueError: On invalid option selection.
        """

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
        except (ValueError, IndexError) as e:
            print("Not a valid selection")
            self.select_car(car_list)


    def wait_for_user_input(self) :
        """Accept input from user until they press "Enter"
        """
        input()
        self.exit_loop.set()

    def location_update(self) :
        """Return booked car.
        """
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
