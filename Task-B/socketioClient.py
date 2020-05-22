"""
socketioClient.py
======================
The socketio client class.
"""
import socketio

class socketClient:
    """Class to register socket events and print appropriate message to console.
    """
    sioc = socketio.Client()

    # Socket Events

    @sioc.event
    def connect(self) :
        print("Connection Successful")

    @sioc.event
    def connect_error(self) :
        print("Connection error")

    @sioc.event
    def disconnect(self) :
        print("Disconnected from server")
