import pickle
import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

import os

# Current Directory
current_directory = os.getcwd()

def init_driver():
    drivers_path = os.path.join(current_directory, 'drivers')
    firefox_browse = False
    if firefox_browse:
        path_to_driver = os.path.join(drivers_path, "geckodriver.exe")
        browser = webdriver.Firefox(executable_path=path_to_driver)
    else:
        # path_to_driver = os.path.join(drivers_path, "chromedriver.exe")
        # browser = webdriver.Chrome(executable_path=path_to_driver)
        browser = uc.Chrome()

    browser.maximize_window()
    browser.implicitly_wait(30)

    return browser

def verify_human():
    time.sleep(15)
    try:
        iframe = driver.find_element(By.TAG_NAME,"iframe")
        print(len(driver.find_elements(By.TAG_NAME,"iframe")))
        driver.switch_to.frame(iframe)
        # time.sleep(120)

        input_elements = driver.find_element(By.CLASS_NAME, "mark")
        input_elements.click()
        time.sleep(5)
        driver.switch_to.default_content()
    except NoSuchElementException:
        print("No iframe found")
def login_to_truthfinder(email, password):
    time.sleep(120)
    email_input = try_catch('//*[@id="login"]/div/div[2]/form/div[1]/input')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[2]/input')
    password_input.send_keys(password)
    time.sleep(3)
    login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[3]/button')
    login_btn.click()
# def login_to_truthfinder(email, password):
#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable(
#             (By.XPATH, '//*[@id="login"]/div/div[2]/form/div[1]/input'),  # Element filtration
#         )
#     )
#
#     email_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[1]/input')
#     email_input.send_keys(email)
#
#     password_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[2]/input')
#     password_input.send_keys(password)
#
#     login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[3]/button')
#     login_btn.click()

def open_webmail():
    print("Opening webmail...")
    driver.execute_script("window.open('http://client1.jewelercart.com:2096/');")
    driver.switch_to.window(driver.window_handles[0])

def verification_by_email():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="verification"]/div/div[2]/button'),  # Element filtration
            )
    )
    verification_btn = driver.find_element(By.XPATH, '//*[@id="verification"]/div/div[2]/button')
    verification_btn.click()
def try_catch(xpath):
    max_attempts = 5
    current_attempt = 1
    while current_attempt <= max_attempts:
        try:
            element = driver.find_element(By.XPATH, f'{xpath}')
            print("located")
            return element
        except Exception as e:
            print(f"Attempt {current_attempt} failed with error: {e}")
            if current_attempt < max_attempts:
                # driver.refresh()
                print("Retrying...")
            else:
                print("Max attempts reached. Moving on to the next part of the code.")

        current_attempt += 1

def switch_tabs_webmail():
    driver.switch_to.window(driver.window_handles[1])
    print("this is my current url", driver.current_url)
