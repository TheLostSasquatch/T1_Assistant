import requests
import json
from secret import password

tokenurl = "https://*****.comservices/oauth2/token?grant_type=password&client_id=3MVG9yZ.WNe6byQBMXp.PrTbt47yoW2ZfaU1oTZ3kyt2_FOkvajF_xfx6fvHJl_wHw4643sfhcn45oYndny3W&client_secret=78391719339E8C0889F05A865DC27E34E71DB3D4B8E4C46D110FF76AB10DDFDB&username=ddexter@********.com&password=" + password
#username = input("What is your salesforce Username?\n")
#password = getpass("What is your password?\n")
#tokenurl = "https://*****.comservices/oauth2/token?grant_type=password&client_id=3MVG9yZ.WNe6byQBMXp.PrTbt47yoW2ZfaU1oTZ3kyt2_FOkvajF_xfx6fvHJl_wHw4643sfhcn45oYndny3W&client_secret=78391719339E8C0889F05A865DC27E34E71DB3D4B8E4C46D110FF76AB10DDFDB&username=" + username + "&password=" + password


payload={}
headers = {
'Cookie': 'BrowserId=_7xN5bepEe2iECO8hFqqHQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

gettoken = requests.request("POST", tokenurl, headers=headers, data=payload)
tokenresponse = json.loads(gettoken.text)
token = tokenresponse["access_token"]