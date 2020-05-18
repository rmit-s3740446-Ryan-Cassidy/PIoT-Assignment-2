"""
Contains the database schema to allow mapping to the database table.
"""
from datetime import datetime
from flask import Flask, Blueprint, request, jsonify, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
import sys
from passlib.hash import sha256_crypt
from datetime import datetime, date, time
from json import JSONDecoder
import datetime
from datetime import timedelta
from datetime import date, time 

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Car(db.Model):
    """
    The database schema for the Car table.
    """
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
    """
    The database schema for the User table.
    """
    __tablename__ = "User"
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    UserName = db.Column(db.Text)
    Email = db.Column(db.Text)
    Role = db.Column(db.Text)

    def __init__(self, FirstName, LastName, UserName, Email, Role, UserID=None):
        self.UserID = UserID
        self.FirstName = FirstName
        self.LastName = LastName
        self.UserName = UserName
        self.Email = Email
        self.Role = Role


class Login(db.Model):
    """
    The database schema for the Login table.
    """
    __tablename__ = "Login"
    LoginID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.Text)
    Password = db.Column(db.Text)

    def __init__(self, Password, UserName, LoginID=None):
        self.LoginID = LoginID
        self.UserName = UserName
        self.Password = Password

class Booking(db.Model):
    """
    The database schema for the Booking table.
    """
    __tablename__ = "Booking"
    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PickUpTime = db.Column(db.Time)
    ReturnDate = db.Column(db.Date)
    ReturnTime = db.Column(db.Time)
    CarID = db.Column(db.Integer)
    UserName = db.Column(db.Text)
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
    """
    Format Car schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")

carsSchema = CarSchema()
carsSchema = CarSchema(many=True)

class UserSchema(ma.Schema):
    """
    Format User schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("UserID", "FirstName", "LastName", "UserName", "Email", "Role")

usersSchema = UserSchema()
usersSchema = UserSchema(many=True)

