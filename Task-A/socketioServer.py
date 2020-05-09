from flask_socketio import SocketIO, send, emit
from flask import request
import time
import requests, json
from recognize_face import recognize

sios = SocketIO()

@sios.on('usercredauth')
def handle_usercred(message):
    cars = []
    print('received user cred auth: ')
    print(message)
    userLoginData = {'username':message[0], 'password':message[1]}
    authResponse = requests.post(request.host_url + "/loginUser", json=userLoginData)
    authData = json.loads(authResponse.text)
    if authData['message'] == 'Success':
        carResponse = requests.post(request.host_url + "/bookingsByUserAndDate/" + message[0])
        cars = json.loads(carResponse.text)
        return 'Success', cars
    else:
        return 'Fail', cars

@sios.on('faceregauth')
def handle_facecred(message):
    cars = []
    print('recieved face recognition auth: ')
    names = recognize(message)
    existsResponse = requests.post(request.host_url + "/users" + names[0])
    exists = json.loads(usersResponse.text)
    if exists['message'] == "True":
        carResponse = requests.post(request.host_url + "/bookingsByUserAndDate/" + names[0])
        cars = json.loads(carResponse.text)
        return 'Success', cars
    else:
        return 'Fail', cars




@sios.on('carupdatestatus')
def handle_carupdatestatus(message):
    print('received updated car status')
    print(message)

@sios.on('carupdatelocation')
def handle_carupdatelocation(message):
    print('received updated car location')
    print(message)
