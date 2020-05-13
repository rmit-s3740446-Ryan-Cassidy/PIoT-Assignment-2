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
    Respose
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
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# We only need calendar.events scope since we are just managing events in user's calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CLIENT_SECRETS_FILE = "client_secret.json"
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

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
            flash(f"Account created for {form.username.data}!!", "success")
            form.firstname.data = ""
            form.lastname.data = ""
            form.username.data = ""
            form.email.data = ""
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

@site.route("/booking", methods=["GET", "POST"])
def booking():
    form = CarsFilterForm()
    response = requests.get(
        request.host_url + "/car/" + form.make.data + "/" + form.seats.data + "/" + form.price.data
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
        request.host_url + "/bookingsByUser/" + session["username"]
    )
    data = json.loads(response.text)
    return flask.render_template("bookingsByUser.html", title="Booking History", data=data, now=date.today().isoformat())


@site.route("/addEvent", methods=["GET", "POST"])
def addEvent():
    d = flask.request.get_json(force=True)
    data = json.loads(d, cls=json.JSONDecoder)

    # Event attributes to be loaded from json
    title = data['title']
    location = data['location']
    description = data['description']
    startTime = data['startTime']
    endTime = data['endTime']
    timeZone = 'Melbourne/Australia'

    """Add event to primary google calendar of current user

            Arguments:
            title {[str]} -- [title of the event]
            location {[str]} -- [location of event]
            desc {[str]} -- [description of event]
            startTime {[str]} -- [even start time in format date-time = full-date "T" full-time (eg. 2020-04-29T09:00:00-07:00)]
            endTime {[str]} -- [event end time. Similar formatting to start time]
            timeZone {[str]} -- [timezone for event - defaults to Melbourne/Australia]
    """
    if 'credentials' not in flask.session:
            print("Error. credentials not found")
            return flask.jsonify({"message": "error", "text": "Google Calendar not authorised!"})

    service = build('calendar', 'v3',
                        credentials=flask.session['credentials'])

    event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {
                'dateTime': startTime,
                'timeZone': timeZone,
            },
            'end': {
                'dateTime': endTime,
                'timeZone': timeZone,
            },
        }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))
    return flask.jsonify({"message": "Success", "text": "Event created"})

@site.route("/oauth2callback")
def oauth2callback():
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    if 'error' in authorization_response:
        return flask.redirect(flask.url_for('site.dashboard'))

    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials
    flask.session['credentials'] = credentials_to_dict(creds)
    Flask.save_session(session=flask.session)
    flask.flash("Gcal authenticated.", 'success')
    return flask.redirect(flask.url_for('site.dashboard'))

@site.route("/authorize")
def authorize():
    flow.redirect_uri = flask.url_for('site.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    return flask.redirect(authorization_url)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
