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
from datetime import date, time 

class DateTimeEncoder(JSONEncoder):
    """
    Encodes datetime into ISO format.
    Args:
        obj(str): datetime
    
    Return:
        Date and time in ISO format.
    """
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
    """
    Routes user to the home page.

    Returns:
        HTML: Home page.
    """
    return render_template("home.html")

@site.route("/logout")
def logout():
    """
    Logs user out and ends the session.

    Returns:
        HTML: Home page.
    """
    session.pop('username')
    return redirect(url_for("site.home"))

@site.route("/register", methods=["GET", "POST"])
def register():
    """
    Routes user to the registration page.

    Returns:
        HTML: Registration page.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        userRegistrationData = {"firstname":form.firstname.data, "lastname":form.lastname.data, "username":form.username.data, "email":form.email.data, "password":sha256_crypt.hash(form.password.data)}
        response = requests.post(request.host_url + "/registerUser", json=userRegistrationData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flash(f"Account created for {form.username.data}!!", "success")
            form.firstname.data = ""
            form.lastname.data = ""
            form.username.data = ""
            form.email.data = ""
        else:
            flash(data["message"], "danger")
    return render_template("register.html", title="Register", form=form)


@site.route("/login", methods=["GET", "POST"])
def login():
    """
    Routes user to the login page.

    Returns:
        HTML: Login page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        userLoginData = {"username":form.username.data, "password":form.password.data}
        response = requests.post(request.host_url + "/loginUser", json=userLoginData)
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
    """
    Routes user to the dashboard page.

    Returns:
        HTML: Dashboard page.
    """
    return render_template("dashboard.html", title="Dashboard")

@site.route("/booking", methods=["GET", "POST"])
def booking():
    """
    Routes user to the booking page.

    Returns:
        HTML: Booking page.
    """
    form = CarsFilterForm()
    response = requests.get(
        request.host_url + "/car/" + form.make.data + "/" + form.seats.data + "/" + form.price.data
    )
    data = json.loads(response.text)
    return render_template("booking.html", cars=data, form=form)


@site.route("/bookingDetails/<carId>", methods=["GET", "POST"])
def bookingDetails(carId):
    """
    Routes user to the registration page.
    Args:
        carId(str): Car unique identifier

    Returns:
        HTML: Bookind details page.
    """
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
        response = requests.post(request.host_url + "/bookingDetails", json=userBookingJSONData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flash(data["message"], "success")
        else:
            flash(data["message"], "danger")
    return render_template("bookingDetails.html", form=form)


@site.route("/bookingsByUser", methods=["GET", "POST"])
def bookingsByUser():
    """
    Displays user's booking history.

    Returns:
        HTML: Booking by user page.
    """
    response = requests.post(
        request.host_url + "/bookingsByUser/" + session["username"]
    )
    data = json.loads(response.text)
    return render_template("bookingsByUser.html", title ="Booking History", data=data, now=date.today().isoformat())

