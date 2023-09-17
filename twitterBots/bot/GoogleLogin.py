import pickle
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By

driver = uc.Chrome()

email = "ambrosetall@gmail.com"
password = "ambroseTall3436"

driver.get('https://www.gmail.com')
time.sleep(5)
def login_to_email(email, password):
    email_input = driver.find_element(By.ID, 'identifierId')
    email_input.send_keys(email)
    email_input.clear()
    email_input.send_keys(email)
    time.sleep(2)
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()
    time.sleep(10)  # wait for next page to load

    # enter password and click sign in button
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)

    time.sleep(3)
    signin_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    signin_button.click()

    time.sleep(30)
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("google_cookies.pkl", "wb"))
    print("Coookie saved successfully")


login_to_email(email, password)