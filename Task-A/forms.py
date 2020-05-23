"""
Contains all the forms required to obtain data from user.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField, TimeField


class RegistrationForm(FlaskForm):
    firstname = StringField(
        "First name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    lastname = StringField(
        "Last name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    username = StringField(
        "User name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class CarsFilterForm(FlaskForm):
    make = SelectField(
        u'Filter by Make:',
        choices = [('All makes', 'All makes'),('Honda', 'Honda'), ('Civic', 'Civic'), ('Alto', 'Alto'), ('Mercedes', 'Mercedes')], default='All makes'
        
    )
    seats = SelectField(
        u'Filter By Seats:',
        choices = [('All seats', 'All seats'),('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='All seats'
        
    )
    price = SelectField(
        u'Filter By Cost/Hr:',
        choices = [('All prices', 'All prices'),('10', '10'), ('20', '20')], default='All prices'
        
    )
    submit = SubmitField("Filter")



class BookingForm(FlaskForm):
    pickup_date = DateField('Enter pick up date', format='%Y-%m-%d')
    pickup_time = TimeField('Enter pick up time', format='%H:%M')
    return_date = DateField('Enter return date', format='%Y-%m-%d')
    return_time = TimeField('Enter return time', format='%H:%M')
    submit = SubmitField("Submit")

