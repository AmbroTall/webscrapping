import time
from datetime import datetime
from selenium.webdriver.support.ui import Select

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = "http://100093.pythonanywhere.com/"

# Set up Chrome options for headless mode
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode without a GUI

username = "Ndoneambrose"
pwd = "ambroseTall3436!"
driver = webdriver.Chrome(options=chrome_options)


def dowell_login():
    driver.get(website)
    driver.maximize_window()

    # Wait for the page to load (you can adjust the timeout as needed)
    wait = WebDriverWait(driver, 30)
    username_input = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_input.send_keys(username)
    password_input = driver.find_element(By.ID, "form-field-password")
    password_input.send_keys(pwd)

    login_btn = driver.find_element(By.ID, 'memberloginbtn')
    login_btn.click()


def click_portfolio():
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.ID, 'productbtn')))
    # Wait for the page to load (you can adjust the timeout as needed)
    dropdown = driver.find_element(By.NAME, 'org')
    # Select the option by its value attribute
    dropdown = Select(dropdown)
    dropdown.select_by_value('HR_Dowell Research')


def scroll_element_into_view(x):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", x)
    time.sleep(5)

def click_products():
    # Wait for the page to load (you can adjust the timeout as needed)
    wait = WebDriverWait(driver, 60)
    element = wait.until(EC.presence_of_element_located((By.ID, 'productbtn')))
    scroll_element_into_view(element)
    element.click()

    time.sleep(5)
    # select product
    product_dropdown = Select(driver.find_element(By.ID, 'form-field-name'))
    scroll_element_into_view(driver.find_element(By.ID, 'form-field-name'))
    # Select the option by its value attribute
    product_dropdown.select_by_value('Team Management')

    # select portfolio
    portfolio_dropdown = Select(driver.find_element(By.ID, 'form-field-field_29d6b3b'))
    scroll_element_into_view(driver.find_element(By.ID, 'form-field-field_29d6b3b'))
    # Select the option by its value attribute
    portfolio_dropdown.select_by_value('674527')

    # click button
    login_hr_portal = driver.find_element(By.XPATH,
                                          '//*[@id="productlogo"]/div/div/div/div/div/div[9]/div/form/div/div[4]')
    scroll_element_into_view(login_hr_portal)
    login_hr_portal.click()


def main():
    dowell_login()
    click_portfolio()
    click_products()
print(main())
