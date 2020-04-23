import socket
import json
import sys

host = None
port = None

def loadconfig(self) :
    try:
        with open("config.json") as f:
            data = json.load(f)
            self.host = data["HOST"]
            self.port = data["PORT"]
    except Exception as e:
        print(str(e))
        sys.exit("Error when reading from Json.")

# Socket to Master
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to Master")
    s.bind(host, port)
    s.listen(5)
    conn, addr = s.accept()
# Prompt user for login type
# Send authentication attempt to Master
# If true, sign in, else ask user again