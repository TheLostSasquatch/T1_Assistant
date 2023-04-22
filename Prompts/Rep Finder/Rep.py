import requests
import json
import sys
sys.path.append("*********")
from BearerToken import token

# Get Case Id
case = input("What is your case number?\n")
idurl = "https://*****.com/services/data/v45.0/query/?q=SELECT Account.Name, Account.SAP_ID__c, Account.Account_Manager_Name__c, Account.Account_Manager_Email__c, Account.Customer_Success_Manager_Name__c, Account.Customer_Success_Manager_Email__c FROM Case WHERE CaseNumber = '" + case + "'"

payload={}
headers = {
    'Authorization': 'Bearer ' + token,
    'Cookie': 'BrowserId=_7xN5bepEe2iECO8hFqqHQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

getid = requests.request("GET", idurl, headers=headers, data=payload)
idresponse = json.loads(getid.text)
accountname = idresponse['records'][0]['Account']['Name']
am = idresponse['records'][0]['Account']['Account_Manager_Name__c']
amemail = idresponse['records'][0]['Account']['Account_Manager_Email__c']
csm = idresponse['records'][0]['Account']['Customer_Success_Manager_Name__c']
csmemail = idresponse['records'][0]['Account']['Customer_Success_Manager_Email__c']
sapid = idresponse['records'][0]['Account']['SAP_ID__c']

print(accountname,"\nSAP ID:",sapid,"\nAccount Manager:",am,"Email:",amemail,"\nCustomer Success Manager:",csm,"Email:",csmemail)