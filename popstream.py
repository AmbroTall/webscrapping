#!/usr/bin/env python3
import datetime
import undetected_chromedriver as uc
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait

import time
import os
from database import get_data
import json
import sqlite3

options = uc.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode if needed
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
website = 'https://app.propstream.com/'
# path = '/home/ambrose/Documents/chromedriver'
driver = uc.Chrome(options=options)
driver.implicitly_wait(10)
driver.execute_script("window.open('https://www.truthfinder.com/login');")
web_email = "cashpro@cashprohomebuyers.com"
web_password = "Tech6491@@"

truth_email = "cashpro@cashprohomebuyers.com"
truth_pwd = "tech6491"

def log(msg):
    print(f"LOG: {msg}")
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    with open(f"logs/{today}.txt", "a+") as log_file:
        log_file.write(f"{time} : {msg}\n")


def start_page():
    driver.get(website)
    switch_to_popstream = switch_tabs_webmail(0)
    driver.maximize_window()
    switch_to_truthfinder = switch_tabs_webmail(1)
    window_handles = driver.window_handles
    login_truthfinder = login_to_truthfinder(truth_email, truth_pwd)
    verification = verification_by_email()
    time.sleep(2)
    driver.execute_script("window.open('https://client.jewelercart.com:2096/');")
    time.sleep(35)
    switch_to_google = switch_tabs_webmail(2)
    login_to_mail = login_to_email(web_email, web_password)
    verify_email = click_mail_to_verify()
    time.sleep(5)
    driver.close()
    close_gmail = switch_tabs_webmail(2)
    time.sleep(3)
    driver.close()
    time.sleep(2)
    switch_to_popstream = switch_tabs_webmail(0)
    login_popstream()


def switch_tabs_webmail(no):
    driver.switch_to.window(driver.window_handles[no])


# def login_to_email(email, password):
# 	email_input = WebDriverWait(driver, 30).until(
# 		EC.element_to_be_clickable(
# 			(By.ID, 'identifierId')
# 		)
# 	)
# 	# email_input = driver.find_element(By.ID, 'identifierId')
# 	email_input.send_keys(email)
# 	next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
# 	next_button.click()
# 	time.sleep(10)  # wait for next page to load
#
# 	# enter password and click sign in button
# 	password_input = driver.find_element(By.XPATH, "//input[@type='password']")
# 	password_input.send_keys(password)
# 	signin_button = driver.find_element(By.XPATH, "//span[text()='Next']")
# 	signin_button.click()
# 	time.sleep(5)  # wait for sign-in to complete
#
# 	conversation_link = driver.find_element(By.XPATH, "(//span[@class='bog'])[1]")
# 	conversation_link.click()
# 	time.sleep(5)  # wait for conversation to load
#
# 	# click the first hyperlink in the conversation
# 	verify_link = driver.find_element(By.XPATH, "//a[text()='VERIFY ACCOUNT']")
# 	verify_link.click()
# 	time.sleep(3)

def verify_human():
    time.sleep(5)
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        input_elements = driver.find_element(By.TAG_NAME, "input")
        input_elements.click()
        time.sleep(5)
        driver.switch_to.default_content()
    except:
        print("No iframe found")

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
def login_to_truthfinder(email, password):
    email_input = try_catch( '//*[@id="login"]/div/div[2]/form/div[1]/input')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[2]/input')
    password_input.send_keys(password)
    time.sleep(3)
    login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[3]/button')
    login_btn.click()


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

    msg = driver.find_element(By.XPATH, '//*[@id]/td[2]/span[4]/a/span')
    msg.click()

    msg_frame = driver.switch_to.frame("messagecontframe")

    verify_account = driver.find_element(By.XPATH,
                                         '//*[@id="message-htmlpart1"]/div/center/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a')
    verify_account.click()


def verification_by_email():
    WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="verification"]/div/div[2]/button'),  # Element filtration
        )
    )
    verification_btn = driver.find_element(By.XPATH, '//*[@id="verification"]/div/div[2]/button')
    verification_btn.click()


def login_popstream():
    # Explicit Wait until username is visible
    driver.refresh()
    email_input = try_catch("//input[@name='username']") # Element filtration

    email_input.send_keys("jewelercart@gmail.com")

    # Explicit Wait until password input is visible
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='password']"),  # Element filtration
        )
    )
    password_input.send_keys("Taqwah79@@")
    login_btn = driver.find_element(By.XPATH, '//*[@id="form-content"]/form/button')
    login_btn.click()


