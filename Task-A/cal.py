from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import flask

class GCal:
    """Implementation for Google calendar api to add booking to user's calendar
    """
    def __init__(self):
        super().__init__()

    # If modifying these scopes, delete the file token.pickle. We only need calendar.events scope since we are just managing events in user's calendar
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    CLIENT_SECRETS_FILE = "client_secret.json"
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

    def auth_gcal(self):
        self.flow.redirect_uri = flask.url_for('site.oauth2callback', _external=True)
        
        authorization_url, state = self.flow.authorization_url(
                # Enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                # Enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true')
        return flask.redirect(authorization_url)

    def add_event(self, title, location, desc, startTime, endTime, timeZone='Melbourne/Australia'):
        """Add event to primary google calendar of current user

            Arguments:
            title {[str]} -- [title of the event]
            location {[str]} -- [location of event]
            desc {[str]} -- [description of event]
            startTime {[str]} -- [even start time in format date-time = full-date "T" full-time (eg. 2020-04-29T09:00:00-07:00)]
            endTime {[str]} -- [event end time. Similar formatting to start time]
            timeZone {[str]} -- [timezone for event - defaults to Melbourne/Australia]
        """

        service = build('calendar', 'v3', credentials=self.creds)

        event = {
            'summary': title,
            'location': location,
            'description': desc,
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
