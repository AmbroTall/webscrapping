import time
# from selenium import webdriver
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.support.ui import Select


options = ChromeOptions()
url = 'https://www.facebook.com/'
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = uc.Chrome(options=options)

class CreateFacebookAccount:
    def __init__(self):
        pass

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        # print("Ambro1")
        driver.get(url)

    def maximize_window(self):
        driver.maximize_window()

    def login(self, f_name,surname, mail, pwd, day, month, year, gender):
        # WebDriverWait(teamdiv, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'live-match__teams__home')))

        create_account_btn = driver.find_elements(By.TAG_NAME, 'a')
        [l.click() for l in create_account_btn if l.text == "Create new account"]
        time.sleep(1)

        first_name = driver.find_element(By.XPATH, '//input[@aria-label="First name"]')
        first_name.send_keys(f_name)
        time.sleep(1)

        sur_name = driver.find_element(By.XPATH, '//input[@aria-label="Surname"]')
        sur_name.send_keys(surname)
        time.sleep(1)

        email = driver.find_element(By.XPATH, '//input[@aria-label="Mobile number or email address"]')
        email.send_keys(mail)
        time.sleep(1)

        confirm_email = driver.find_element(By.XPATH, '//input[@aria-label="Re-enter email address"]')
        confirm_email.send_keys(mail)
        time.sleep(1)

        password = driver.find_element(By.XPATH, '//input[@aria-label="New password"]')
        password.send_keys(pwd)
        time.sleep(1)

        # Find the dropdown element by its name, ID, or other appropriate locator
        dropdown_day = driver.find_element(By.ID, "day")
        drop_day = Select(dropdown_day)
        drop_day.select_by_visible_text(day)   # Select an option by visible text
        time.sleep(1)

        # Find the dropdown element by its name, ID, or other appropriate locator
        dropdown_month = driver.find_element(By.ID, "month")
        drop_month = Select(dropdown_month)
        drop_month.select_by_visible_text(month)   # Select an option by visible text
        time.sleep(1)

        # Find the dropdown element by its name, ID, or other appropriate locator
        dropdown_year = driver.find_element(By.ID, "year")
        drop_year = Select(dropdown_year)
        drop_year.select_by_visible_text(year)   # Select an option by visible text
        time.sleep(1)

        if gender == "male":
            sex = driver.find_elements(By.XPATH,'//input[@type="radio"]')[1]
        elif gender == "female":
            sex = driver.find_elements(By.XPATH,'//input[@type="radio"]')[0]
        else:
            sex = driver.find_elements(By.XPATH,'//input[@type="radio"]')[2]

        sex.click()
        [x.click() for x in driver.find_elements(By.XPATH, '//button[@type="submit"]') if x.text == "Sign Up"]







