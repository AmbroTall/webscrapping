import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import calendar
from selenium.webdriver.support.wait import WebDriverWait
import pickle
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By

driver = uc.Chrome()

email = "ambrosetall@gmail.com"
password = "ambroseTall3436"

# Create a new instance of the Chrome driver
password_mail = "MoneyPrintingBots12345"
recovery_mail = "maziwamrefuajab@gmail.com"
driver.get('https://www.gmail.com')
time.sleep(5)
driver.execute_script("window.open('https://accounts.google.com/signup');")


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

    time.sleep(5)
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("google_cookies.pkl", "wb"))
    print("Coookie saved successfully")
    time.sleep(60)

# Function for wait for prescence of element
def wait_for_prescence_of_element(locator):
    # Wait for the presence of the element (e.g., by ID)
    wait = WebDriverWait(driver, 30)  # Wait up to 10 seconds
    element = wait.until(EC.presence_of_element_located((locator)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                          element)
    return element


# Function to generate random names
def generate_random_names():
    # Generate a random first name using a combination of letters
    first_name_mail = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
    # Generate a random last name using a combination of letters
    last_name_mail = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
    return first_name_mail, last_name_mail


def generate_random_birthday():
    # Generate a random birth year between 1978 and 2005
    birth_year = random.randint(1978, 2005)

    # Generate a random birth month (1-12)
    birth_month = random.randint(1, 12)

    # Generate a random day within a valid range for the selected month
    if birth_month in [1, 3, 5, 7, 8, 10, 12]:
        birth_day = random.randint(1, 31)
    elif birth_month == 2:
        # Check for leap years (divisible by 4)
        if birth_year % 4 == 0:
            birth_day = random.randint(1, 29)
        else:
            birth_day = random.randint(1, 28)
    else:
        birth_day = random.randint(1, 30)

    # Get the month name
    month_name = calendar.month_name[birth_month]

    # Combine the day, month, and year to create the birthday
    birthday = f"{birth_day} {month_name}, {birth_year}"
    print(birthday)
    return birth_day, month_name, birth_year


def random_gender():
    genders = ["Male", "Female"]
    return random.choice(genders)


def click_next():
    next_step = driver.find_element(By.XPATH, "//span[text()='Next']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                          next_step)
    next_step.click()

def gmail_account_creation():
    first_name_name, last_name_name = generate_random_names()
    dob, month, year = generate_random_birthday()
    gender = random_gender()

    # Fill in the registration form
    first_name = wait_for_prescence_of_element((By.NAME, "firstName"))
    first_name.send_keys(first_name_name)
    time.sleep(3)

    last_name = driver.find_element(By.NAME, "lastName")
    last_name.send_keys(last_name_name)
    time.sleep(3)

    click_next()

    # Second Page Form (DOB and Gender)
    day_birth = wait_for_prescence_of_element((By.NAME, "day"))
    day_birth.send_keys(dob)
    time.sleep(3)

    # Find the dropdown for month
    dropdown = Select(driver.find_element(By.ID, "month"))
    # Select an option by text (e.g., "January")
    desired_option_text = month
    dropdown.select_by_visible_text(desired_option_text)
    time.sleep(3)

    day_birth = driver.find_element(By.NAME, "year")
    day_birth.send_keys(year)
    time.sleep(3)

    # Find the dropdown for Gender
    dropdown = Select(driver.find_element(By.ID, "gender"))
    # Select an option by text (e.g., "January")
    gender_option_text = gender
    dropdown.select_by_visible_text(gender_option_text)
    time.sleep(3)

    click_next()

    # Third page form display
    choose_email = wait_for_prescence_of_element((By.ID, "selectionc0"))
    create_mail = choose_email.text
    time.sleep(1)

    print("This is the choosen/created email", create_mail)
    choose_email.click()  # Replace with your desired password
    time.sleep(3)

    click_next()

    # Fourth page screen
    password_input = wait_for_prescence_of_element((By.NAME, "Passwd"))
    password_input.send_keys(password_mail)
    time.sleep(3)

    confirm_password = driver.find_element(By.NAME, "PasswdAgain")
    confirm_password.send_keys(password_mail)  # Repeat your password
    time.sleep(3)

    click_next()

    # Fifth Screen Enter recovery_mail
    time.sleep(3)
    recovery_email = wait_for_prescence_of_element((By.NAME, "recovery"))
    recovery_email.send_keys(recovery_mail)

    click_next()

    # Sixth Screen Phone Number
    skip_step = wait_for_prescence_of_element((By.XPATH, "//span[text()='Skip']"))
    skip_step.click()

    # Sixth Screen Confirm Account Info
    time.sleep(5)
    click_next()

    # Seventh Page Terms And Conditions
    agree = wait_for_prescence_of_element((By.XPATH, "//span[text()='I agree']"))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", agree)
    agree.click()

def renew_cookies():
    with open("google_cookies.pkl", "rb") as cookie_file:
        cookies = pickle.load(cookie_file)
    # Add each cookie to the new session
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(2)
def main():
    # renew_cookies()
    login_to_email(email, password)
    # Load cookies from the "cookies.pkl" file
    renew_cookies()
    # Open the Google account creation page
    driver.switch_to.window(driver.window_handles[1])  # Switch to the second window
    # driver.get("https://accounts.google.com/signup")
    while True:
        try:
            #Create gmail account
            gmail_account_creation()
        except Exception as e:
            print("This is the error", e)
main()