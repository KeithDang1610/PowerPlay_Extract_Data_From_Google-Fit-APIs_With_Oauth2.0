import requests
import time
from google.oauth2 import service_account
#from google.cloud import storage
from pprint import pprint
import json
import csv
from google.auth.transport.requests import Request
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# def get_data():
#     import requests

#     res = requests.get("https://randomuser.me/api/")
#     res = res.json()
#     res = res['results'][0]
#     return res

# def format_data(res):
#     data = {}
#     location = res['location']
#     data['id'] = uuid.uuid4()
#     data['first_name'] = res['name']['first']
#     data['last_name'] = res['name']['last']
#     data['gender'] = res['gender']
#     data['address'] = f"{str(location['street']['number'])} ' ' {location['street']['name']}"\
#                     f"{location['city']}, {location['state']}, {location['country']}"
#     data['postcode']= res['location']['postcode']
#     data['email']=res['email']
#     data['username'] =res['login']['username']
#     data['dob'] = res['dob']['date']
#     data['registered_date'] = res['registered']['date']
#     data['phone'] = res['phone']
#     data['picture'] =res['picture']['medium']

#     return data

# def stream_data():
#     import json
#     from kafka import KafkaProducer
#     import time
#     import logging


#     producer = KafkaProducer(bootstrap_servers = ['broker:29092'], max_block_ms=5000)
#     curr_time =time.time()

#     while True:
#         if time.time() > curr_time + 60:
#             break
#         try:
#             res= get_data()
#             res = format_data(res)
#             producer.send('user_created', json.dumps(res).encode('utf-8'))
        
#         except Exception as e:
#             logging.error(f'An error occured: {e}')
#             continue


# with DAG('user_automation',
#         default_args=default_args,
#         schedule_interval='@daily',
#         catchup=False) as dag:
    
#    streaming_task = PythonOperator(
#        task_id = 'stream_data_from_api',
#        python_callable= stream_data
#    )

SCOPES = ["https://www.googleapis.com/auth/fitness.activity.read",
          "https://www.googleapis.com/auth/fitness.heart_rate.read",
          "https://www.googleapis.com/auth/fitness.location.read",
          "https://www.googleapis.com/auth/fitness.sleep.read",
          "https://www.googleapis.com/auth/fitness.reproductive_health.read"
          ]

# Path to the client secret file you downloaded
CLIENT_SECRETS_FILE = "client_secret.json"

# Authenticate and create the service
def get_fit_service():
    # Check if we already have a saved token.json file (to avoid re-authenticating each time)
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        # If there are no (valid) credentials, go through the OAuth flow
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service using the credentials
    service = build('fitness', 'v1', credentials=creds)
    return service

# Initialize the Google Fit API service
fit_service = get_fit_service()
