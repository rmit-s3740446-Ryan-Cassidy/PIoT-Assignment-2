from datetime import datetime
from flask import Flask, Blueprint, request, jsonify, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
import sys, flask
from passlib.hash import sha256_crypt
from datetime import datetime, date, time
from json import JSONDecoder
import datetime
from datetime import timedelta
from datetime import date, time 
import google.oauth2.credentials
from googleapiclient.discovery import build

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Car(db.Model):
    __tablename__ = "Car"
    CarID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Make = db.Column(db.Text)
    Type = db.Column(db.Text)
    Location = db.Column(db.Text)
    Color = db.Column(db.Text)
    Seats = db.Column(db.Text)
    CostPerHour = db.Column(db.Text)
    Status = db.Column(db.Text)

    def __init__(self, Make, Type, Location, Color, Seats,Status, CostPerHour, CarID=None):
        self.CarID = CarID
        self.Make = Make
        self.Type = Type
        self.Location = Location
        self.Color = Color
        self.Seats = Seats
        self.CostPerHour = CostPerHour,
        self.Status = Status


class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    UserName = db.Column(db.Text)
    Email = db.Column(db.Text)
    Role = db.Column(db.Text)
    credentials = db.Column(db.JSON)

    def __init__(self, FirstName, LastName, UserName, Email, Role, UserID=None):
        self.UserID = UserID
        self.FirstName = FirstName
        self.LastName = LastName
        self.UserName = UserName
        self.Email = Email
        self.Role = Role


class Login(db.Model):
    __tablename__ = "Login"
    LoginID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.Text)
    Password = db.Column(db.Text)

    def __init__(self, Password, UserName, LoginID=None):
        self.LoginID = LoginID
        self.UserName = UserName
        self.Password = Password


class Booking(db.Model):
    __tablename__ = "Booking"
    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PickUpDate = db.Column(db.Date)
    PickUpTime = db.Column(db.Time)
    ReturnDate = db.Column(db.Date)
    ReturnTime = db.Column(db.Time)
    CarID = db.Column(db.Integer)
    UserName = db.Column(db.Text)
    eventId = db.Column(db.Text)
    # TotalCost = db.Column(db.Text)

    def __init__(
        self,
        PickUpDate,
        PickUpTime,
        ReturnDate,
        ReturnTime,
        CarID,
        UserName,
        BookingID=None,
    ):
        self.BookingID = BookingID
        self.PickUpDate = PickUpDate
        self.PickUpTime = PickUpTime
        self.ReturnDate = ReturnDate
        self.ReturnTime = ReturnTime
        self.CarID = CarID
        self.UserName = UserName
        # self.TotalCost = TotalCost


class CarSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")


carsSchema = CarSchema()
carsSchema = CarSchema(many=True)


class UserSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("UserID", "FirstName", "LastName", "UserName", "Email", "Role")


usersSchema = UserSchema()
usersSchema = UserSchema(many=True)


class LoginSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("LoginID", "UserName", "Password")


loginSchema = LoginSchema()
loginSchema = LoginSchema(many=True)


class BookingSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = (
            "BookingID",
            "PickUpDate",
            "PickUpTime",
            "ReturnDate",
            "ReturnTime",
            "CarID",
            "UserName",
        )


