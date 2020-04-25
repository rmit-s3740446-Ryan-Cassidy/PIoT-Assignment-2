from flask import Flask, render_template, url_for, flash, redirect, Blueprint, request, jsonify
from forms import RegistrationForm, LoginForm, BookingForm
from passlib.hash import sha256_crypt
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

site = Blueprint("site", __name__)
cars = [
    {
        'id': '1',
        'make': 'Honda',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '2',
        'make': 'Civic',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '3',
        'make': 'Benz',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '4',
        'make': 'Hyundai',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '5',
        'make': 'Honda',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '6',
        'make': 'Honda',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
    },
    {
        'id': '7',
        'make': 'Honda',
        'type': 'Sedan',
        'color': 'black',
        'seats': '6',
        'location': '3073',
        'costPerHour': '$20'
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
        print(form.username.data)
        print(form.lastname.data)
        print(form.email.data)
        print(form.password.data)
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("register"))
    return render_template("register.html", title="Register", form=form)


@site.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        hashedPassword = sha256_crypt.hash("password")
        if email == 'admin@blog.com' and sha256_crypt.verify(form.password.data, hashedPassword):
            return redirect(url_for('site.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@site.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")

@site.route("/booking", methods=['GET', 'POST'])
def booking():
    response = requests.get("http://127.0.0.1:5000/car")
    data = json.loads(response.text)
    print(data)
    return render_template("booking.html", cars = data)

@site.route("/bookingDetails/<carId>", methods=['GET', 'POST'])
def bookingDetails(carId):
    form = BookingForm()
    print(carId)
    return render_template("bookingDetails.html", form=form)







