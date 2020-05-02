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
    response = requests.post(request.host_url + "/loginUser", json=userLoginData)
    data = json.loads(response.text)
    if data['message'] == 'Success':
        return 'Success'
    else:
        return 'Fail'
