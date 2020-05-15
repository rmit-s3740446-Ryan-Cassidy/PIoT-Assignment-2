import socketio

sioc = socketio.Client()

# Socket Events

@sioc.event
def connect() :
    print("Connection Successful")

@sioc.event
def connect_error() :
    print("Connection error")

@sioc.event
def disconnect() :
    print("Disconnected from server")
