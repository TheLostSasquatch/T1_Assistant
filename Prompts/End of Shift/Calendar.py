import requests
from datetime import date, timedelta
import json
import sys
sys.path.append("*********")
from BearerToken import token

# Set up authentication headers
instance_url = 'https://********prod.my.salesforce.com'
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

# Define tomorrow's date and the date range for the query
tomorrow = date.today() + timedelta(days=1)
start_date = tomorrow.isoformat() + 'T00:00:00.000Z'
end_date = (tomorrow + timedelta(days=1)).isoformat() + 'T00:00:00.000Z'

# Define the SOQL query
soql_query = f"SELECT Id, Subject, StartDateTime, EndDateTime FROM Event WHERE StartDateTime >= {start_date} AND StartDateTime < {end_date}"

# Define the API endpoint
api_endpoint = instance_url + '/services/data/v51.0/query'

# Make the request to run the query
response = requests.get(api_endpoint, headers=headers, params={'q': soql_query})

# Check for successful API response
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit()

# Parse the JSON response
events = json.loads(response.text)['records']

# Print the events
for event in events:
    print(event['Subject'], event['StartDateTime'], event['EndDateTime'])
