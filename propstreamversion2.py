import json
import time
from datetime import datetime
import mysql.connector

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
import requests

# Set up Chrome options for headless mode
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
website = 'https://app.propstream.com/search'
propstream_session = requests.Session()

propstream_email = "jewelercart@gmail.com"
propstream_pwd = "Taqwah79@@"
def login_session_propstream():
    while True:
        try:
            driver.get(website)
            # Explicit Wait until username is visible
            email_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']") ))
            email_input.clear()
            time.sleep(2)
            email_input.send_keys(propstream_email)
            # Explicit Wait until password input is visible
            password_input = driver.find_element(By.XPATH, "//input[@name='password']")  # Element filtration
            time.sleep(2)

            password_input.send_keys(propstream_pwd)
            login_btn = driver.find_element(By.XPATH, '//*[@id="form-content"]/form/button')
            time.sleep(2)
            login_btn.click()
            driver.maximize_window()
            wait = WebDriverWait(driver, 30)

            # Define the XPath for the element you want to wait for
            element_xpath = '//*[@id="alert"]/div/div/div/div/div/div/div[2]/button/span'

            # Wait until the element is visible
            element = wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
            # Get the cookies
            cookies = driver.get_cookies()

            # Print the cookies
            for cookie in cookies:
                propstream_session.cookies.set(cookie['name'], cookie['value'])

            print("Logging in successfully ...")
            time.sleep(2)
            driver.quit()
            return True
        except:
            driver.refresh()
            try:
                wait = WebDriverWait(driver, 30)
                # Wait until the element is visible
                element = wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
                # Get the cookies
                cookies = driver.get_cookies()

                # Print the cookies
                for cookie in cookies:
                    propstream_session.cookies.set(cookie['name'], cookie['value'])

                print("Logging in successfully ...")
                time.sleep(2)
                driver.quit()
            except:
                driver.refresh()
                continue


def search_propstream(address):
    url = f"https://app.propstream.com/eqbackend/resource/auth/ps4/property/suggestionsnew?q={address}"

    payload = {}
    headers = {
        'authority': 'app.propstream.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://app.propstream.com/search',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-auth-token': 'd6560c197e02f999c1480004b38dfd2248d4fa68795c5bac7b'
    }

    response = propstream_session.get(url, headers=headers, data=payload)
    r = response.json()
    for property in r:
        if property['stateCode'] == "GA":
            print("Getting address id : Address --", r)
            return r[0]['id']
    return None



def get_propstream_address_details(id):
    url = f"https://app.propstream.com/eqbackend/resource/auth/ps4/property/{id}?m=F"

    payload = {}
    headers = {
        'authority': 'app.propstream.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://app.propstream.com/search/1743767474',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-auth-token': 'd6560c197e02f999c1480004b38dfd2248d4fa68795c5bac7b'
    }

    response = propstream_session.get(url, headers=headers, data=payload)
    r = response.json()
    print(r)

def main():
    address_db = '3440 Freedom Lane, Dalton, GA 30721'
    login = login_session_propstream()
    if login:
        property_id = search_propstream(address_db)
        if property_id:
            get_propstream_address_details(property_id)
        time.sleep(3333)

print(main())


