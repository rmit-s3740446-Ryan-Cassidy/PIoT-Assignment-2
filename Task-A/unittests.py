import unittest
import flask
import requests, json
from passlib.hash import sha256_crypt
from json import JSONEncoder
import datetime
from datetime import date, time 

class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()

class TestStringMethods(unittest.TestCase):
    def test_login_CorrectUsernameAndPassword(self):
        userLoginData = {"username":"s3734938", "password":"password"}
        response = requests.post("http://raspberry.localpi.com:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Success")
    
    def test_login_CorrectUsernameAndIncorrectPassword(self):
        userLoginData = {"username":"s3734938", "password":"passwordTrial"}
        response = requests.post("http://raspberry.localpi.com:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
    
    def test_login_InCorrectUsernameAndCorrectPassword(self):
        userLoginData = {"username":"s3734932", "password":"password"}
        response = requests.post("http://raspberry.localpi.com:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
    
    def test_login_InCorrectUsernameAndPassword(self):
        userLoginData = {"username":"s3734932", "password":"passwordp"}
        response = requests.post("http://raspberry.localpi.com:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Invalid username or password")
    
    def test_register_withExistingUsername(self):
        userRegistrationData = {"firstname":"Vineet", "lastname":"Bugtani", "username":"s3734938", "email":"s3734938@gmail.com", "password":sha256_crypt.hash("abc123")}
        response = requests.post("http://raspberry.localpi.com:5000/registerUser", json=userRegistrationData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "This username is already taken")
    
    def test_register_withExistingEmail(self):
        userRegistrationData = {"firstname":"Vineet", "lastname":"Bugtani", "username":"s3734938", "email":"admin@blog.com", "password":sha256_crypt.hash("abc123")}
        response = requests.post("http://raspberry.localpi.com:5000/registerUser", json=userRegistrationData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "This email is already registered with another account")
    
    def test_booking_withPickupDateBeforeReturnDate(self):
        userBookingData = {"pickUpDate": "2020-06-10", "pickUpTime": "02:03:00", "returnDate": "2020-06-09", "returnTime": "00:21:00", "carID": "6", "username": "s3734938"}
        userBookingJSONData = json.dumps(userBookingData, cls=DateTimeEncoder)
        response = requests.post("http://raspberry.localpi.com:5000/bookingDetails", json=userBookingJSONData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Pick up date has to be before return date")
    
    def test_booking_PickupDateInThePast(self):
        userBookingData = {"pickUpDate": "2020-04-03", "pickUpTime": "02:03:00", "returnDate": "2020-05-09", "returnTime": "00:21:00", "carID": "6", "username": "s3734938"}
        userBookingJSONData = json.dumps(userBookingData, cls=DateTimeEncoder)
        response = requests.post("http://raspberry.localpi.com:5000/bookingDetails", json=userBookingJSONData)
        data = json.loads(response.text)
        self.assertEqual(data["message"], "Cannot enter a date in the past")

if __name__ == "__main__":
    unittest.main()    