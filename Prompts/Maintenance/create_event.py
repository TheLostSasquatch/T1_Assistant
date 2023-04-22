import msal
import requests
import json
from access_token import access_token

# Set up variables for authentication and calendar ID
calendar_id = '********'

# Set up headers with access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Set up the event data
event_data = {
    'subject': 'Test Event',
    'start': {
        'dateTime': '2023-04-15T10:00:00',
        'timeZone': 'Pacific Standard Time'
    },
    'end': {
        'dateTime': '2023-04-15T11:00:00',
        'timeZone': 'Pacific Standard Time'
    }
}

# Set up the API endpoint for creating a new event in the calendar
api_url = f'https://graph.microsoft.com/v1.0/me/calendars/{calendar_id}/events'

# Make the API call to create a new event in the specified calendar
response = requests.post(api_url, headers=headers, data=json.dumps(event_data))

# Check the response status code to see if the event was created successfully
if response.status_code == 201:
    print('Event created successfully!')
else:
    print(response.text,'\nFailed to create event\n',access_token)