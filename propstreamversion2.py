import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select  # Drop down menu selection (line-17)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import json
from database import get_data
import json

options = ChromeOptions()
propstream = 'https://app.propstream.com/'
truthfinder = 'https://www.truthfinder.com/login'
# options.add_experimental_option('prefs', {
#     'download.default_directory': '/home/ambrose/PycharmProjects/WebScraping/pdfs',
#     'download.prompt_for_download': False,
#     'download.directory_upgrade': True,
#     'plugins.always_open_pdf_externally': True
# })
path = '/home/ambrose/Documents/chromedriver'
driver = uc.Chrome(use_subprocess=True)
driver.implicitly_wait(10)
# driver.execute_script("window.open('https://www.truthfinder.com/login');")


def log(msg):
    print(f"LOG: {msg}")
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    with open(f"logs/{today}.txt", "a+") as log_file:
        log_file.write(f"{time} : {msg}\n")

def switch_tabs_webmail(no):
    driver.switch_to.window(driver.window_handles[no])

def popstream_start():
    driver.get(propstream)
    driver.maximize_window()
    login_popstream()

def truthfinder_start():
    driver.get('https://www.truthfinder.com/login')
    driver.maximize_window()
    login_truthfinder = login_to_truthfinder("cashhomebuyersincusa@gmail.com", "tech6491")
    verification = verification_by_email()
    # time.sleep(2)
    driver.execute_script("window.open('https://www.gmail.com');")
    time.sleep(35)
    switch_to_google = switch_tabs_webmail(1)
    login_to_gmail = login_to_email("cashhomebuyersincusa@gmail.com", "Taqwah79@@")
    time.sleep(2)
    driver.close()
    close_gmail = switch_tabs_webmail(2)
    time.sleep(2)
    driver.close()
    time.sleep(2)
    # switch_to_popstream = switch_tabs_webmail(0)
    # driver.close()

def login_to_email(email, password):
    email_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.ID, 'identifierId')
        )
    )
    # email_input = driver.find_element(By.ID, 'identifierId')
    email_input.send_keys(email)
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()
    time.sleep(5)  # wait for next page to load

    # enter password and click sign in button
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)
    signin_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    signin_button.click()
    time.sleep(5)  # wait for sign-in to complete

    conversation_link = driver.find_element(By.XPATH, "(//span[@class='bog'])[1]")
    conversation_link.click()
    time.sleep(5)  # wait for conversation to load

    # click the first hyperlink in the conversation
    verify_link = driver.find_element(By.XPATH, "//a[text()='VERIFY ACCOUNT']")
    verify_link.click()
    time.sleep(3)

def login_to_truthfinder(email, password):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="login"]/div/div[2]/form/div[1]/input'),  # Element filtration
            )
        )
        print("hello")
    except:
        driver.refresh()

    email_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[1]/input')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[2]/input')
    password_input.send_keys(password)
    time.sleep(2)
    login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[3]/button')
    login_btn.click()

def verification_by_email():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="verification"]/div/div[2]/button'),  # Element filtration
            )
    )
    verification_btn = driver.find_element(By.XPATH, '//*[@id="verification"]/div/div[2]/button')
    verification_btn.click()

def login_popstream():
    # driver.switch_to.window(driver.window_handles[0])
    # Explicit Wait until username is visible
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='username']"),  # Element filtration
        )
    )
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
    # Open a new tab
    driver.refresh()
    time.sleep(2)
    if len(driver.window_handles) > 1:
        # Switch to the last window handle
        driver.switch_to.window(driver.window_handles[-1])

        # Iterate over window handles starting from the second to last window
        for handle in driver.window_handles[:-1]:
            # Switch to the window handle
            driver.switch_to.window(handle)
            # Close the window
            driver.close()

    # Switch back to the last window handle
    driver.switch_to.window(driver.window_handles[-1])

    try:
        login_btn = driver.find_element(By.XPATH, '//*[@id="form-content"]/form/button')
        login_btn.click()
    except:
        log("No login button")

    # Performing search
    try:
        pop_up = driver.find_element(By.XPATH, '//*[@id="alert"]/div/div/div/div/div/div/div[2]/button/span')
        pop_up.click()
        log("pop up closed")
    except:
        close_details = driver.find_element(By.XPATH, '//*[@id="propertyDetail"]/div/div/div[1]/button')
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
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[3]/div[1]/div/section/div[2]/div/div/div/div/div[1]/div[3]/a'))
    )
    details_btn.click()
    final_data = scrape_user_data()
    return final_data