class LoginSchema(ma.Schema):
    """
    Format Login schema output with marshmallow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("LoginID", "UserName", "Password")

loginSchema = LoginSchema()
loginSchema = LoginSchema(many=True)

class BookingSchema(ma.Schema):
    """
    Format Booking schema output with marshmallow.
    """
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
    """
    Format Booking Detail schema output with marshmallow.
    """
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

@api.route("/car", methods=["GET"])
def getCars():
    """
    Gets cars information from database.

    Returns:
        JSON: Car information (e.g "CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")
    """
    cars = Car.query.all()
    result = carsSchema.dump(cars)
    return jsonify(result)

@api.route("/updatecarlocation", methods=["POST"])
def updateCarLocation():
    """
    Updates car location in the database.

    Returns:
        JSON: Car information (e.g "CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")
    """
    data = request.get_json(force=True)
    car = Car.query.filter(Car.CarID == data["id"])
    car[0].Location = data["location"]
    db.session.commit()
    result = carsSchema.dump(car)
    return jsonify(result)

@api.route("/updatecarstatus", methods=["POST"])
def updateCarStatus():
    """
    Updates car status in the database.

    Returns:
        JSON: Car information (e.g "CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")
    """
    data = request.get_json(force=True)
    car = Car.query.filter(Car.CarID == data["id"])
    car[0].Status = data["status"]
    db.session.commit()
    result = carsSchema.dump(car)
    return jsonify(result)


@api.route("/car/<make>/<seats>/<price>", methods=["GET"])
def getFilteredCars(make, seats,price):
    """
    Retrieve car information from database and filter them based on make/seat/price.

    Args:
        make (str): Car make
        seats (int): No. of Seats in the car
        price (str): Rental price of car

    Returns:
        JSON: Car information (e.g "CarID", "Make", "Type", "Location", "Color", "Seats", "CostPerHour","Status")
    """
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
    """
    Retrieve users' information from database.

    Returns:
        JSON: User information (e.g "UserID", "FirstName", "LastName", "UserName", "Email", "Role")
    """
    users = User.query.all()
    result = usersSchema.dump(users)
    return jsonify(result)

@api.route("/users/<username>", methods=["POST"])
def user_exists(username):
    """
    Check whether input username exists in the database.

    Returns:
        JSON: "message": "True"/"False"
    """
    print(username)
    user = User.query.filter_by(UserName=username).first()
    if user:
        return jsonify({"message": "True"})
    else:
        return jsonify({"message": "False"})


@api.route("/logins", methods=["GET"])
def getLogins():
    """
    Get all login data from database.

    Returns:
        JSON: Login information (e.g "LoginID", "UserName", "Password")
    """
    logins = Login.query.all()
    result = loginSchema.dump(logins)
    return jsonify(result)


@api.route("/bookings/<carId>", methods=["GET"])
def getBookings(carId):
    """
    Get all bookings from database.

    Args:
        carId (str): Car unique identifier

    Returns:
        JSON: Booking information (e.g "BookingID","PickUpDate","PickUpTime","ReturnDate","ReturnTime","CarID","UserName")
    """
    bookings = Booking.query.filter_by(CarID=carId)
    result = bookingSchema.dump(bookings)
    return jsonify(result)


@api.route("/bookingsByUser/<userId>", methods=["GET", "POST"])
def getBookingsByUserId(userId):
    """
    Get all booking details from database.

    Returns:
        JSON: Booking details information (e.g "BookingID","PickUpDate","PickUpTime","ReturnDate","ReturnTime",
        "UserName","CarID","Make","Type","Location","Color","Seats","CostPerHour")
    """
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
    """
    Fetch bookings for a particular user from database where the return date and return time is greater than the current time and todays date.

    Args:
        userId (str): User's unique identifier.

    Returns:
        JSON: Booking details information (e.g "BookingID","PickUpDate","PickUpTime","ReturnDate","ReturnTime","UserName",
        "CarID","Make","Type","Location","Color","Seats","CostPerHour")
    """
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
    """
    Get all bookings from database.

    Returns:
        JSON: Booking information (e.g "BookingID","PickUpDate","PickUpTime","ReturnDate","ReturnTime","CarID","UserName")
    """
    bookings = Booking.query.all()
    result = bookingSchema.dump(bookings)
    return jsonify(result)

# Endpoint to create new user.
@api.route("/registerUser", methods=["GET", "POST"])
def addUser():
    """
    Add user into the database.

    Returns:
        JSON: "message": "This email is already registered with another account"/"This username is already taken"/"Success"
    """
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
    """
    Retrieve login information from database and verify login details based on username and password. 

    Returns:
        JSON: "message": "Invalid username or password"/"Success"
    """
    data = request.get_json(force=True)
    user = Login.query.filter_by(UserName=data["username"]).first()
    if user:
        if sha256_crypt.verify(data["password"], user.Password):
            return jsonify({"message": "Success"})
    return jsonify({"message": "Invalid username or password"})

@api.route("/cancelBooking/<bookingId>", methods = ["GET", "POST"])
def cancelBooking(bookingId):
    """
    Remove booking from database.
    Args:
        bookingId (str): Booking's unique identifier.

    Returns:
        Redirects client to "site.bookingsByUser"
    """
    cancel = Booking.query.filter_by(BookingID = bookingId).one()
    db.session.delete(cancel)
    db.session.commit()
    return redirect(url_for("site.bookingsByUser"))

@api.route("/bookingDetails", methods=["GET", "POST"])
def addBooking():
    """
    Add booking into database.

    Returns:
        JSON: "message": "Pick up and return dates cannot be same"/"Cannot enter a date in the past"/"Pick up date has to be before return date"/"Car not available in this slot"/"Success"
    """
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
    db.session.add(newBooking)
    db.session.commit()
    return jsonify({"message": "Success"})


