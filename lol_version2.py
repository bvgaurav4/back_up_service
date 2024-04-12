from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive']

# if os.path.exists('token.pickle'):
#     print("asdasd")
#     os.remove('token.pickle')



def upload_file():
    """Shows basic usage of the Drive v3 API.
    Creates a Drive v3 API service and uploads a file.
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = Credentials.from_service_account_file('c3.json', scopes=SCOPES)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': 'My Report', 'mimeType': 'application/vnd.google-apps.spreadsheet'}
    media = MediaFileUpload('wallpaper/127076-porsche-918-spyder-wallpaper-top-free-porsche-918-spyder.jpg', mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(file_metadata)
    print('File ID: %s' % file.get('id'))


import schedule # type: ignore
import time

# upload_file()
schedule.every(1).minutes.do(upload_file)

while True:
    schedule.run_pending()
    time.sleep(1)