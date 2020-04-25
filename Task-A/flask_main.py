from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api import api, db
from app import site
import MySQLdb
from database_utils import DatabaseUtils
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
basedir = os.path.abspath(os.path.dirname(__file__))

HOST = "35.244.74.229"
USER = "root"
PASSWORD = "abc123"
DATABASE = "CarBookingApp"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)

socketio.init_app(app)

if __name__ == "__main__":
    with DatabaseUtils() as db:
        db.createTables()
    socketio.run(app, host = "0.0.0.0", debug=True)
    #app.run(host = "0.0.0.0", debug=True)