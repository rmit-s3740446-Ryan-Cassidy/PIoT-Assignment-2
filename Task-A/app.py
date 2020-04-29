from flask import (
    Flask,
    render_template,
    url_for,
    flash,
    redirect,
    Blueprint,
    request,
    jsonify,
    session,
)
from forms import RegistrationForm, LoginForm, BookingForm, CarsFilterForm
from passlib.hash import sha256_crypt
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from json import JSONEncoder
import datetime


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()


site = Blueprint("site", __name__)
cars = [
    {
        "id": "1",
        "make": "Honda",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "2",
        "make": "Civic",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "3",
        "make": "Benz",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "4",
        "make": "Hyundai",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "5",
        "make": "Honda",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "6",
        "make": "Honda",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
    {
        "id": "7",
        "make": "Honda",
        "type": "Sedan",
        "color": "black",
        "seats": "6",
        "location": "3073",
        "costPerHour": "$20",
    },
]


@site.route("/")
@site.route("/home")
def home():
    return render_template("home.html")


@site.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        userRegistrationData = {
            "firstname": form.firstname.data,
            "lastname": form.lastname.data,
            "username": form.username.data,
            "email": form.email.data,
            "password": sha256_crypt.hash(form.password.data),
        }
        response = requests.post(
            "http://127.0.0.1:5000/registerUser", json=userRegistrationData
        )
        data = json.loads(response.text)
        if data["message"] == "Success":
            form.firstname.data = ""
            form.lastname.data = ""
            form.username.data = ""
            form.email.data = ""
            flash(f"Account created for {form.username.data}!", "success")
        else:
            flash(data["message"], "danger")
    return render_template("register.html", title="Register", form=form)


@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userLoginData = {"username": form.username.data, "password": form.password.data}
        response = requests.post("http://127.0.0.1:5000/loginUser", json=userLoginData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            session["username"] = form.username.data
            return redirect(url_for("site.dashboard"))
        else:
            flash(data["message"], "danger")
            form.username.data = ""
    return render_template("login.html", title="Login", form=form)


@site.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@site.route("/booking/", defaults={"name": "Person"}, methods=["GET", "POST"])
@site.route("/booking/<name>", methods=["GET", "POST"])
def booking(name):
    form = CarsFilterForm()
    response = requests.get(
        "http://127.0.0.1:5000/car/" + form.make.data + "/" + form.seats.data
    )
    data = json.loads(response.text)
    return render_template("booking.html", cars=data, form=form)


@site.route("/bookingDetails/<carId>", methods=["GET", "POST"])
def bookingDetails(carId):
    form = BookingForm()
    if form.validate_on_submit():
        userBookingData = {
            "pickUpDate": form.pickup_date.data,
            "pickUpTime": form.pickup_time.data,
            "returnDate": form.return_date.data,
            "returnTime": form.return_time.data,
            "carID": carId,
            "username": session["username"],
        }
        userBookingJSONData = json.dumps(userBookingData, cls=DateTimeEncoder)
        response = requests.post(
            "http://127.0.0.1:5000/bookingDetails", json=userBookingJSONData
        )
        data = json.loads(response.text)
        if data["message"] == "Success":
            flash(data["message"], "success")
        else:
            flash(data["message"], "danger")
    return render_template("bookingDetails.html", form=form)


@site.route("/bookingsByUser", methods=["GET", "POST"])
def bookingsByUser():
    response = requests.post(
        "http://127.0.0.1:5000/bookingsByUser/" + session["username"]
    )
    data = json.loads(response.text)
    return render_template("bookingsByUser.html", data=data)

