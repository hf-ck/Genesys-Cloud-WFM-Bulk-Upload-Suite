from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import json
import requests
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load configuration
with open('config.json') as f:
    config = json.load(f)

client_id = config['client_id']
client_secret = config['client_secret']

# Authenticate and get the API client
api_client = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(client_id, client_secret)

# Create an instance of the Users API class
usersApi = PureCloudPlatformClientV2.UsersApi(api_client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        df = pd.read_excel(file_path)
        # Clean and prepare data for rendering
        table_html = df.to_html(classes='table table-striped', index=False)
        return render_template('preview.html', file=file.filename, table_html=table_html)

@app.route('/process', methods=['POST'])
def process():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['file'])
    df = pd.read_excel(file_path)

    # Function to get user ID by email address
    def get_user_id_by_email(email):
        UserDict = {
            "pageSize": 1,  # Limit to 1 result for exact match
            "pageNumber": 1,
            "query": [
                {
                    "type": "EXACT",
                    "fields": ["email"],
                    "value": email
                }
            ]
        }

        try:
            # Search for the user by email to get the user ID
            response = usersApi.post_users_search(UserDict)
            if response.results:
                user_info = response.results[0]
                user_id = user_info.id
                print(f"User info for {email}: {user_info}")
                return user_id
            else:
                print(f"No results for {email}")
                return None
        except ApiException as e:
            print(f"Exception when searching for {email}: {e}")
            return None

    # OAuth 2.0 Token Request
    def get_oauth_token(client_id, client_secret):
        url = "https://login.mypurecloud.com/oauth/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("Failed to get OAuth token:", response.status_code, response.text)
            exit()

    # Get the OAuth token
    oauth_token = get_oauth_token(client_id, client_secret)

    results = []
    # Process the data from the Excel file
    for index, row in df.iterrows():
        email = row['Email Address']
        user_id = get_user_id_by_email(email)
        
        if user_id:
            email_max_capacity = int(row['Email Maximum Capacity'])
            email_interruptable_media_types = row['Email Interruptable Media Types'].split(',') if pd.notna(row['Email Interruptable Media Types']) else []

            chat_max_capacity = int(row['Chat Maximum Capacity'])
            chat_interruptable_media_types = row['Chat Interruptable Media Types'].split(',') if pd.notna(row['Chat Interruptable Media Types']) else []

            message_max_capacity = int(row['Message Maximum Capacity'])
            message_interruptable_media_types = row['Message Interruptable Media Types'].split(',') if pd.notna(row['Message Interruptable Media Types']) else []

            callback_max_capacity = int(row['Callback Maximum Capacity'])
            callback_interruptable_media_types = row['Callback Interruptable Media Types'].split(',') if pd.notna(row['Callback Interruptable Media Types']) else []

            call_max_capacity = int(row['Call Maximum Capacity'])
            call_interruptable_media_types = row['Call Interruptable Media Types'].split(',') if pd.notna(row['Call Interruptable Media Types']) else []

            workitem_max_capacity = int(row['Workitem Maximum Capacity'])
            workitem_interruptable_media_types = row['Workitem Interruptable Media Types'].split(',') if pd.notna(row['Workitem Interruptable Media Types']) else []

            # Update the payload with new values
            payload = {
                "utilization": {
                    "email": {
                        "maximumCapacity": email_max_capacity,
                        "interruptableMediaTypes": email_interruptable_media_types,
                        "includeNonAcd": False
                    },
                    "chat": {
                        "maximumCapacity": chat_max_capacity,
                        "interruptableMediaTypes": chat_interruptable_media_types,
                        "includeNonAcd": False
                    },
                    "message": {
                        "maximumCapacity": message_max_capacity,
                        "interruptableMediaTypes": message_interruptable_media_types,
                        "includeNonAcd": False
                    },
                    "callback": {
                        "maximumCapacity": callback_max_capacity,
                        "interruptableMediaTypes": callback_interruptable_media_types,
                        "includeNonAcd": False
                    },
                    "call": {
                        "maximumCapacity": call_max_capacity,
                        "interruptableMediaTypes": call_interruptable_media_types,
                        "includeNonAcd": False
                    },
                    "workitem": {
                        "maximumCapacity": workitem_max_capacity,
                        "interruptableMediaTypes": workitem_interruptable_media_types,
                        "includeNonAcd": True
                    }
                }
            }

            endpoint = f"https://api.mypurecloud.com/api/v2/routing/users/{user_id}/utilization"
            headers = {
                "Authorization": f"Bearer {oauth_token}",
                "Content-Type": "application/json"
            }

            # Print endpoint and payload for debugging
            print(f"Updating user utilization at endpoint: {endpoint}")
            print(f"Payload: {json.dumps(payload, indent=2)}")

            # Send the payload to Genesys Cloud
            response = requests.put(endpoint, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                results.append(f"Updated utilization for user with email {email}")
            else:
                results.append(f"Failed to update utilization for user with email {email}: {response.status_code}, {response.text}")
        else:
            results.append(f"User ID not found for email {email}")

    return render_template('results.html', results=results)

@app.route('/reset', methods=['POST'])
def reset():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