# def login_to_email(email, password):  #Gmail
#     email_input = driver.find_element(By.ID, 'identifierId')
#     email_input.send_keys(email)
#     next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
#     next_button.click()
#     time.sleep(5)  # wait for next page to load
#
#     # enter password and click sign in button
#     password_input = driver.find_element(By.XPATH, "//input[@type='password']")
#     password_input.send_keys(password)
#     signin_button = driver.find_element(By.XPATH, "//span[text()='Next']")
#     signin_button.click()
#     time.sleep(5)  # wait for sign-in to complete
#
#     conversation_link = driver.find_element(By.XPATH, "(//span[@class='bog'])[1]")
#     conversation_link.click()
#     time.sleep(5)  # wait for conversation to load
#
#     # click the first hyperlink in the conversation
#     verify_link = driver.find_element(By.XPATH, "//a[text()='VERIFY ACCOUNT']")
#     verify_link.click()
#     time.sleep(2)

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
    WebDriverWait(driver, 30).until(
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

    msg = driver.find_element(By.XPATH, '//*[@id]/td[2]/span[4]/a/span')
    msg.click()

    msg_frame = driver.switch_to.frame("messagecontframe")

    verify_account = driver.find_element(By.XPATH, '//*[@id="message-htmlpart1"]/div/center/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a')
    verify_account.click()

def dashboard():
    time.sleep(3)
    driver.close()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    driver.refresh()

def click_address_search():
    time.sleep(3)
    driver.refresh()
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Address']"),
            )
        )
    except:
        driver.refresh()
        time.sleep(2)

    street = '3440 Freedom Lane'
    city = 'Dalton'
    zip_add = '30721'
    address_button = driver.find_element(By.XPATH, "//span[text()='Address']")
    address_button.click()

    street_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[1]/input'),
            )
        )
    street_address.send_keys(street)
    time.sleep(1)
    city_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[2]/input'),
            )
        )
    city_address.send_keys(city)
    time.sleep(1)
    state = driver.find_element(By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[3]/div/select')
    dropdown = Select(state)
    dropdown.select_by_visible_text('Georgia')
    time.sleep(1)
    zip_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[4]/input'),
            )
        )
    zip_address.send_keys(zip_add)
    time.sleep(1)
    search_btn = driver.find_element(By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[5]/button')
    search_btn.click()
    time.sleep(2)

def click_property_report():
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
    except:
        print("Hello this is iframe 1")
    links = driver.find_elements(By.TAG_NAME, "a")
    for x in links:
        if x.text == "OPEN REPORT":
            print("I found it")
            x.click()
    # driver.switch_to.default_content()
    time.sleep(2)

# passs the name to get the owner reports of the property
def click_residents():
    identity = "ROBERTS JOSEPH"
    links = driver.find_elements(By.CLASS_NAME, "nav-text")
    for x in links:
        print(x.text, "\n")
        if x.text == "RESIDENTS":
            x.click()
        # print(x.text, '\n')
    residents = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="site-main"]/div/div[4]/div/div[1]/div/div/div/div[1]/a[2]'),
        )
    )
    residents.click()
    time.sleep(2)
    owners = driver.find_elements(By.XPATH, "//div[@class='ui-grid outer-gutter-xx-small residents-subsection-item']")
    for x in owners:
        name = x.find_element(By.TAG_NAME,"p").text
        print(name)
        link = x.find_element(By.TAG_NAME,"a")
        print(link.text)
        # Pass here the name
        if len(name.split()) > len(identity.split()):
            longer_name = name
            shorter_name = identity
        else:
            longer_name = identity
            shorter_name = name

        longer_name = longer_name.lower()
        shorter_name = shorter_name.lower()
        if all(name in longer_name for name in shorter_name.split()):
            link.click()
            break
        else:
            print(longer_name)
            print(shorter_name)
            print("The names are different.")
    time.sleep(5)
    driver.switch_to.default_content()

    contacts = driver.find_elements(By.CLASS_NAME, "nav-text")
    # print(contacts)
    for x in contacts:
        print(x.text, "\n")
        if x.text == "CONTACT":
            x.click()
            break
    time.sleep(5)
    phone_nos = []
    # Extract all phone numbers
    phone_numbers = driver.find_elements(By.CLASS_NAME, 'phone-subsection-item')
    for x in phone_numbers:
        phone_no = x.find_element(By.CLASS_NAME, "phone-number")
        print(phone_no.text)
        phone_nos.append(phone_no.text)

    print(phone_nos)
    emails = []
    # extract all emails
    mails = driver.find_elements(By.XPATH, "//div[@class='ui-div email-subsection-item']")
    for x in mails:
        mail = x.find_element(By.TAG_NAME, "h5")
        print(mail.text)
        emails.append(mail.text)

if __name__ == '__main__':
    print("--Starts--")
    truth_email = "cashhomebuyersincusa@gmail.com"
    truth_password = "tech6491"

    web_email = "cashpro@cashprohomebuyers.com"
    web_password = "l.ZtLZX}e_vT"

    link = "https://www.truthfinder.com/login"

    print("Initializing webdriver...")
    driver = init_driver()
    print('Loading: "{}"'.format(link))
    open_webmail()
    driver.get(
        'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    google_cookies = pickle.load(
        open("/home/ambrose/PycharmProjects/WebScraping/webscrapping/twitterBots/bot/google_cookies.pkl", "rb"))

    for cookie in google_cookies:
        cookie['domain'] = ".google.com"
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            pass

    driver.get(link)
    time.sleep(10)
    # verify_human()
    print('Connection Security ByPassed...')
    login = login_to_truthfinder(truth_email, truth_password)
    verification = verification_by_email()
    open_webmail = switch_tabs_webmail()
    time.sleep(35)
    login_to_mail = login_to_email(web_email, web_password)
    dashboard = dashboard()
    click_address_search()
    click_property_report()
    click_residents()
    time.sleep(9999)
    print("\n--Finish--")

