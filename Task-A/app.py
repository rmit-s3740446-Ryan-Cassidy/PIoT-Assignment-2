from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, BookingForm
from passlib.hash import sha256_crypt
import sys
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        hashedPassword = sha256_crypt.hash("password")
        if email == 'admin@blog.com' and sha256_crypt.verify(form.password.data, hashedPassword):
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    return render_template("booking.html", cars = cars)

@app.route("/bookingDetails/<carId>", methods=['GET', 'POST'])
def bookingDetails(carId):
    form = BookingForm()
    print(carId)
    return render_template("bookingDetails.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
