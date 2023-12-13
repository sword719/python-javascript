from pyminuteinbox import TempMailInbox, TempMail
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import os
import pickle
from dotenv import load_dotenv
import firebase_admin
import sys
from firebase_admin import credentials
from firebase_admin import db

# put the path to your .env file here
dotenv_path = '.env'

# load the .env file
load_dotenv(dotenv_path)

print(os.getenv('MAIL_SENDER'))

service_account = {
    "type": "service_account",
    "project_id": "upwork-7aafa",
    "private_key_id": "f577fffdd19382c7c903179858be107403e3c9e5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDIXijGAHIvrscK\nJw3FVMGDvXMvTiNUeOpboCZxCp/XnYHIK95fA3IglYgLsHHvh2hkS3tRlezOsFns\n9/ZNDON9fbfT33AeePhji0RtY8eK8zX1Z4Gu5GZ5wzBQ29/wj8tVkrtvwGdBNDpz\njtKpmcAsgy0ycqvxxgW6vVcVe29io+4FOHBZJzbHHqPq8tHKbz3NaXXs7uyqtdCS\nygL1vpIycUgtEsxbyYaXzrx0ZR3jaYBf9LwvXWeFxMVgUySEXQE2dJUYaYt5XSpO\nQcgX8C8qpE/l9gpnl9POgK4xtkv3Fq5gxfkL1Y5KpCBdbfQoiCiGGNGfqS8gpVf+\nTLdYSq7bAgMBAAECggEAKYg++l/gS1r2nfefZp5daGHOLOmM8DcKGQj2vuq9XDOl\nUakqNFaiAvgL1aRy0XwnWta8jpo9llA+q5xwXONFil8TSiMf+ekIT5XwDp6mn3ov\nXplga7CjPy0C6FfTMOmVc7zxBkaDAKSDUy2xI/+fMnrUVQco9foeeOlDUkweN/s1\niX91G85L0shjkmtANR81Va5Sz6h53OEbRwhugJFWP2iIdruxOTz4WaRcxFXX30Bo\nU7m8MNtyJYJCBGezCN9ub7NTMkF3wZfDbDmX4brCTHq/SolBwhqyCwaGu+YStPRG\nDxMWnk1MQOCRjGAZTTbC+tTeB3eiyj1bnJg56nAqbQKBgQD5T0hTLJSoC1VWT/H6\nydLTiFjFBxp1PeoTv7KcRP/UAlDgHCf1GobZrKo3rOKLbjJ9iOkNjGVLVqi17/iK\n4JEEOu6NSir3MQx/2j01HUEXm5ji3Bh2R0GU4WeLqUF7zFwEhBY/MNGRfD+Z5KuT\nIV8uYripsumsQ41/puNc7/VMzwKBgQDNvqdjmjSCVQBtcp8sWCqez87/WZIQ03kz\n8150oFWI48LmZeL0fB6CnmlEWDMvAGYacN3owyT64FbbMowxIiwN4k3Tw32DDC4p\nC3S/PXVlwtRwxiBSdD7DHDzXXwKl6nfR7e1FKO6M330LRgaYOBcGCXxGfC8KXvrF\nIT6fNSO4NQKBgQCkrgQePMJtRh82hlRWzl3esJ/CdfC6JQ2rweKfasx6JJV7k92o\n/763pmBBqodyhnX/iiI3etemLjX/B+ZrBe+EldDhr242HkYdZfEsVoiaqYMRx0S5\nTFQ7nbCiBkllFxZpPT7cusiTizkP1IapB1Ax+a/1GGNWEME04u4og7DK7QKBgQCo\nAAga0q4Rxmrk8/V5djzHFRUHeRJGXwfXHeCBBvMRJjndfFDIJhmbutJmFkclGARH\njuYEzGQD3u/NaQcEj8y9QY8fXb+9JFME/O/FwN99yotB0uZNrdIZ65LaoiA9bqmM\nZ+WY1YWEznECpZl47kQOj+xEed7HbysBkNXblr6mCQKBgHTii3lUddeieJP1VKG/\nYf8farg8WvlsSu9kYRikaBPSzgNn4iuP3ZixMUJy40YBM86ehqCWFNIMMqP+8Kv3\n8B+2Rh8JBR/sohNnCeCjLCGbNxcLZ+yv0Ok+UQt8uHB+6jqxaW0rlH/Nll+ytqXZ\nRc+kdy2OmICnEpo3WvHR659K\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-45afr@upwork-7aafa.iam.gserviceaccount.com",
    "client_id": "101368472993344267063",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-45afr%40upwork-7aafa.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(service_account)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://upwork-7aafa-default-rtdb.firebaseio.com'
})

accountRef = db.reference('/accounts')


def service_account_login():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    if os.path.exists('../gmail-credential/token.pickle'):
        with open('../gmail-credential/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../gmail-credential/credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../gmail-credential/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print('An error occurred: %s' % e)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    return {'raw': raw_message}


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)


while True:
    print("=========== START CHECKING ===========")
    data = accountRef.order_by_child('status').equal_to(sys.argv[1]).get()
    keys = list(data.keys())
    print(len(keys))
    for index, key in enumerate(keys):
        if data[key]['type'] == 'generator.email':
            continue
        mail = data[key]['email']
        token = data[key]['token']

        print("      " + str(index + 1) + "\t\t" + mail)

        try:
            msgs = 0
            if 'received' in data[key]:
                msgs = data[key]['received']

            messages = []

            inbox = TempMailInbox(address=mail, access_token=token)
            received_mails = inbox.get_all_mails()

            if (len(received_mails) > msgs):
                new_mails = received_mails

                flag = False
                verifyNum = 0

                for mail_item in new_mails:
                    messages.append(mail_item.subject)
                    if mail_item.subject.count('Welcome to Upwork') > 0 or mail_item.subject.count('Verify your email address') > 0 or mail_item.subject.count('Welcome to MinuteInbox') > 0 or mail_item.subject.count('Welcome to FakeMail') > 0 or mail_item.subject.count("Let’s keep your momentum going") > 0:
                        continue
                    elif mail_item.subject.count('Action required') > 0:
                        verifyNum += 1
                        if (verifyNum > 1):
                            flag = True
                        continue
                    sender = 'ANTI-UPWORK'
                    to = os.getenv("MAIL_RECEIVER")
                    subject = mail_item.subject
                    message_text = mail
                    service = service_account_login()
                    msg = create_message(sender, to, subject, message_text)
                    if (sys.argv[1] == 'sent'):
                        send_message(service, 'me', msg)

                ref = db.reference('/accounts/' + key)
                if flag:
                    ref.update({
                        'status': 'delete',
                        'received': len(received_mails),
                        'messages': messages
                    })
                    print("      DELETED-0: " + mail + "\n")
                else:
                    ref.update({
                        'received': len(received_mails),
                        'messages': messages
                    })
        except Exception as e:
            if (str(e).count('Expecting value: line 1 column 1 (char 0)') > 0):
                ref = db.reference('/accounts/' + key)
                ref.delete()
                print("      DELETED-1: " + mail + "\n")
            else:
                print(str(e))
    print("=========== END   CHECKING ===========")
    time.sleep(1)