def scrape_user_data():
    scrapped_data = {}
    time.sleep(1)
    fields = ["name", "beds", "baths", "sqFt", "lot_size", "year_built", "APN", "property_type", "status", "distressed", "short_scale", "HOA_COA", "owner_type", "owner_status", "occupancy",
              "length_of_ownership", "purchase_method", "county", "estimated_value", "last_year ", "properties", "avg_sale_price", "days_on_market", "open_mortgages", "est_mortgage_balance",
              "involuntary_liens", "total_involuntary_amt", "public_record", "MLS", "est_equity", "linked_properties", "monthly_rent", "gross_yield", "owner_1_name", "owner_2_name", "mailing_address",
              "mailing_care_of_name", "total_rooms", "bedrooms", "total_bathrooms", "full_bathrooms", "partial_bathrooms", "number_of_bathroom_fixtures", "number_of_fireplaces",
              "air_conditioning_type",
              "heating_type", "heating_fuel_type", "garage_type", "basement_type", "building_class_type", "building_condition", "construction_type", "exterior_wall_type", "roof_type",
              "roof_cover_type",
              "sewer_type", "water_source", "number_of_stories", "number_of_residential_units", "building_area", "living_area", "basement_area", "garage_area", "alternate_APN", "property_class",
              "zoning",
              "county_land_use_code", "census_tract", "lot_width", "lot_size", "lot_area", "school_district", "block", "municipality", "lot_number", "district", "subdivision_name",
              "legal_description",
              "total_assessed_value", "assessed_land_value", "assessed_improvement_value", "assessment_year", "tax_year", "market_total_value", "market_land_value", "market_improvement_value",
              "property_tax", "HOA_type", "HOA_fee", "HOA_fee_frequency", "sale_date", "sale_amount", "document_type", "recording_date", "book", "page", "buyer_1_name", "buyer_2_name",
              "seller_1_name",
              "buyer_mailing_address", "amount", "lender_name", "term", "maturity_date", ]

    element_ids = ['//*[@id="propertyDetail"]/div/div/div[1]/div/div/div[1]',
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
                         '//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[10]/div[2]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[3]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div[2]/div[3]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[3]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[1]/div/div/div/div/div/div[2]/div[4]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[1]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div[2]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[3]/div[1]','//*[@id="propertyDetail"]/div/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[4]/div[1]','//*[@id="react-tabs-1"]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]','//*[@id="react-tabs-17"]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div']

    for i, element_id in enumerate(element_ids):
        try:
            data = driver.find_element(By.XPATH, element_id).text.strip()
        except:
            data = ''
        scrapped_data[fields[i]] = data

    # download_pdf = driver.find_element(By.XPATH,'//*[@id="propertyDetail"]/div/div/div[1]/div/div/div[2]/button[1]')
    # download_pdf.click()
    # download_path = '/home/ambrose/PycharmProjects/WebScraping/pdfs'
    # time.sleep(6)

    # filename = max([download_path + "/" + f for f in os.listdir(download_path)], key=os.path.getctime)
    # scrapped_data['pdf_link'] = filename
    scrapped_data['propstream_url'] = driver.current_url

    return scrapped_data

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

def click_residents(identity=None):
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
    if identity != None:
        for x in owners:
            name = x.find_element(By.TAG_NAME,"p").text
            link = x.find_element(By.TAG_NAME,"a")
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
                print("The names are different.")
    else:
        for x in owners:
            link = x.find_element(By.TAG_NAME,"a")
            link.click()
            break

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
        phone_nos.append(phone_no.text)

    emails = []
    # extract all emails
    mails = driver.find_elements(By.XPATH, "//div[@class='ui-div email-subsection-item']")
    for x in mails:
        mail = x.find_element(By.TAG_NAME, "h5")
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

