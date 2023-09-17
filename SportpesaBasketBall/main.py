import time
from selenium import webdriver
import re
from datetime import datetime
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

site = "https://www.ke.sportpesa.com/en/live/events/9940575/markets?sportId=10"
driver = webdriver.Chrome()

driver.get(site)
driver.maximize_window()
time.sleep(10)
slip_bar = driver.find_element(By.CLASS_NAME, "betslip-options-trigger")
slip_bar.click()

accept_oddschange = driver.find_elements(By.XPATH, '//input[@type="radio"]')
accept_oddschange[0].click()

default_amount = driver.find_element(By.ID, 'amount-user')
default_amount.clear()
default_amount.send_keys(50)

direct_bet_mode = driver.find_elements(By.CLASS_NAME, 'material-toggle')[1]
driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                direct_bet_mode)
direct_bet_mode.click()


time.sleep(333)