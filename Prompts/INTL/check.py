import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("*********")
from secret import salesforcepassword
from BearerToken import token
import json
from pprint import pprint
import paramiko

# Get SAPID
case = input("What is your case number?\n")
idurl = f"https://*****.com/services/data/v45.0/query/?q=SELECT Account.Name, Account.SAP_ID__c FROM Case WHERE CaseNumber = '{case}'"

payload={}
headers = {
    'Authorization': 'Bearer ' + token,
    'Cookie': 'BrowserId=_7xN5bepEe2iECO8hFqqHQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

getid = requests.request("GET", idurl, headers=headers, data=payload)
idresponse = json.loads(getid.text)
accountname = idresponse['records'][0]['Account']['Name']
sapid = idresponse['records'][0]['Account']['SAP_ID__c']

# Look for INTL in ******** Portal
url = 'https://customer.********.com'
data_url = f'{url}/index.php/enterprise-manager?cmd=getEnterpriseServices&task=ajax&customerEID={sapid}'

# Login to ******** Portal
username = "****"
password = salesforcepassword
session = requests.Session()
response = session.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', attrs={'value': '1'})['name']
login_data = {
    'username': username,
    'password': password,
    csrf_token: '1',
    'option': 'com_users',
    'task': 'user.login'
    }

# Search for INTL Status
response = session.post(url, data=login_data)
response.raise_for_status()

response = session.post(data_url)
response.raise_for_status()
dictt = json.loads(response.text)

# Extract the value of internationalTermination key
international_termination = dictt['services'][6]['productionStatus']

# Convert international_termination to True/False
if international_termination == 0:
    print(sapid,accountname,"is not contracted for international dialing")
if international_termination == 1:
    # Look for Trunk Names in ******** Portal
    url = 'https://customer.********.com'
    data_url = f'{url}/index.php/number-administration-search/trunkgroup?task=ajax&cmd=searchInventory&type=TrunkGroup&peek=1&f%5B%5D=Customer+ID&v%5B%5D={sapid}&_search=false&nd=1681771947373&numRecords=250&page=1&sortBy=&sortDirection=asc'

    # Login to ******** Portal
    username = "******"
    password = salesforcepassword
    session = requests.Session()
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', attrs={'value': '1'})['name']
    login_data = {
        'username': username,
        'password': password,
        csrf_token: '1',
        'option': 'com_users',
        'task': 'user.login'
        }

    # Search for INTL Status
    response = session.post(url, data=login_data)
    response.raise_for_status()

    response = session.post(data_url)
    response.raise_for_status()
    dictt = json.loads(response.text)
    trunks = []
    for trunk in dictt['numbers']:
        trunks.append(trunk['******** Trunk Name'])
    for trunk in trunks:
        # Define the SSH connection details
        hostname = '*****'   # Replace with the hostname or IP address of the remote server
        port = 22                   # Replace with the SSH port of the remote server
        username = 'a-*****' # Replace with your username on the remote server
        password = '******' # Replace with your password on the remote server

        # Create an SSH client object
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote server
            client.connect(hostname, port, username, password)

            # Run a command on the remote server
            command = f'sendcmd host=srprov01.den02.********.net command=listIntlTG tg={trunk}' # Replace with the command you want to run
            stdin, stdout, stderr = client.exec_command(command)

            # Print the output of the command
            print(stdout.read().decode())

            # Close the SSH connection
            client.close()

        except Exception as e:
            print(f'Error: {e}')
            client.close()
                


    print(sapid,accountname,"is contracted for international dialing")
