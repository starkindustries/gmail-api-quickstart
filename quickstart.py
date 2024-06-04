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


def get_api_service_obj():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
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
    service = build("gmail", "v1", credentials=creds)
    return service


def list_labels(service):
    try:
        # Call the Gmail API
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return None
        return labels
    except HttpError as error:
        # TODO: Handle errors from gmail API.
        print(f"An error occurred: {error}")


def create_label(service, label_name):
    label_body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    
    try:
        label = service.users().labels().create(userId='me', body=label_body).execute()
        print(f"Label created: {label['name']} (ID: {label['id']})")
        return label
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


def delete_label(service, label_id):
    try:
        service.users().labels().delete(userId='me', id=label_id).execute()
        print(f'Label with ID {label_id} deleted successfully.')
        return True
    except Exception as e:
        print(f'An error occurred: {e}')
        return False


def list_messages(service):
    try:
        # Call the Gmail API to list messages
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        return messages
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


def get_full_message(service, msg_id):
    user_id = "me"
    message_data = {
        "headers": {},
        "body": "",
        "html_body": ""
    }

    try:
        # Fetch the full message using the Gmail API
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()

        # Extract headers from the message payload
        headers = message['payload']['headers']
        for header in headers:
            message_data["headers"][header['name']] = header['value']

        # Check if the message payload contains parts
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    # Decode and store the plain text body of the email
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    message_data["body"] += body
                elif part['mimeType'] == 'text/html':
                    # Decode and store the HTML body of the email
                    html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    message_data["html_body"] += html_body
        else:
            # If no parts are found, decode and store the body of the email directly
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            message_data["body"] = body

    except HttpError as error:
        # Store the error in the dictionary if one occurs during the API call
        message_data["error"] = str(error)

    return message_data


def apply_label(service, msg_id, label_id):
    # Hardcoding user_id to 'me' - currently do not have a use-case for another user_id
    user_id = "me"
    try:
        # Apply the label to the message
        message = service.users().messages().modify(
            userId=user_id,
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        
        print(f"Label applied: {label_id} to message ID: {msg_id}")
        print("Updated Labels: ", message['labelIds'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def main():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    service = get_api_service_obj()

    labels = list_labels(service)
    print("LABELS:")
    print(labels)

    return

    # # Create a new label
    # label_body = {
    #     'name': 'foo',
    #     'labelListVisibility': 'labelShow',
    #     'messageListVisibility': 'show'
    # }

    # # CREATE A NEW LABEL 
    # try:
    #     label = service.users().labels().create(userId='me', body=label_body).execute()
    #     print(f"Label created: {label['name']} (ID: {label['id']})")
    # except Exception as error:
    #     print(f"An error occurred: {error}")
            
    # # List all emails and open them one by one
    # try:
    #     # Call the Gmail API to list messages
    #     results = service.users().messages().list(userId='me', maxResults=10).execute()
    #     messages = results.get('messages', [])

    #     if not messages:
    #         print('No messages found.')
    #     else:
    #         print('Messages:')
    #         for message in messages:
    #             # breakpoint()
    #             get_full_message(service, 'me', message['id'])
    #             # msg = service.users().messages().get(userId='me', id=message['id']).execute()
    #             # print(f"Message snippet: {msg['snippet']} (ID: {msg['id']})")
    #             #
    #             # Label a message
    #             #
    #             apply_label(service, 'me', message['id'], label['id'])
    # except Exception as error:
    #     print(f"An error occurred: {error}")
    
    
if __name__ == "__main__":
    main()

# [END gmail_quickstart]