class BookingDetailsSchema(ma.Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = (
            "BookingID",
            "PickUpDate",
            "PickUpTime",
            "ReturnDate",
            "ReturnTime",
            "UserName",
            "CarID",
            "Make",
            "Type",
            "Location",
            "Color",
            "Seats",
            "CostPerHour",
        )


bookingSchema = BookingSchema()
bookingSchema = BookingSchema(many=True)

bookingDetailsSchema = BookingDetailsSchema()
bookingDetailsSchema = BookingDetailsSchema(many=True)



@api.route("/car", defaults={'id':'all'}, methods=["GET"])
@api.route("/car/<id>")
def getCars(id):
    cars = Car.query.all()
    if 'all' in id:
        result = carsSchema.dump(cars)
        return jsonify(result)
    else:
        for car in cars:
            if car.CarID == int(id):
                result = CarSchema().dump(car)
                return (result)

@api.route("/updatecarlocation", methods=["POST"])
def updateCarLocation():
    data = request.get_json(force=True)
    car = Car.query.filter(Car.CarID == data["id"])
    car[0].Location = data["location"]
    db.session.commit()
    result = carsSchema.dump(car)
    return jsonify(result)

@api.route("/updatecarstatus", methods=["POST"])
def updateCarStatus():
    data = request.get_json(force=True)
    car = Car.query.filter(Car.CarID == data["id"])
    car[0].Status = data["status"]
    db.session.commit()
    result = carsSchema.dump(car)
    return jsonify(result)


@api.route("/car/<make>/<seats>/<price>", methods=["GET"])
def getFilteredCars(make, seats,price):
    cars = Car.query.all()
    filteredByMake = []
    filteredBySeats = []
    filteredByCost = []
    if make != "All makes":
        for car in cars:
            if car.Make == make:
                filteredByMake.append(car)
    else:
        filteredByMake = cars
    if seats != "All seats":
        for car in filteredByMake:
            if car.Seats == seats:
                filteredBySeats.append(car)
    else:
        filteredBySeats = filteredByMake
    if price != "All prices":
        for car in filteredBySeats:
            if car.CostPerHour == price:
                filteredByCost.append(car)
    else:
        filteredByCost = filteredBySeats
    result = carsSchema.dump(filteredByCost)
    return jsonify(result)


@api.route("/users", methods=["GET"])
def getUsers():
    users = User.query.all()
    result = usersSchema.dump(users)
    return jsonify(result)

@api.route("/users/<username>", methods=["POST"])
def user_exists(username):
    print(username)
    user = User.query.filter_by(UserName=username).first()
    if user:
        return jsonify({"message": "True"})
    else:
        return jsonify({"message": "False"})


@api.route("/logins", methods=["GET"])
def getLogins():
    logins = Login.query.all()
    result = loginSchema.dump(logins)
    return jsonify(result)


@api.route("/bookings/<carId>", methods=["GET"])
def getBookings(carId):
    bookings = Booking.query.filter_by(CarID=carId)
    result = bookingSchema.dump(bookings)
    return jsonify(result)


@api.route("/bookingsByUser/<userId>", methods=["GET", "POST"])
def getBookingsByUserId(userId):
    bookings = (
        Booking.query.join(Car, Booking.CarID == Car.CarID)
        .add_columns(
            Booking.BookingID,
            Booking.PickUpDate,
            Booking.PickUpTime,
            Booking.ReturnDate,
            Booking.ReturnTime,
            Booking.CarID,
            Booking.UserName,
            Car.CarID,
            Car.Make,
            Car.Type,
            Car.Location,
            Car.Color,
            Car.Seats,
            Car.CostPerHour,
        )
        .filter(Booking.UserName == userId)
    )
    result = bookingDetailsSchema.dump(bookings)
    return jsonify(result)

# This api will fetch only those bookings for a particular user where the return date and return time is greater than the
# current time and todays date
# For testing this add a booking one in the morning and one at night.You would only receive the booking which at night.
@api.route("/bookingsByUserAndDate/<userId>", methods=["GET", "POST"])
def getBookingsByUserIdAndDate(userId):
    today = date.today().isoformat()
    currentTime = datetime.datetime.now().time()
    print(datetime.datetime.now().time())
    bookings = (
        Booking.query.join(Car, Booking.CarID == Car.CarID)
        .add_columns(
            Booking.BookingID,
            Booking.PickUpDate,
            Booking.PickUpTime,
            Booking.ReturnDate,
            Booking.ReturnTime,
            Booking.CarID,
            Booking.UserName,
            Car.CarID,
            Car.Make,
            Car.Type,
            Car.Location,
            Car.Color,
            Car.Seats,
            Car.CostPerHour,
        )
        .filter(Booking.UserName == userId, Booking.ReturnDate >= today, Booking.ReturnTime >= currentTime )
    )
    result = bookingDetailsSchema.dump(bookings)
    return jsonify(result)



@api.route("/bookings/", methods=["GET"])
def getAllBookings():
    bookings = Booking.query.all()
    result = bookingSchema.dump(bookings)
    return jsonify(result)


# Endpoint to create new user.
@api.route("/registerUser", methods=["GET", "POST"])
def addUser():
    data = request.get_json(force=True)
    userWithSameUsername = User.query.filter_by(UserName=data["username"]).first()
    userWithSameEmail = User.query.filter_by(Email=data["email"]).first()
    if userWithSameEmail:
        return jsonify(
            {"message": "This email is already registered with another account"}
        )
    if userWithSameUsername:
        return jsonify({"message": "This username is already taken"})

    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    newUser = User(
        FirstName=firstname,
        LastName=lastname,
        UserName=username,
        Email=email,
        Role="Customer",
    )
    newLoginDetails = Login(UserName=username, Password=password)

    db.session.add(newUser)
    db.session.add(newLoginDetails)
    db.session.commit()
    return jsonify({"message": "Success"})


@api.route("/loginUser", methods=["GET", "POST"])
def checkLogin():
    data = request.get_json(force=True)

    user = Login.query.filter_by(UserName=data["username"]).first()
    if user:
        if sha256_crypt.verify(data["password"], user.Password):
            return jsonify({"message": "Success"})
    return jsonify({"message": "Invalid username or password"})

@api.route("/cancelBooking/<bookingId>", methods = ["GET", "POST"])
def cancelBooking(bookingId):
    cancel = Booking.query.filter_by(BookingID = bookingId).one()
    # Delete calendar event associated with this booking.
    eventId = cancel.eventId
    user_creds = User.query.filter_by(UserName=cancel.UserName).first().credentials

    if not user_creds:
        flask.flash("Google calendar not authorised by user!", "danger")
        return redirect(url_for("site.bookingsByUser"))

    credentials = google.oauth2.credentials.Credentials(**user_creds)
    service = build('calendar', 'v3', credentials=credentials)
    try:
        service.events().delete(calendarId='primary', eventId=eventId).execute()
        db.session.delete(cancel)
        db.session.commit()
    except:
        flask.flash('Unable to delete booking')

    return redirect(url_for("site.bookingsByUser"))

@api.route("/bookingDetails", methods=["GET", "POST"])
def addBooking():
    today = date.today()
    data = request.get_json(force=True)
    dataOne = json.loads(data, cls=json.JSONDecoder)
    pickUpDate = date.fromisoformat(dataOne["pickUpDate"])
    whileLoopPickUpDate = pickUpDate
    pickUpTime = dataOne["pickUpTime"]
    returnDate = date.fromisoformat(dataOne["returnDate"])
    returnTime = dataOne["returnTime"]
    carID = dataOne["carID"]
    username = dataOne["username"]
    if pickUpDate == returnDate:
        return jsonify({"message": "Pick up and return dates cannot be same"})
    if pickUpDate < today:
        print('came here')
        return jsonify({"message": "Cannot enter a date in the past"})
    if pickUpDate >= returnDate:
        return jsonify({"message":"Pick up date has to be before return date"})
    response = requests.get(request.host_url + "/bookings/" +carID)
    data = json.loads(response.text)
    for x in data:
        whileLoopPickUpDate = pickUpDate
        xpickUpDate = x["PickUpDate"]
        xreturnDate = x["ReturnDate"]
        format_str = "%Y-%m-%d"
        pickUpDateTime = datetime.datetime.strptime(xpickUpDate, format_str)
        returnDateTime = datetime.datetime.strptime(xreturnDate, format_str)
        while whileLoopPickUpDate <= returnDate:
            if pickUpDateTime.date() <= whileLoopPickUpDate <= returnDateTime.date():
                return jsonify({"message": "Car not available in this slot"})
            whileLoopPickUpDate = whileLoopPickUpDate + timedelta(days=1)
    newBooking = Booking(
        PickUpDate=pickUpDate,
        PickUpTime=pickUpTime,
        ReturnDate=returnDate,
        ReturnTime=returnTime,
        CarID=carID,
        UserName=username,
    )

    #Create calendar event
    carInfo = getCars(carID)
    location = carInfo['Location']
    carDesc = carInfo['Make'] + " (" + carInfo['Seats'] + " seater " + carInfo['Color'] + " " + carInfo['Type'] + ")"
    startTime = dataOne['pickUpDate'] + "T" + pickUpTime
    endTime = dataOne['returnDate'] + "T" + returnTime
    data = {
        'username': username,
        "title":'Car Booking', 
        "location":location, 
        "description":carDesc, 
        "startTime":startTime, 
        "endTime":endTime
        }
    data = json.dumps(data)

    event = requests.get(request.host_url + "/addEvent", json=data)
    event_response = json.loads(event.text)
    if 'error' in event_response['message']:
        return jsonify({"message":event_response['text']})
    else:
        #Commit booking to db
        eventId = event_response['eventId']
        newBooking.eventId = eventId
        db.session.add(newBooking)
        db.session.commit()
        return jsonify({"message": "Success"})
