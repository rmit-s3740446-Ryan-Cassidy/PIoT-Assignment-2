import socket
import json

def loadconfig()
    
# Socket to Master
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to Master")
    s.bind()
# Prompt user for login type
# Send authentication attempt to Master
# If true, sign in, else ask user again