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
    Response
)
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
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.oauth2.credentials
from flask_api import User, db

# We only need calendar.events scope since we are just managing events in user's calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CLIENT_SECRETS_FILE = "client_secret.json"

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


site = flask.Blueprint("site", __name__)

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
    """
    Routes user to the login page.
    Returns:
        HTML: Login page.
    """
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
    """
    Routes user to the dashboard page.
    Returns:
        HTML: Dashboard page.
    """
    if not User.query.filter_by(UserName=flask.session['username']).first().credentials:
        flask.flash("Google calendar permission not authorised. Redirecting...")
        return flask.redirect(flask.url_for('site.authorize'))
    return flask.render_template("dashboard.html", title="Dashboard")

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
    lats = []
    lngs = []
    makes = []
    seats = []
    types = []
    costs = []
    for x in data:
        y = json.loads(x["Location"])
        lats.append(y["location"]["lat"])
        lngs.append(y["location"]["lng"])
        makes.append(x["Make"])
        seats.append(x["Seats"])
        types.append(x["Type"])
        costs.append(x["CostPerHour"])

    return render_template(
        "booking.html",
        cars=data,
        form=form,
        lats=lats,
        lngs=lngs,
        makes=makes,
        seats=seats,
        types=types,
        costs=costs,
    )

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
    """
    Displays user's booking history.
    Returns:
        HTML: Booking by user page.
    """
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
    username = data['username']
    title = data['title']
    location = data['location']
    description = data['description']
    startTime = data['startTime']
    endTime = data['endTime']
    timeZone = 'Australia/Melbourne'

    """Add event to primary google calendar of current user

            Arguments:
            title {[str]} -- [title of the event]
            location {[str]} -- [location of event]
            desc {[str]} -- [description of event]
            startTime {[str]} -- [even start time in format date-time = full-date "T" full-time (eg. 2020-04-29T09:00:00-07:00)]
            endTime {[str]} -- [event end time. Similar formatting to start time]
            timeZone {[str]} -- [IANA timezone for event - defaults to Australia/Melbourne]
    """
    creds = User.query.filter_by(UserName=username).first().credentials
    if not creds:
            print("Error. credentials not found")
            return flask.jsonify({"message": "error", "text": "Google Calendar not authorised!"})

    credentials = google.oauth2.credentials.Credentials(**creds)
    service = build('calendar', 'v3',
                        credentials=credentials)

    event = {
            'summary': title,
            'location': location,
            'description': description,
            'start': {
                'timeZone': timeZone,
                'dateTime': startTime       
            },
            'end': {
                'timeZone': timeZone,
                'dateTime': endTime
            },
        }
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        id = event.get('id')
        print('Event created: {}'.format(event.get('htmlLink')))
        return flask.jsonify({"message": "Success", "text": "Event created", "eventId":id})
    except:
        return flask.jsonify({"message": "error", "text": "Error creating event!"})

@site.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = flask.url_for('site.oauth2callback', _external=True)
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    auth_response = flask.request.url
    if 'error' in auth_response:
        return flask.redirect(flask.url_for('site.dashboard'))

    flow.fetch_token(authorization_response=auth_response)
    creds = flow.credentials
    
    user = User.query.filter_by(UserName=flask.session['username']).first()
    user.credentials = credentials_to_dict(creds)
    db.session.commit()

    flask.flash("Gcal authenticated.", 'success')
    return flask.redirect(flask.url_for('site.dashboard'))

@site.route("/clear_creds")
def clear_creds():
    if 'username' in flask.session:
        user = User.query.filter_by(UserName=flask.session['username']).first()
        user.credentials = None
        db.session.commit()
        return jsonify({"success":"Credentials cleared for {user.UserName}"})
    else:
        return jsonify({"error":"Not signed in!"})

@site.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = flask.url_for('site.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        prompt='select_account',
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
