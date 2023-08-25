import time
import random

# from selenium import webdriver
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.support.ui import Select

options = ChromeOptions()
url = 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp'
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = uc.Chrome(options=options)


class CreateGmailAccount:
    def __init__(self):
        pass

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get(url)

    def maximize_window(self):
        driver.maximize_window()

    def click_next(self):
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        time.sleep(5)  # wait for next page to load

    def click_skip(self):
        skip_button = driver.find_element(By.XPATH, "//span[text()='Skip']")
        skip_button.click()
        time.sleep(5)  # wait for next page to load

    def create_account(self, f_name, surname, pwd, day, month, year, gender, recovery_mail):
        first_name = driver.find_element(By.ID, 'firstName')
        first_name.send_keys(f_name)
        time.sleep(1)

        sur_name = driver.find_element(By.ID, 'lastName')
        sur_name.send_keys(surname)
        time.sleep(1)

        self.click_next()

        day_input = driver.find_element(By.ID, "day")
        day_input.send_keys(day)
        time.sleep(1)

        # Find the dropdown element by its name, ID, or other appropriate locator
        dropdown_month = driver.find_element(By.ID, "month")
        drop_month = Select(dropdown_month)
        drop_month.select_by_visible_text(month)  # Select an option by visible text
        time.sleep(1)

        year_input = driver.find_element(By.ID, "year")
        year_input.send_keys(year)
        time.sleep(1)

        # Find the dropdown element by its name, ID, or other appropriate locator
        dropdown_gender = driver.find_element(By.ID, "gender")
        drop_gender = Select(dropdown_gender)
        drop_gender.select_by_visible_text(gender)  # Select an option by visible text
        time.sleep(1)

        self.click_next()

        time.sleep(1)
        # time.sleep(3333333)
        random_numbers = [random.randint(1, 100) for _ in range(4)]
        combined_number = int(''.join(map(str, random_numbers)))

        email_address = driver.find_element(By.XPATH, '//input[@aria-label="Username"]')
        email_address.send_keys(f'{surname}{f_name}{combined_number}')
        time.sleep(1)

        self.click_next()

        password = driver.find_element(By.XPATH, '//input[@aria-label="Password"]')
        password.send_keys(pwd)

        confirm_password = driver.find_element(By.XPATH, '//input[@aria-label="Confirm"]')
        confirm_password.send_keys(pwd)

        show_password = driver.find_element(By.XPATH, '//input[@type="checkbox"]')
        show_password.click()

        self.click_next()

        recovery_email = driver.find_element(By.ID, 'recoveryEmailId')
        recovery_email.send_keys(recovery_mail)
        time.sleep(1)

        self.click_skip()

        self.click_next()

        agree = driver.find_element(By.XPATH, "//span[text()='I agree']")
        agree.click()
        time.sleep(5)
