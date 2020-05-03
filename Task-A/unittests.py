import unittest
import flask
import requests, json

class TestStringMethods(unittest.TestCase):
    def test_login_CorrectUsernameAndPassword(self):
        userLoginData = {"username":"s3734938", "password":"password"}
        response = requests.post("http://127.0.0.1:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Success")
    
    def test_login_CorrectUsernameAndIncorrectPassword(self):
        userLoginData = {"username":"s3734938", "password":"passwordTrial"}
        response = requests.post("http://127.0.0.1:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
    
    def test_login_InCorrectUsernameAndCorrectPassword(self):
        userLoginData = {"username":"s3734932", "password":"password"}
        response = requests.post("http://127.0.0.1:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
    
    def test_login_InCorrectUsernameAndPassword(self):
        userLoginData = {"username":"s3734932", "password":"passwordp"}
        response = requests.post("http://127.0.0.1:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")

if __name__ == "__main__":
    unittest.main()      
