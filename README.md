# PIoT-Assignment-2

## Team Members

Ryan Cassidy (s3740446) - Worked on Task-B and C (agent.py, socketing between Pi's, facial recognition, Trello Board, Unit Testing)

Vineet Bugtani (s3734938) - Worked on Task-A (API, Site, Google Cloud Database, Unit Testing, Trello Board, Google Maps)

Akshay Sunil Salunke (s3730440) - Worked on Task-A and B (API, Site, Google Calendar, Trello Board, Sphinx Documentation)

Pui Ling Chan (s3561165) - Worked on Task-A (API, Site, Google Cloud Database, Sphinx Documentation, Trello Board)

## Feature Description

Group assignment 2 for RMIT Programming Internet of Things 2020
Features a flask website for renting cars and a python agent script for socketing to Master Pi and unlocking cars.

A database schema for the cloud database can be seen in the root directory of this repo.

In order for site to operate correctly the host address must be raspberry.localpi.com:5000 in order to utilize google calendar's redirect-uri. This may require some configuration in the host file in order to work in a local environment (add the ip you are hosting the site on or the loopback address followed by raspberry.localpi.com)

Site utilizes google maps, google calendar and a google cloud database. For configs and keys to these please ask above team members.

Flask-socketio is used to provide socketing through gevent-websocket to the agent, agent utilizes python-socketio to socket with site.

Agent uses google geolocation API to lookup location through IP address, config.json with api key required in order to use.

Both applications can be run on different Pi's and communicate.

Trello Board: https://trello.com/b/j2XWnnbK/programming-iot-assignment-2

**Run below commands in a terminal in MacOS**
## Setup venv
`python3 -m venv <virtual env path>`

## Activate venv
`source <virtual env path>/bin/activate` *alternatively* `. <virtual env path>/bin/activate`

## Install requirements
`pip install -r requirements.txt`

### To run and work on Task-A :
`cd Task-A` & `python3 flask_main.py`

### To run and work on Task-B :
`cd Task-B` & `python3 agent.py`

## To generate docs:
`cd docs` and then `make clean html`

## To view docs:
`Navigate to index.html in docs/build/html`
