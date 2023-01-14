import undetected_chromedriver as uc
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_email(email, password):
    # By passing Your connection is not private
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'details-button'),
            )
        )

        advanced_btn = driver.find_element(By.ID, 'details-button')
        advanced_btn.click()

        proceed_link = driver.find_element(By.ID, 'proceed-link')
        proceed_link.click()
    except:
        print("All clear")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'user'),
        )
    )

    email_input = driver.find_element(By.ID, 'user')
    email_input.send_keys(email)

    pswd_input = driver.find_element(By.ID, 'pass')
    pswd_input.send_keys(password)

    login_btn = driver.find_element(By.ID, 'login_submit')
    login_btn.click()

def click_mail_to_verify():
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'messagelist'),
        )
    )

    refresh = driver.find_element(By.ID, "rcmbtn115")
    refresh.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'messagelist'),
        )
    )


    msg = driver.find_element(By. XPATH, '//*[@id]/td[2]/span[4]/a/span')
    msg.click()

    msg_frame = driver.switch_to.frame("messagecontframe")

    verify_account = driver.find_element(By.XPATH, '//*[@id="message-htmlpart1"]/div/center/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a')
    verify_account.click()



web_email = "corp@jbetadev.com"
web_password = "tech2022@@"

path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
link = 'https://client.jewelercart.com:2096/'
driver.get(link)
login_to_mail = login_to_email(web_email, web_password)
verify_email = click_mail_to_verify()
time.sleep(9999);