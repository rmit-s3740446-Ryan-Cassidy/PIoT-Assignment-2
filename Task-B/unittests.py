import unittest
import agent

class Agent_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        agent.load_config()
        agent.connect()

    #Test Google Geolocation
    def test_Geolocation_API(self):
        response = requests.post(geolocateURL)
        data = json.loads(response.text)
        assertIn('location' in data)
    
    #Test connection to Master server by retrieving SID
    #SID is the ID assigned to a socket connection by Master
    def test_Socket_Connection(self):
        sid = agent.sioc.sid
        assertTrue(sid)
    
    #Test Login - Username/Password incorrect
    def test_Login_Incorrect(self):
        username = "thisis"
        password = "incorrect"
        sioc.emit('usercredauth', [username, password])

    #Test Login - Username correct, Password incorrect
    def test_Login_Username_Correct(self):
        username = "ryan"
        password = "incorrect"

    #Test Login - Username correct, Password correct
    def test_Login_Correct(self):
        username = "ryan"
        password = "pass"

    #Test Facial Recognition Login - Correct Image
    def test_Login_Facial_Match(self):

    #Test Facial Recognition Login - Incorrect Image
    def testLogin_Facial_Mismatch(self):

if __name__ = "__main__":
    unittest.main()