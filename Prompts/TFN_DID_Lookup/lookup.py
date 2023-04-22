import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("*********")
from secret import salesforcepassword
from secret import neustarpassword
import json
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
import time
import re

numbers = ["8008778111", "8587769581"]
 
# Set options for running Chrome in headless mode  
chrome_options = Options()  
chrome_options.add_argument("--headless")  
  
# Create a new Chrome webdriver instance with the headless option    
driver = webdriver.Chrome(options=chrome_options)

# Look for number in ******** Portal
url = 'https://customer.********.com'

for number in numbers:
    # Determine TFN or DID
    if number.startswith(("800","888","877","866","855","844","833")):
        data_url = f'{url}/index.php/number-administration-search/toll-free?task=ajax&cmd=searchInventory&type=TollFree&peek=1&f[]=Toll-Free+Number&v[]={number}&grid-page=1&_search=false&nd=1681338487481&numRecords=250&page=1&sortBy=&sortDirection=asc'
        type = "TFN"
    else:
        data_url = f'{url}/index.php/number-administration-search/local?task=ajax&cmd=searchInventory&type=DID&peek=1&f[]=DID Number&v[]={number}&grid-page=1&_search=false&nd=1681336972630&numRecords=250&page=1&sortBy=&sortDirection=asc'
        type = "DID"

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

    # Search for number
    response = session.post(url, data=login_data)
    response.raise_for_status()

    response = session.post(data_url)
    response.raise_for_status()
    dictt = json.loads(response.text)

    if dictt["recordCount"] == 0:
        if type == "DID":
            # Navigate to the login page  
            driver.get('https://numbering.neustar.biz/login')  
            
            # Find the username input field and enter your username  
            username_field = driver.find_element(By.NAME, 'username')  
            username_field.send_keys('support@********.com')  
            
            # Find the password input field and enter your password  
            password_field = driver.find_element(By.NAME, 'password')  
            password_field.send_keys(neustarpassword)  
            
            # Click the "Sign In" button to submit the form  
            sign_in_button = driver.find_element(By.ID, 'login-submit')  
            sign_in_button.click()  
            
            # Find the password input field and enter your password  
            search_field = driver.find_element(By.NAME, 'portps-search-keyword')  
            search_field.send_keys(number)  
            
            # Click the "Search" button to submit the form  
            search_button = driver.find_element(By.ID, 'portps-search-submit')  
            search_button.click()  
            
            time.sleep(2)  
            
            # Find the element by its id    
            element = driver.find_element(By.ID,"tn_code_owner")    
                
            # Get the text of the element    
            owner = element.text    
            
            # Print the value of the owner variable    
            print(number,"This is not an ******** number", owner, "owns this number")
        if type == "TFN":
            area_code = number[:3]  
            local_number = number[3:]  
            
            # Navigate to the login page
            driver.get('https://www.somos.com/find-toll-free-number?searchType=number')  

            # Click the "Area Code" button 
            area_button = driver.find_element(By.CSS_SELECTOR, f'label[for="ac-{area_code}"]')  
            area_button.click()  
            
            # Enter the "Number" in the search field  
            search_field = driver.find_element(By.ID, 'phone-number-search')  
            search_field.send_keys(local_number)

            time.sleep(2) 

            # Click the "Search" button to submit the form  
            search_button = driver.find_element(By.ID, 'js-get-toll-free')  
            search_button.click()  
            
            time.sleep(10)  
            
            # Find the element by its id    
            element = driver.find_element(By.CLASS_NAME,"find-toll-free-number-results-item-text")    
                
            # Get the text of the element    
            tfresult = element.text    
            
            # Regex out owner
            pattern = r'reserved by\s+(.*?)\.'  
            owner = re.search(pattern, tfresult).group(1)  
            
            print(number,"This is not an ******** number", owner, "owns this number")


    else:
        enterprise_name = dictt['numbers'][0]['enterpriseName']
        print(number,"This number is owned by ******** the customer is",enterprise_name)


driver.quit()