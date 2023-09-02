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

options = uc.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode if needed
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
website = 'https://twitter.com/'
# path = '/home/ambrose/Documents/chromedriver'
driver = uc.Chrome(options=options)

email = "ambrosetall@gmail.com"
password = "ambroseTall3436"

driver.get(
    'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
google_cookies = pickle.load(open("google_cookies.pkl", "rb"))
for cookie in google_cookies:
    cookie['domain'] = ".google.com"
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        pass

# twitter_cookies = pickle.load(open("twitter_cookies.pkl", "rb"))
# for cookie in twitter_cookies:
#     cookie['domain'] = ".twitter.com"
#     try:
#         driver.add_cookie(cookie)
#     except Exception as e:
#         pass

driver.get(website)


def login_twitter():
    # time.sleep(5)
    # Find all iframe elements
    # iframes_dialogue = driver.find_element(By.XPATH,'//iframe[@title="Sign in with Google Dialog"]')
    iframes_dialogue = try_catch('//iframe[@title="Sign in with Google Dialog"]')
    driver.switch_to.frame(iframes_dialogue)
    username = driver.find_element(By.TAG_NAME, 'button')
    username.click()
    driver.switch_to.default_content()

# scroll my timeline
def find_posts():
    # timeline_container = driver.find_element(By.XPATH,'//div[@aria-label="Timeline: Your Home Timeline"]')
    timeline_container = try_catch('//div[@aria-label="Timeline: Your Home Timeline"]')
    post_container = timeline_container.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
    print(len(post_container))
    for index, post in enumerate(post_container, start=1):
        print(f"Post number {index}", post.text)


def post():
    input = try_catch('//div[@role="textbox"]')
    input.click()
    input.send_keys("Hello guys.")

    time.sleep(2)

    post_btn = driver.find_element(By.XPATH,
                                   '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]')
    post_btn.click()


def try_catch(xpath):
    max_attempts = 5
    current_attempt = 1
    while current_attempt <= max_attempts:
        try:
            time.sleep(30)
            element = driver.find_element(By.XPATH, f'{xpath}')
            return element
        except Exception as e:
            print(f"Attempt {current_attempt} failed with error: {e}")
            if current_attempt < max_attempts:
                driver.refresh()
                print("Retrying...")
            else:
                print("Max attempts reached. Moving on to the next part of the code.")

        current_attempt += 1


def main():
    login_twitter()
    post()
    find_posts()
    time.sleep(33333)


main()
# title="Sign in with Google Dialog"
