from flask_socketio import SocketIO, send, emit
from flask import request
import time
import requests, json

sios = SocketIO()

@sios.on('usercredauth')
def handle_usercred(message):
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
        return 'Fail'

@sios.on('carupdatestatus')
def handle_carupdatestatus(message):
    print('received updated car status')
    print(message)

@sios.on('carupdatelocation')
def handle_carupdatelocation(message):
    print('received updated car location')
    print(message)
