# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 
# https://developers.google.com/gmail/api/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#

# [START gmail_quickstart]
import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_full_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()

        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'Subject':
                print("Subject: ", header['value'])
            if header['name'] == 'From':
                print("From: ", header['value'])
            if header['name'] == 'To':
                print("To: ", header['value'])

        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    print("Body: ", body)
                elif part['mimeType'] == 'text/html':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    print("HTML Body: ", body)
        else:
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            print("Body: ", body)

    except HttpError as error:
        print(f'An error occurred: {error}')


def apply_label(service, user_id, msg_id, label_id):
    try:
        # Apply the label to the message
        message = service.users().messages().modify(
            userId=user_id,
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        
        print(f"Label applied: {label_id} to message ID: {msg_id}")
        print("Updated Labels: ", message['labelIds'])

    except HttpError as error:
        print(f'An error occurred: {error}')


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    breakpoint()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])
            if label["name"] == "foo":
                break
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    # Create a new label
    label_body = {
        'name': 'foo',
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }

    # CREATE A NEW LABEL 
    # try:
    #     label = service.users().labels().create(userId='me', body=label_body).execute()
    #     print(f"Label created: {label['name']} (ID: {label['id']})")
    # except Exception as error:
    #     print(f"An error occurred: {error}")
            
    # List all emails and open them one by one
    try:
        # Call the Gmail API to list messages
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            print('Messages:')
            for message in messages:
                # breakpoint()
                get_full_message(service, 'me', message['id'])
                # msg = service.users().messages().get(userId='me', id=message['id']).execute()
                # print(f"Message snippet: {msg['snippet']} (ID: {msg['id']})")
                # Label a message
                apply_label(service, 'me', message['id'], label['id'])
    except Exception as error:
        print(f"An error occurred: {error}")
    
    
if __name__ == "__main__":
  main()
# [END gmail_quickstart]