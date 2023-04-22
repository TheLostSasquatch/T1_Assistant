import requests
import json
import sys
sys.path.append("*********")
from BearerToken import token

# Get Case Id
case = "01031694"
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

#Assign Case to NumberAdmin

url = "https://*****.comservices/data/v51.0/sobjects/Case/" + caseid

payload = json.dumps({
"RecordTypeId": "012G00000017ARPIA2",
"Status": "Email Recieved",
"OwnerId": "005G0000001lnPFIAY",
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
            "emailBody" : "Hey Number Admin" + case + " has been assigned to you",
            "emailAddresses" : "provisioning@********.com",
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