def popstream_information(address):
    switch_tabs_webmail(0)
    driver.refresh()
    time.sleep(2)
    # Performing search
    try:
        login_btn = driver.find_element(By.XPATH, '//*[@id="form-content"]/form/button')
        login_btn.click()
    except:
        log("No login button")
    # Performing search
    try:
        pop_up = driver.find_element(By.XPATH, '//*[@id="alert"]/div/div/div/div/div/div/div[2]/button/span')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                              pop_up)
        pop_up.click()
        log("pop up closed")
    except:
        close_details = driver.find_element(By.XPATH, '//*[@id="propertyDetail"]/div/div/div[1]/button')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                              close_details)
        close_details.click()
        log('Close details')
    # Search Bar
    wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    search_bar = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'input')))
    search_bar.click()
    search_bar.clear()
    search_bar.send_keys(address)
    time.sleep(3)
    # Selecting the first choice after searching for an address
    select_address = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "react-autowhatever-1--item-0"))
    )
    select_address.click()
    # Getting the details
    details_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="root"]/div/div[2]/div/div/div[3]/div[1]/div/section/div[2]/div/div/div/div/div[1]/div[3]/a'))
    )
    details_btn.click()
    final_data = scrape_user_data(address)
    return final_data


def scrape_user_data(address):
    scrapped_data = {}
    scrapped_data['name'] = address
    time.sleep(1)
    fields = ["beds", "baths", "sqFt", "lot_size", "year_built", "APN", "property_type", "status", "distressed",
              "short_scale", "HOA_COA", "owner_type", "owner_status", "occupancy",
              "length_of_ownership", "purchase_method", "county", "estimated_value", "last_year ", "properties",
              "avg_sale_price", "days_on_market", "open_mortgages", "est_mortgage_balance",
              "involuntary_liens", "total_involuntary_amt", "public_record", "MLS", "est_equity", "linked_properties",
              "monthly_rent", "gross_yield", "owner_1_name", "owner_2_name", "mailing_address",
              "mailing_care_of_name", "total_rooms", "bedrooms", "total_bathrooms", "full_bathrooms",
              "partial_bathrooms", "number_of_bathroom_fixtures", "number_of_fireplaces",
              "air_conditioning_type",
              "heating_type", "heating_fuel_type", "garage_type", "basement_type", "building_class_type",
              "building_condition", "construction_type", "exterior_wall_type", "roof_type",
              "roof_cover_type",
              "sewer_type", "water_source", "number_of_stories", "number_of_residential_units", "building_area",
              "living_area", "basement_area", "garage_area", "alternate_APN", "property_class",
              "zoning",
              "county_land_use_code", "census_tract", "lot_width", "lot_size", "lot_area", "school_district", "block",
              "municipality", "lot_number", "district", "subdivision_name",
              "legal_description",
              "total_assessed_value", "assessed_land_value", "assessed_improvement_value", "assessment_year",
              "tax_year", "market_total_value", "market_land_value", "market_improvement_value",
              "property_tax", "HOA_type", "HOA_fee", "HOA_fee_frequency", "sale_date", "sale_amount", "document_type",
              "recording_date", "book", "page", "buyer_1_name", "buyer_2_name",
              "seller_1_name",
              "buyer_mailing_address", "amount", "lender_name", "term", "maturity_date", ]

    element_ids = [
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[1]/span',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/div[2]/span',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[3]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[4]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[5]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[3]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[4]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[6]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[9]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[10]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[10]/div[2]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[3]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[3]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[3]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[4]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[3]/div[1]',
        '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[4]/div[1]',
        '//*[@id="react-tabs-21"]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div',
        '//*[@id="react-tabs-17"]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div']

    for i, element_id in enumerate(element_ids):
        try:
            data = driver.find_element(By.XPATH, element_id).text.strip()
        except:
            data = ''
        scrapped_data[fields[i]] = data

    scrapped_data['url'] = driver.current_url

    # TruthFinder Code
    switch_to_truthfinder = switch_tabs_webmail(1)
    street = address.split(",")[0]
    city = address.split(",")[1]
    zip = address.split(",")[-1].split(" ")[-1]
    click_address_search(street, city, zip)
    time.sleep(2)
    try:
        click_property_report()
    except:
        driver.refresh()
        click_property_report()

    phone_nos, emails, truthfinder_url = click_residents()
    scrapped_data['phone_numbers'] = f"{phone_nos}"
    scrapped_data['email_contacts'] = f"{emails}"
    scrapped_data['truthfinder_url'] = truthfinder_url
    time.sleep(2)
    return_to_dashboard()
    switch_tabs_webmail(0)
    time.sleep(2)
    return scrapped_data


# TruthFinder Code. Enter Search Address
def click_address_search(street, city, zip):
    time.sleep(3)
    driver.refresh()
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Address']"),
            )
        )
    except:
        return_to_dashboard()
        time.sleep(2)

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
    zip_address.send_keys(zip)
    time.sleep(1)
    search_btn = driver.find_element(By.XPATH, '//*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[5]/button')
    search_btn.click()
    time.sleep(2)


def click_property_report():
    links = driver.find_elements(By.TAG_NAME, "a")
    for x in links:
        if x.text.lower() == "open report":
            x.click()
    time.sleep(2)


