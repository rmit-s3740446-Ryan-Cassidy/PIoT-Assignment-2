import socketio

class socketClient:
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
