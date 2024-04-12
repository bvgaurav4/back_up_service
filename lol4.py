from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive']


if os.path.exists('token.pickle'):
    os.remove('token.pickle')

def upload_file():
    """Shows basic usage of the Drive v3 API.
    Creates a Drive v3 API service and uploads a file.
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
                'god.json', SCOPES)
            creds = flow.run_console()  # Use console-based flow
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Call the Drive v3 API
    service = build('drive', 'v3', credentials=creds)

    # Upload a file
    file_metadata = {'name': 'My Report', 'mimeType': 'application/vnd.google-apps.spreadsheet'}
    media = MediaFileUpload('wallpaper/127076-porsche-918-spyder-wallpaper-top-free-porsche-918-spyder.jpg', mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))

import schedule # type: ignore
import time

schedule.every(1/2).minutes.do(upload_file)

while True:
    schedule.run_pending()
    time.sleep(1)