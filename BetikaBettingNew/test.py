from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from  data import url,username,passwordc,password,day,year
import time
import json
import random
import sqlite3

driver = uc.Chrome()

def land_first_page():
    driver.get(url)

def first_name():
    username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'firstName'))
                )
    username_field.send_keys(username)
    clickable = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'collectNameNext'))
                )
    clickable.click()
def birth_gender():
    day_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'day'))
                )
    day_field.send_keys(day)

    month_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'month'))
                )
    if month_field.tag_name == 'select':
            select = Select(month_field)
            select.select_by_value('4')
    else:
        print("The 'month' element is not a select input.")


    year_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'year'))
                )
    year_field.send_keys(year)

    gender_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'gender'))
                )
    if gender_field.tag_name == 'select':
        select = Select(gender_field)
        select.select_by_value('1')
    else:
        print("The 'gender' element is not a select input.")

        next = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'birthdaygenderNext'))
                )
        next.click()

def email():
    select = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,'selectionc0'))
                    )
    time.sleep(2)
        # select.text
    select.click()

    clicknext = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,'next'))
                    )
    clicknext.click()
def password():
    password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="passwd"]/div[1]/div/div[1]/input'))
                )

    password_field.send_keys(password)
    time.sleep(2)
    passwordc_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="confirm-passwd"]/div[1]/div/div[1]/input'))
                )
    passwordc_field.send_keys(passwordc)
    time.sleep(2)
    passwordbutton = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,'createpasswordNext'))
                )
    passwordbutton.click()

def verification():
    time.sleep(100)


if __name__ == '__main__':
    try:
        land_first_page()
        first_name()
        birth_gender()
        email()
        password()
        verification()
    except Exception as e:
        print("error:", e)