def click_residents():
    links = driver.find_elements(By.CLASS_NAME, "nav-text")
    for x in links:
        if x.text.lower() == "residents":
            x.click()
            break
    residents = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="site-main"]/div/div[4]/div/div[1]/div/div/div/div[1]/a[2]'),
        )
    )
    residents.click()
    time.sleep(2)
    owners = driver.find_elements(By.XPATH, "//div[@class='ui-grid outer-gutter-xx-small residents-subsection-item']")
    for x in owners:
        link = x.find_element(By.TAG_NAME, "a")
        link.click()
        break
    # Pass here the name
    # name = x.find_element(By.TAG_NAME,"p").text
    # if len(name.split()) > len(identity.split()):
    #     longer_name = name
    #     shorter_name = identity
    # else:
    #     longer_name = identity
    #     shorter_name = name
    #
    # longer_name = longer_name.lower()
    # shorter_name = shorter_name.lower()
    # if all(name in longer_name for name in shorter_name.split()):
    #     link.click()
    #     break
    # else:
    #     print("The names are different.")
    time.sleep(5)
    contacts = driver.find_elements(By.CLASS_NAME, "nav-text")
    for x in contacts:
        if x.text.lower() == "contact":
            x.click()
            break
    time.sleep(2)
    phone_nos = []
    # Extract all phone numbers
    phone_numbers = driver.find_elements(By.CLASS_NAME, 'phone-subsection-item')
    for x in phone_numbers:
        phone_no = x.find_element(By.CLASS_NAME, "phone-number")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                              phone_no)
        phone_nos.append(phone_no.text)

    emails = []
    # extract all emails
    mails = driver.find_elements(By.XPATH, "//div[@class='ui-div email-subsection-item']")
    for x in mails:
        mail = x.find_element(By.TAG_NAME, "h5")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                              mail)
        emails.append(mail.text)
    truthfinder_url = driver.current_url
    return phone_nos, emails, truthfinder_url


def return_to_dashboard():
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href == "https://www.truthfinder.com/dashboard":
            # Click on the link
            link.click()
            break
    time.sleep(2)

def save_data_to_mysql(data):
    try:
        # Connect to the MySQL database
        conn_mysql = mysql.connector.connect(
            host='168.119.4.62',
            user='helixhel_oldcrawlersusr',
            password='NdSZIAfVZHoA',
            database='helixhel_oldcrawlersdb',
        )
        cursor_mysql = conn_mysql.cursor()

        # Insert data into the MySQL table
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO properties_two ({keys}) VALUES ({placeholders})"
        cursor_mysql.execute(query, values)

        # Commit the changes to MySQL
        conn_mysql.commit()
        conn_mysql.close()
        print("Data saved to MySQL successfully!")
    except mysql.connector.Error as e:
        print("An error occurred while saving data to MySQL:", str(e))


def save_data_to_databases(data):
    try:
        # Connect to the SQLite database or create a new one if it doesn't exist
        conn_sqlite = sqlite3.connect('property_data.db')
        cursor_sqlite = conn_sqlite.cursor()

        # Insert data into the SQLite table
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO properties_two ({keys}) VALUES ({placeholders})"
        cursor_sqlite.execute(query, values)

        # Commit the changes to SQLite and MySQL
        conn_sqlite.commit()
        conn_sqlite.close()
        save_data_to_mysql(data)
        print("Data saved to both SQLite successfully!")
    except (sqlite3.Error, mysql.connector.Error) as e:
        print("An error occurred while saving data:", str(e))

def fetch_all_ids_from_sqlite():
    try:
        # Connect to the SQLite database or create a new one if it doesn't exist
        conn = sqlite3.connect("property_data.db")
        cursor = conn.cursor()

        # Fetch all the IDs from the table
        select_ids_query = f"SELECT ga_id FROM properties_two"
        cursor.execute(select_ids_query)
        rows = cursor.fetchall()

        # Extract the IDs from the fetched rows
        ids = [row[0] for row in rows]
        # Close the database connection
        conn.close()
        return ids
    except sqlite3.Error as e:
        print("An error occurred while fetching IDs from SQLite:", str(e))
        return []


def main():
    gapubs_data = get_data()
    print(len(gapubs_data))
    exisiting_ids = fetch_all_ids_from_sqlite()
    print(exisiting_ids)
    # step 1 Login
    start_page()
    time.sleep(2)
    db_data_holder = []
    count = 0
    for x in reversed(gapubs_data):
        address = json.loads(x)
        if address["Street"] != "" and address["Zip_Code"] != "" and address['Id'] not in exisiting_ids:
            print("Record no", count)
            address_db = f'{address["Street"]}, {address["City"]}, GA {address["Zip_Code"]}'
            log(address_db)
            try:
                # step 2 Propstream information (TruthFinder Code)
                db_data = popstream_information(address_db)
                # Retrieve the data from the page and store it
                db_data['ga_id'] = address['Id']
                db_data_holder.append(db_data)
                print(db_data_holder)
                save_data_to_databases(db_data)
                time.sleep(2)  # Wait for the information to load
                count += 1
                continue
            except Exception as e:
                switch_tabs_webmail(0)
                count += 1
                driver.refresh()
                print(e)
                continue
    return db_data_holder


print(main())

# //*[@id="dashboard"]/div[1]/div/div/div/div/form/div/div[1]/div/div