def propstream_info():
    gapubs_data = get_data()
    print( gapubs_data)
    # step 1 Login
    popstream_start()

    time.sleep(2)

    propstream_data = []
    count = 0
    for x in gapubs_data:
        if count == 20:
            break

        address = json.loads(x)
        if address["Street"] != "" and address["Zip_Code"] != "":
            address_db = f'{address["Street"]}, {address["City"]}, GA {address["Zip_Code"]}'
            log(address_db)
            try:

                # Step 2: Propstream information
                x = popstream_information(address_db)
                # driver.execute_script("window.open('https://app.propstream.com/');")

                time.sleep(2)  # Wait for the information to load
                # Retrieve the data from the page and store it
                propstream_data.append(x)
                count += 1
                continue
            except Exception as e:
                driver.refresh()
                print("Taller")
                continue
    return propstream_data
def truthfinder_info():
    # data = propstream_info()
    final_data = []
    data = [{'name': '3322 Waggoner Pl Rex, GA 30273', 'beds': '4', 'baths': '3', 'sqFt': '1,763', 'lot_size': '562', 'year_built': '2004', 'APN': '12-152C- E-001', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '1 Year', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$294,578', 'last_year ': '$292,141', 'properties': '14', 'avg_sale_price': '$559,134', 'days_on_market': '42', 'open_mortgages': '42', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': 'N/A\n06/27/2022', 'MLS': 'N/A', 'est_equity': '$294,578',
          'linked_properties': '4', 'monthly_rent': '$1,657', 'gross_yield': '6.75%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740083360'},
         {'name': '521 Villa Esta Cir Macon, GA 31206', 'beds': '4', 'baths': '3', 'sqFt': '1,620', 'lot_size': '', 'year_built': '1939', 'APN': 'Q093-0064', 'property_type': 'Single Family Residential', 'status': 'On Market', 'distressed': 'No', 'short_scale': 'Yes', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '11 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$35,227', 'last_year ': '$36,056', 'properties': '16', 'avg_sale_price': '$75,969', 'days_on_market': '98', 'open_mortgages': '98', 'est_mortgage_balance': '$154,910', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$165,000\n07/21/2022', 'MLS': 'N/A\n07/2022', 'est_equity': '$-119,683',
          'linked_properties': '0', 'monthly_rent': '$1,034', 'gross_yield': 'N/A', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739453162'},
         {'name': '542 Valley Hill Rd SE Riverdale, GA 30274', 'beds': '4', 'baths': '3', 'sqFt': '2,508', 'lot_size': '55,757', 'year_built': '1961', 'APN': '13-179D- D-026', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Trust', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '19 Years 8 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$292,409', 'last_year ': '$284,937', 'properties': '6', 'avg_sale_price': '$238,147', 'days_on_market': '43', 'open_mortgages': '43', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$129,000\n10/03/2003', 'MLS': 'N/A',
          'est_equity': '$292,409', 'linked_properties': '1', 'monthly_rent': '$1,427', 'gross_yield': '5.86%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740098404'},
         {'name': '6486 Bobolink Ct Rex, GA 30273', 'beds': '3', 'baths': '2', 'sqFt': '1,618', 'lot_size': '12,160', 'year_built': '1979', 'APN': '12-118D- D-026', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'Pre-Foreclosure', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$254,626', 'last_year ': '$253,897', 'properties': '16', 'avg_sale_price': '$1,603,650', 'days_on_market': '59', 'open_mortgages': '59', 'est_mortgage_balance': '$54,190', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': 'N/A', 'MLS': 'N/A', 'est_equity': '$200,436',
          'linked_properties': '2', 'monthly_rent': '$1,297', 'gross_yield': '6.11%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740079515'},
         {'name': '', 'beds': '', 'baths': '2', 'sqFt': '1,360', 'lot_size': '842', 'year_built': '1997', 'APN': '13-238B- A-044', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'Yes', 'HOA_COA': 'No', 'owner_type': 'Corporate', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '1 Year 5 Months', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': '$257,559', 'last_year ': '$233,306', 'properties': '15', 'avg_sale_price': '$531,568', 'days_on_market': '62', 'open_mortgages': '62', 'est_mortgage_balance': '$134,726,890', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$231,492\n12/30/2021', 'MLS': '$219,670/est\n10/2021', 'est_equity': '$-134,469,331',
          'linked_properties': '49', 'monthly_rent': '$1,273', 'gross_yield': '5.93%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740100521'},
         {'name': '188 3rd St Macon, GA 31201', 'beds': '', 'baths': '', 'sqFt': '16,198', 'lot_size': '43,560', 'year_built': '1948', 'APN': 'R073-0110', 'property_type': 'Governmental/Public Use (General)', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Corporate', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '10 Years', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': 'N/A', 'last_year ': 'N/A', 'properties': '1', 'avg_sale_price': '$350,000', 'days_on_market': 'N/A', 'open_mortgages': 'N/A', 'est_mortgage_balance': 'N/A', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$367,500\n06/13/2013', 'MLS': 'N/A', 'est_equity': 'N/A', 'linked_properties': '463',
          'monthly_rent': 'N/A', 'gross_yield': 'N/A', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739455947'},
         {'name': '2918 Houston Ave Macon, GA 31206', 'beds': '1', 'baths': '1', 'sqFt': '640', 'lot_size': '14,375', 'year_built': '1940', 'APN': 'P092-0265', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'Yes', 'owner_type': 'Individual', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Vacant', 'length_of_ownership': '2 Years', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': '$18,620', 'last_year ': '$45,048', 'properties': '4', 'avg_sale_price': '$8,487', 'days_on_market': '3', 'open_mortgages': '3', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$9,033\n06/16/2021', 'MLS': 'N/A', 'est_equity': '$18,620', 'linked_properties': '2',
          'monthly_rent': '$985', 'gross_yield': '63.48%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739452558'},
         {'name': '3952 Singletree Pl Norcross, GA 30093', 'beds': '3', 'baths': '2.5', 'sqFt': '2,490', 'lot_size': '13,068', 'year_built': '1986', 'APN': '6-183 -288', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$386,879', 'last_year ': '$376,672', 'properties': '5', 'avg_sale_price': '$298,200', 'days_on_market': '54', 'open_mortgages': '54', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': 'N/A', 'MLS': 'N/A', 'est_equity': '$386,879', 'linked_properties': '0',
          'monthly_rent': '$1,611', 'gross_yield': '5%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1741921269'},
         {'name': '1771 Poplar St SE Conyers, GA 30013', 'beds': '3', 'baths': '2', 'sqFt': '2,009', 'lot_size': '20,909', 'year_built': '1971', 'APN': '075-A-01-0141', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Mixed', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '1 Year 5 Months', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': '$296,892', 'last_year ': '$278,337', 'properties': '13', 'avg_sale_price': '$231,764', 'days_on_market': '57', 'open_mortgages': '57', 'est_mortgage_balance': '$64,263', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$86,700\n01/07/2022', 'MLS': 'N/A', 'est_equity': '$232,629',
          'linked_properties': '0', 'monthly_rent': '$1,650', 'gross_yield': '6.67%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1743231259'},
         {'name': '', 'beds': '', 'baths': '', 'sqFt': '', 'lot_size': '', 'year_built': '', 'APN': '18018301220', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'Yes', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '17 Years 2 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$456,988', 'last_year ': '$475,504', 'properties': '9', 'avg_sale_price': '$414,511', 'days_on_market': '103', 'open_mortgages': '103', 'est_mortgage_balance': '$0', 'involuntary_liens': '4', 'total_involuntary_amt': '$21,573.48', 'public_record': '$263,700\n03/31/2006', 'MLS': 'N/A', 'est_equity': '$456,988', 'linked_properties': '0',
          'monthly_rent': '$2,353', 'gross_yield': '6.18%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740286520'},
         {'name': '1523 Wooten Rd Augusta, GA 30904', 'beds': '3', 'baths': '1.5', 'sqFt': '1,062', 'lot_size': '7,405', 'year_built': '1926', 'APN': '072-1-067-00-0', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Vacant', 'length_of_ownership': '2 Years 1 Month', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': '$20,227', 'last_year ': '$66,089', 'properties': '21', 'avg_sale_price': '$26,100', 'days_on_market': '95', 'open_mortgages': '95', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$10,500\n05/28/2021', 'MLS': 'N/A', 'est_equity': '$20,227',
          'linked_properties': '10', 'monthly_rent': '$904', 'gross_yield': '53.63%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1743174537'},
         {'name': '111 Summer St Adairsville, GA 30103', 'beds': '3', 'baths': '1', 'sqFt': '2,482', 'lot_size': '19,602', 'year_built': '1890', 'APN': 'A005-0005-006', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Corporate', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Vacant', 'length_of_ownership': '7 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$375,891', 'last_year ': '$266,997', 'properties': '6', 'avg_sale_price': '$260,833', 'days_on_market': '49', 'open_mortgages': '49', 'est_mortgage_balance': '$128,870', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$153,716\n11/17/2022', 'MLS': 'N/A', 'est_equity': '$247,021',
          'linked_properties': '4', 'monthly_rent': '$1,478', 'gross_yield': '4.72%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739362328'},
         {'name': '119 Bay Court Dr Stockbridge, GA 30281', 'beds': '3', 'baths': '2', 'sqFt': '1,318', 'lot_size': '9,536', 'year_built': '1998', 'APN': '050A01005000', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '17 Years', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$257,675', 'last_year ': '$236,480', 'properties': '16', 'avg_sale_price': '$265,790', 'days_on_market': '58', 'open_mortgages': '58', 'est_mortgage_balance': '$94,867', 'involuntary_liens': '1', 'total_involuntary_amt': '$113.60', 'public_record': '$135,000\n05/15/2006', 'MLS': 'N/A',
          'est_equity': '$162,808', 'linked_properties': '0', 'monthly_rent': '$1,537', 'gross_yield': '7.16%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1742248777'},
         {'name': '403 Rosemary Ct Statesboro, GA 30458', 'beds': '3', 'baths': '2', 'sqFt': '1,641', 'lot_size': '38,333', 'year_built': '1986', 'APN': 'MS47 -054-000', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '2 Years', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$237,790', 'last_year ': '$196,610', 'properties': '6', 'avg_sale_price': '$579,478', 'days_on_market': '143', 'open_mortgages': '143', 'est_mortgage_balance': '$99,712', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$193,500\n06/18/2021', 'MLS': '$255,260/est\n05/2023',
          'est_equity': '$138,078', 'linked_properties': '0', 'monthly_rent': '$1,251', 'gross_yield': '6.32%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739553847'},
         {'name': '949 Ponce De Leon Cir N Macon, GA 31206', 'beds': '3', 'baths': '1.5', 'sqFt': '1,048', 'lot_size': '9,583', 'year_built': '1971', 'APN': 'P091-0026', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '2 Years', 'purchase_method': 'Cash', 'county': 'Cash', 'estimated_value': '$34,156', 'last_year ': '$52,230', 'properties': '32', 'avg_sale_price': '$33,225', 'days_on_market': '39', 'open_mortgages': '39', 'est_mortgage_balance': '$0', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$10,000\n06/16/2021', 'MLS': 'N/A', 'est_equity': '$34,156',
          'linked_properties': '13', 'monthly_rent': '$780', 'gross_yield': '27.4%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739453192'},
         {'name': '20 Julian Farm Rd Dawsonville, GA 30534', 'beds': '2', 'baths': '1', 'sqFt': '900', 'lot_size': '21,780', 'year_built': '1945', 'APN': 'L22 051', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Corporate', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '2 Years', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$234,631', 'last_year ': '$195,570', 'properties': 'N/A', 'avg_sale_price': 'N/A', 'days_on_market': 'N/A', 'open_mortgages': 'N/A', 'est_mortgage_balance': '$125,838', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$175,000\n06/25/2021', 'MLS': '$175,180/est\n06/2021',
          'est_equity': '$108,793', 'linked_properties': '2', 'monthly_rent': '$1,424', 'gross_yield': '7.29%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740581256'},
         {'name': '', 'beds': '', 'baths': '', 'sqFt': '', 'lot_size': '', 'year_built': '', 'APN': '', 'property_type': '', 'status': '', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': '', 'owner_status': '', 'occupancy': 'Occupied', 'length_of_ownership': '', 'purchase_method': '', 'county': '', 'estimated_value': 'N/A', 'last_year ': 'N/A', 'properties': 'N/A', 'avg_sale_price': 'N/A', 'days_on_market': 'N/A', 'open_mortgages': 'N/A', 'est_mortgage_balance': 'N/A', 'involuntary_liens': 'N/A', 'total_involuntary_amt': 'N/A', 'public_record': 'N/A', 'MLS': 'N/A', 'est_equity': 'N/A', 'linked_properties': '0', 'monthly_rent': 'N/A', 'gross_yield': 'N/A', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1739404748'},
         {'name': '3070 Pierce Rd Gainesville, GA 30507', 'beds': '3', 'baths': '2', 'sqFt': '1,782', 'lot_size': '115,870', 'year_built': '1999', 'APN': '15-021 -000-169', 'property_type': 'Mobile home', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'No', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$108,403', 'last_year ': '$108,477', 'properties': '1', 'avg_sale_price': '$108,000', 'days_on_market': '3', 'open_mortgages': '3', 'est_mortgage_balance': '$50,162', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': 'N/A', 'MLS': 'N/A', 'est_equity': '$58,241', 'linked_properties': '0',
          'monthly_rent': '$1,444', 'gross_yield': '15.98%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1742128611'},
         {'name': '7101 Secret Rose Douglasville, GA 30134', 'beds': '5', 'baths': '3.5', 'sqFt': '3,120', 'lot_size': '14,063', 'year_built': '2005', 'APN': '0192-02-5- -00126', 'property_type': 'Single Family Residential', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'No', 'HOA_COA': 'Yes', 'owner_type': 'Individual', 'owner_status': 'Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '17 Years 10 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$429,556', 'last_year ': '$416,898', 'properties': '3', 'avg_sale_price': '$372,000', 'days_on_market': '50', 'open_mortgages': '50', 'est_mortgage_balance': '$191,640', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$270,400\n07/20/2005', 'MLS': 'N/A',
          'est_equity': '$237,916', 'linked_properties': '0', 'monthly_rent': '$1,841', 'gross_yield': '5.14%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1740944841'},
         {'name': '1066 Wedgewood Ln Tucker, GA 30084', 'beds': '3', 'baths': '2', 'sqFt': '1,220', 'lot_size': '436', 'year_built': '1985', 'APN': '6-168A-007', 'property_type': 'Townhouse (Residential)', 'status': 'Off Market', 'distressed': 'No', 'short_scale': 'Yes', 'HOA_COA': 'Yes', 'owner_type': 'Individual', 'owner_status': 'Non-Owner Occupied', 'occupancy': 'Occupied', 'length_of_ownership': '9 Months', 'purchase_method': 'Financed', 'county': 'Financed', 'estimated_value': '$216,578', 'last_year ': '$176,228', 'properties': '15', 'avg_sale_price': '$183,060', 'days_on_market': '63', 'open_mortgages': '63', 'est_mortgage_balance': '$226,943', 'involuntary_liens': '0', 'total_involuntary_amt': '$0', 'public_record': '$236,000\n09/29/2022', 'MLS': '$236,000/est\n09/2022',
          'est_equity': '$-10,365', 'linked_properties': '7', 'monthly_rent': '$1,900', 'gross_yield': '10.53%', 'owner_1_name': '', 'owner_2_name': '', 'propstream_url': 'https://app.propstream.com/search/1741882798'}]
    print(len(data))
    truthfinder_start()

    for x in data:
        try:
            street = x['name'].split(",")[0]
            city = x['name'].split(",")[1]
            zip = x['name'].split(",")[-1].split(" ")[-1]
            click_address_search(street, city, zip)
            time.sleep(2)
            click_property_report()
            phone_nos, emails, truthfinder_url = click_residents(x['owner_1_name'])
            x['phone_numbers'] = phone_nos
            x['email_contacts'] = emails
            x['truthfinder_url'] = truthfinder_url
            final_data.append(x)
            time.sleep(2)
            return_to_dashboard()
        except:
            return_to_dashboard()
    return final_data

print(truthfinder_info())
