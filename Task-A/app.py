import flask
from forms import RegistrationForm, LoginForm, BookingForm, CarsFilterForm
from passlib.hash import sha256_crypt
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from json import JSONEncoder
import datetime
from datetime import date, time
from cal import GCal
from google_auth_oauthlib.flow import Flow


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()


site = flask.Blueprint("site", __name__)
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
    return flask.render_template("home.html")

@site.route("/logout")
def logout():
        flask.session.pop('username')
        return flask.redirect(flask.url_for("site.home"))


@site.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        userRegistrationData = {"firstname":form.firstname.data, "lastname":form.lastname.data, "username":form.username.data, "email":form.email.data, "password":sha256_crypt.hash(form.password.data)}
        response = requests.post(flask.request.host_url + "/registerUser", json=userRegistrationData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            form.firstname.data = ""
            form.lastname.data = ""
            form.username.data = ""
            form.email.data = ""
            flask.flash(f"Account created for {form.username.data}!", "success")
        else:
            flask.flash(data["message"], "danger")
    return flask.render_template("register.html", title="Register", form=form)


@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userLoginData = {"username":form.username.data, "password":form.password.data}
        response = requests.post(flask.request.host_url + "/loginUser", json=userLoginData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flask.session["username"] = form.username.data
            return flask.redirect(flask.url_for("site.dashboard"))
        else:
            flask.flash(data["message"], "danger")
            form.username.data = ""
    return flask.render_template("login.html", title="Login", form=form)


@site.route("/dashboard/")
def dashboard():
    if 'credentials' not in flask.session:
        flask.flash("Google calendar permission not authorised. Redirecting...")
        return flask.redirect(flask.url_for('site.authorize'))
    return flask.render_template("dashboard.html", title="Dashboard")

@site.route("/oauth2callback")
def oauth2callback():
    flow = GCal.flow
    flow.redirect_uri = flask.url_for('site.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials
    flask.session['credentials'] = credentials_to_dict(creds)
    flask.flash("GCal authorization successful.")
    return flask.redirect(flask.url_for('site.dashboard'))

@site.route("/authorize")
def authorize():
    return GCal().auth_gcal()

@site.route("/clear")
def clear_credentials():
    flask.session.clear()
    return flask.make_response('GCal credentials cleared.', 200)

@site.route("/booking/", defaults={"name": "Person"}, methods=["GET", "POST"])
@site.route("/booking/<name>", methods=["GET", "POST"])
def booking(name):
    form = CarsFilterForm()
    response = requests.get(
        flask.request.host_url + "/car/" + form.make.data + "/" + form.seats.data
    )
    data = json.loads(response.text)
    return flask.render_template("booking.html", cars=data, form=form)


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
            "username": flask.session["username"],
        }
        userBookingJSONData = json.dumps(userBookingData, cls=DateTimeEncoder)
        response = requests.post(flask.request.host_url + "/bookingDetails", json=userBookingJSONData)
        data = json.loads(response.text)
        if data["message"] == "Success":
            flask.flash(data["message"], "success")
        else:
            flask.flash(data["message"], "danger")
    return flask.render_template("bookingDetails.html", form=form)


@site.route("/bookingsByUser", methods=["GET", "POST"])
def bookingsByUser():
    response = requests.post(
        "http://127.0.0.1:5000/bookingsByUser/" + flask.session["username"]
    )
    data = json.loads(response.text)
    return flask.render_template("bookingsByUser.html", title ="Booking History", data=data, now=date.today().isoformat())


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}