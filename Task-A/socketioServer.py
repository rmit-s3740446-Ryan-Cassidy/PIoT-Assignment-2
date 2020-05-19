from flask_socketio import SocketIO, send, emit
from flask import request
import time
import requests, json
from recognize_face import recognize

sios = SocketIO()

#Reset agent event
@sios.on('reset')
def handle_reset():
    return

#User credential authentication event
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
        return 'Success', message[0], cars
    else:
        return 'Fail', message[0], cars

#Face recognition event
@sios.on('facerecauth')
def handle_facerec(message):
    cars = []
    print('recieved face recognition auth')
    names = recognize(message)
    existsResponse = requests.post(request.host_url + "/users/" + names[0])
    exists = json.loads(existsResponse.text)
    if exists['message'] == "True":
        carResponse = requests.post(request.host_url + "/bookingsByUserAndDate/" + names[0])
        cars = json.loads(carResponse.text)
        return 'Success', names[0], cars
    else:
        return 'Fail', names[0], cars

#Update Car status event
@sios.on('carupdatestatus')
def handle_carupdatestatus(message):
    print('received updated car status')
    statusjson = {'id': message[0], 'status': message[1]}
    requests.post(request.host_url + "/updatecarstatus", json=statusjson)

#Update Car location event
@sios.on('carupdatelocation')
def handle_carupdatelocation(message):
    print('received updated car location')
    locationjson = {'id': message[0], 'location': message[1]}
    requests.post(request.host_url + "/updatecarlocation", json=locationjson)

#Following events are for unit testing purposes

#Event for testing credential login responses over socket
@sios.on('usercredauth', namespace='/test')
def handle_usercredtest(message):
    userLoginData = {'username':message[0], 'password':message[1]}
    authResponse = requests.post(request.host_url + "/loginUser", json=userLoginData)
    authData = json.loads(authResponse.text)
    if authData['message'] == 'Success':
        return message[0]
    else:
        return 'Fail'

#Event for testing facial recognition login response over socket
@sios.on('facerecauth', namespace='/test')
def handle_facerectest(message):
    names = recognize(message)
    existsResponse = requests.post(request.host_url + "/users/" + names[0])
    exists = json.loads(existsResponse.text)
    if exists['message'] == "True":
        return 'Success'
    else:
        return 'Fail'

#Event for testing receival of car location coordinates
@sios.on('carupdatelocation', namespace='/test')
def handle_carupdatelocationtest(message):
    if 'location' in message:
        return 'Success'
    else:
        return 'Fail'