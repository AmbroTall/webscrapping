import datetime
import json
import pickle
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys

options = uc.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode if needed
# options.add_argument("--no-sandbox")
# options.addimport requests

website = 'https://twitter.com/i/flow/login'
# path = '/home/ambrose/Documents/chromedriver'
driver = uc.Chrome(options=options)

username = "paolosiroko@gmail.com"
password = "$Kwendo@2023"
driver.get(website)

def login_twitter():
    username_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'))
    )
    username_field.send_keys(username)

    username_field.send_keys(Keys.TAB)
    username_field.send_keys(Keys.ENTER)


    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.TAB)
    password_field.send_keys(Keys.ENTER)


# scroll my timeline
def find_posts():
    # timeline_container = driver.find_element(By.XPATH,'//div[@aria-label="Timeline: Your Home Timeline"]')
    timeline_container = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//div[@aria-label="Timeline: Your Home Timeline"]')))
    post_container = timeline_container.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
    print(len(post_container))
    for index, post in enumerate(post_container, start=1):
        print(f"Post number {index}", post.text)


def post():
    input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//div[@role="textbox"]')))
    input.click()
    input.send_keys("\n Do you believe in the Red Devils' victory tonight? \n If you're backing Manchester United to triumph in today's match, join the winning team and follow me. Let's share the joy of victory together!  #Amrabat #MUFC #MUNCRY #GGMU #Sancho #Russia #Ferguson #mount #old ..")

    time.sleep(2)
    post_btn = driver.find_element(By.XPATH,
                                   '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]')
    post_btn.click()




def main():
    login_twitter()
    post()
    find_posts()
    time.sleep(33333)


main()
# title="Sign in with Google Dialog"
