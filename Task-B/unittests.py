import unittest
import sys, json, base64, requests
from pil import Image
import time
import socketio

class Agent_Tests(unittest.TestCase):
    client = socketio.Client() #Test socket client
    ip = None
    geolocateURL = None

    #Config and Testing methods
    def load_config(self) :
        try:
            with open("config.json") as f:
                data = json.load(f)
                self.ip = "http://" + data["host"] + ":" + data["port"]
                self.geolocateURL = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + data['apikey']
        except Exception as e:
            print(str(e))
            sys.exit("Error when reading from Json.")
    
    #Convert image to base64 string
    def image_to_str(self, imagepath) :
        with open(imagepath, "rb") as image:
            b64str = base64.b64encode(image.read())
            return b64str

    # Connect to testing namespace
    def connect(self) : 
        self.client.connect(self.ip, namespaces=['/test'])

    # Before All
    @classmethod
    def setUpClass(self):
        self.load_config(self)
        self.connect(self)
    
    # After All
    @classmethod
    def tearDownClass(self):
        self.client.disconnect()
        exit
    
    #Tests utilize thread-unsafe call method instead of emit as it is better suited for unit testing purposes
    #Call is functionally the same as emit. Resumes method that called it when returning response from Master
    
    #Test connection to Master server by retrieving SID
    #SID is the ID assigned to a socket connection by Master
    def test_Socket_Connection(self):
        sid = self.client.sid
        self.assertTrue(sid)

    #Test Master Login responses
    #Tests use credential login test event

    #Test Login - Username/Password incorrect
    def test_Login_Incorrect(self):
        username = "thisis"
        password = "incorrect"
        auth = self.client.call('usercredauth', [username, password], namespace = '/test')
        self.assertFalse(username == auth) #If login was successful, auth equals username, else 'Fail'

    #Test Login - Username correct, Password incorrect
    def test_Login_Username_Correct(self):
        username = "ryan"
        password = "incorrect"
        auth = self.client.call('usercredauth', [username, password], namespace = '/test')
        self.assertFalse(username == auth) #If login was successful, auth equals username, else 'Fail'

    #Test Login - Username correct, Password correct
    def test_Login_Correct(self):
        username = "ryan"
        password = "pass"
        auth = self.client.call('usercredauth', [username, password], namespace = '/test')
        self.assertTrue(username == auth) #If login was successful, auth equals username, else 'Fail'

    #OpenCV Testing
    #Tests use facial recognition test event

    #Test Facial Recognition Login - Incorrect Image
    def testLogin_Facial_Mismatch(self):
        image = self.image_to_str("wrongimage.jpg")
        auth = self.client.call('facerecauth', image, namespace = '/test')
        self.assertTrue(auth == 'Fail') #If image is not matched with encoding, auth equals 'Fail'
    
    #Test Facial Recognition Login - Correct Image
    def test_Login_Facial_Match(self):
        image = self.image_to_str("image.jpg")
        auth = self.client.call('facerecauth', image, namespace = '/test')
        self.assertTrue(auth == 'Success') #If image is matched with encoding, auth equals 'Success'

    #Agent function testing

    #Test Google Geolocation
    def test_Geolocation_API(self):
        response = requests.post(self.geolocateURL)
        data = json.loads(response.text)
        self.assertIn('location', data) #If API key is set and request is returned. Data will contain location
        response = self.client.call('carupdatelocation', data, namespace = '/test')
        self.assertTrue(response == 'Success') #If location update sent correctly, response requals 'Success'

if __name__ == "__main__":
    unittest.main()