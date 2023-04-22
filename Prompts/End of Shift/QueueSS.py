from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# SCREEN SHOT OF CURRENT QUEUE
# Navigate to the login page
driver.get('https://*****.com')

# Find the username input field and enter your username
username_field = driver.find_element(By.NAME, 'username')
username_field.send_keys('ddexter@********.com')

# Find the password input field and enter your password
password_field = driver.find_element(By.NAME, 'pw')
password_field.send_keys('****')

# Click the "Sign In" button to submit the form
sign_in_button = driver.find_element(By.NAME, 'Login')
sign_in_button.click()

# Wait for the dashboard page to load
time.sleep(5)

# Click the "Try Now" button to enter Lightning
try:
    tryNow_button = driver.find_element(By.NAME, 'tryNow')
    tryNow_button.click()
except:
    print("Already on Lightning")

# Wait for the dashboard page to load
time.sleep(5)

# Take a screenshot of the entire window
driver.save_screenshot('CurrentQueue.png')

#Swap back to classic
profilebutton = driver.find_element(By.CSS_SELECTOR, 'button.slds-button.branding-userProfile-button')
profilebutton.click()
time.sleep(5)
classicbutton = driver.find_element(By.LINK_TEXT, "Switch to Salesforce Classic")
classicbutton.click()

time.sleep(5)

# Close the browser window
driver.quit()

