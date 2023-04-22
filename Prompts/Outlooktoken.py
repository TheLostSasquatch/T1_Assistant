import requests
from msal import ConfidentialClientApplication
from datetime import datetime

# Set the credentials
client_id = '*****'
client_secret = '*****'
tenant_id = '*****'

# Create a ConfidentialClientApplication instance
app = ConfidentialClientApplication(client_id, client_secret, authority='https://login.microsoftonline.com/' + tenant_id)

# Acquire an access token
result = app.acquire_token_silent(scopes=['https://graph.microsoft.com/.default'], account=None)
if not result:
    result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

# Check for errors in token acquisition
if 'access_token' not in result:
    print(result.get('error'))
    print(result.get('error_description'))
    exit()

access_token = result['access_token']

print(access_token)

# Set up the email data
to = '******@********.com'
subject = 'Test Email'
body = 'This is a test email sent from Python using Microsoft Graph API.'
sent_datetime = datetime.now().isoformat() + "+00:00"  # Add time zone offset

# Create the email message
message = {
    'message': {
        'toRecipients': [{'emailAddress': {'address': to}}],
        'subject': subject,
        'body': {
            'contentType': 'text',
            'content': body
        },
        'sentDateTime': sent_datetime
    }
}

# Send the email
url = 'https://graph.microsoft.com/v1.0/users/*****/sendMail'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, json=message)

# Check for errors in email sending
if response.status_code == 202:
    print('Email sent successfully!')
else:
    print('Failed to send email. Status code: {}'.format(response.status_code))
    print(response.text)
