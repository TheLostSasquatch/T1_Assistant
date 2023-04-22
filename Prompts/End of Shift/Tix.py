import requests
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

#Total Cases
# Define the report ID and API endpoint
report_id = '00O16000007Lmjg'
total_api_endpoint = instance_url + '/services/data/v51.0/analytics/reports/' + report_id

# Make the request to run the report
response = requests.get(total_api_endpoint, headers=headers)

# Parse the response into a dictionary
total_response_dict = json.loads(response.text)

# Get the total number of cases in the report
total_cases = total_response_dict['factMap']['T!T']['aggregates'][1]['value']

print('Total cases:', total_cases)

#Total Escalations (This works as long as people use the escalation checkbox)
# Define the report ID and API endpoint
escalate_report_id = '00O4p000004ckQZ'
escalate_api_endpoint = instance_url + '/services/data/v51.0/analytics/reports/' + escalate_report_id

# Make the request to run the report
escalate_response = requests.get(escalate_api_endpoint, headers=headers)

# Parse the response into a dictionary
esc_response_dict = json.loads(escalate_response.text)

# Get the total number of cases in the report
esc_cases = esc_response_dict['factMap']['T!T']['aggregates'][1]['value']

print('Total Escalations:', esc_cases)