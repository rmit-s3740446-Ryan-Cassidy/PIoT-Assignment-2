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

class CarSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
    
    class Meta:
        fields = ("CarID","Make","Type","Location","Color", "Seats","CostPerHour")

carsSchema = CarSchema()
carsSchema = CarSchema(many = True)

@api.route("/car", methods = ["GET"])
def getCars():
    cars = Car.query.all()
    result = carsSchema.dump(cars)
    print(result)
    return jsonify(result)


