import requests
import json
import sys
sys.path.append("*********")
from BearerToken import token
import re

# Get Case Id
case = input("What is your case number?")
url = "https://*****.com/services/data/v45.0/query/?q=SELECT Description,Subject FROM Case WHERE CaseNumber = '" + case + "'"

payload={}
headers = {
    'Authorization': 'Bearer ' + token,
    'Cookie': 'BrowserId=_7xN5bepEe2iECO8hFqqHQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

getdscript = requests.request("GET", url, headers=headers, data=payload)
dscriptresponse = json.loads(getdscript.text)
dscript = dscriptresponse['records'][0]['Description']
subject = dscriptresponse['records'][0]['Subject']


if "Inteliquent" in subject:
    start_time_match = re.search(r"Start Time:\s*([A-Za-z]+,\s+[A-Za-z]+\s+\d+,\s+\d+:\d+:\d+\s+\w{2}\s+\(\w{3}\))", dscript)
    stop_time_match = re.search(r"Stop Time:\s*([A-Za-z]+,\s+[A-Za-z]+\s+\d+,\s+\d+:\d+:\d+\s+\w{2}\s+\(\w{3}\))", dscript)

    if start_time_match:
        start_time = start_time_match.group(1)
        stop_time = stop_time_match.group(1)
        print(start_time)
        print(stop_time)
    else:
        print("Start time not found.")
else:
    print("No")