import requests
import json
import sys
sys.path.append("*********")
from BearerToken import token
#from Outlooktoken import access_token

# Get Case Id
#case = input("What is your case number?\n")
#case = '01031714'
case = sys.argv[2]
idurl = "https://*****.com/services/data/v45.0/query/?q=SELECT Id FROM Case WHERE CaseNumber = '" + case + "'"

payload={}
headers = {
    'Authorization': 'Bearer ' + token,
    'Cookie': 'BrowserId=_7xN5bepEe2iECO8hFqqHQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

getid = requests.request("GET", idurl, headers=headers, data=payload)
idresponse = json.loads(getid.text)
caseid = idresponse['records'][0]['Id']

print(caseid)

#Assign Case to Billing

url = "https://*****.comservices/data/v51.0/sobjects/Case/" + caseid

payload = json.dumps({
"RecordTypeId": "0121L000000WerHQAS",
"Status": "New",
"OwnerId": "00G16000004p7Q1EAI",
})
headers = {
'Sforce-Auto-Assign': 'False',
'Authorization': 'Bearer ' + token,
'Content-Type': 'application/json',
'Cookie': 'BrowserId=fSYc37elEe2Cts8v-wZCXw; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

complete = requests.request("PATCH", url, headers=headers, data=payload)

#Send Email to New Owner

url = "https://*****.comservices/data/v56.0/actions/standard/emailSimple"

payload = json.dumps(
{
    "inputs" : [
        {
            "emailBody" : "Hey Billing " + case + " has been assigned to you",
            "emailAddresses" : "dl-csr@********.com",
            "emailSubject" : "Hey " + case + " has been assigned to you",
            "senderType" : "CurrentUser"
        }
    ]
})
headers = {
'Authorization': 'Bearer ' + token,
'Content-Type': 'application/json',
'Cookie': 'BrowserId=fSYc37elEe2Cts8v-wZCXw; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

sendemail = requests.request("POST", url, headers=headers, data=payload)