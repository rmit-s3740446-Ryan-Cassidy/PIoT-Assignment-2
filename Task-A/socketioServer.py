from flask_socketio import SocketIO, send, emit
import time

sios = SocketIO()


@sios.on('message')
def handle_message(message):
    print('received message: ' + message)
    time.sleep(2)
    send(message)