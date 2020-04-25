from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
import sys

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Car(db.Model):
    __tablename__ = "Car"
    CarID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Make = db.Column(db.Text)
    Type = db.Column(db.Text)
    Location = db.Column(db.Text)
    Color = db.Column(db.Text)
    Seats = db.Column(db.Text)
    CostPerHour = db.Column(db.Text)

    def __init__(self, Make,Type,Location,Color, Seats,CostPerHour,CarID = None):
        self.CarID = CarID
        self.Make = Make
        self.Type = Type
        self.Location = Location
        self.Color = Color
        self.Seats = Seats
        self.CostPerHour = CostPerHour

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    UserName = db.Column(db.Text)
    Email = db.Column(db.Text)
    Role = db.Column(db.Text)

    def __init__(self, FirstName,LastName,UserName,Email,Role,UserID = None):
        self.UserID = UserID
        self.FirstName = FirstName
        self.LastName = LastName
        self.UserName = UserName
        self.Email = Email
        self.Role = Role

class CarSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
    
    class Meta:
        fields = ("CarID","Make","Type","Location","Color", "Seats","CostPerHour")

carsSchema = CarSchema()
carsSchema = CarSchema(many = True)

class UserSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
    
    class Meta:
        fields = ("UserID","FirstName","LastName","UserName","Email","Role")

usersSchema = UserSchema()
usersSchema = UserSchema(many = True)

@api.route("/car", methods = ["GET"])
def getCars():
    cars = Car.query.all()
    result = carsSchema.dump(cars)
    print(result)
    return jsonify(result)

@api.route("/users", methods = ["GET"])
def getUsers():
    users = User.query.all()
    result = usersSchema.dump(users)
    print(result)
    return jsonify(result)

# Endpoint to create new user.
@api.route("/registerUser", methods=["GET", "POST"])
def addUser():
    data = request.get_json(force=True)
    print(data)
    print(data['password'])
    userWithSameUsername = User.query.filter_by(UserName=data['username']).first()
    userWithSameEmail = User.query.filter_by(Email=data['email']).first()
    print(userWithSameUsername)
    if userWithSameEmail:
        return jsonify({"message":"This email is already registered with another account"})
    if userWithSameUsername:
        return jsonify({"message":"This username is already taken"})
   
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    email = request.json["email"]

    newUser = User(FirstName = firstname,LastName = lastname,UserName = username,Email = email,Role="Customer")

    db.session.add(newUser)
    db.session.commit()
    return jsonify({"message":"Success"})


