from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# If modifying these scopes, delete the file token.pickle.
# This scope allows read and write.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def get_cred():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(service, date):
    # date must be in datetime.date format.
    date_begin = datetime.datetime.combine(date, datetime.datetime.min.time())
    date_end = datetime.datetime.combine(date, datetime.datetime.max.time())
    
    date_begin = date_begin.astimezone(pytz.UTC)
    date_end = date_end.astimezone(pytz.UTC)
    # Call the Calendar API
    events_result = service.events().list(calendarId='primary',
                                        timeMin=date_begin.isoformat(),
                                        timeMax=date_end.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def add_event(service, date, event_name):
    date = date.strftime("%Y-%m-%d")
    event = {
    'summary': event_name,
    'start': {
        'date': date
    },
    'end': {
        'date': date
    }
    }
    # calendarId='primary' refers to the primary calendar of the logged in user
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return

if __name__ == '__main__':
    today  = datetime.date.today()
    event_name = 'Have fun'

    service = get_cred()
    add_event(service, today, event_name)
    events= get_events(service, today)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
