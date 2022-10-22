from selenium import webdriver
from .BookingFilters import BookingFilter
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select
from .Constants import WEBSITE

path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
driver.implicitly_wait(15)
driver.maximize_window()


class Booking:
    def __init__(self):
        pass

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get(WEBSITE)

    def change_currency(self, currency=None):
        currency_btn = driver.find_element(By.XPATH, '//button[@data-modal-aria-label="Select your currency"]')
        currency_btn.click()
        selected_currency = driver.find_element(By.XPATH, f'//a[@data-modal-header-async-url-param="changed_currency=1&selected_currency={currency}&top_currency=1"]')
        selected_currency.click()

    def destination(self, country):
        destination = driver.find_element(By.ID, 'ss')
        destination.send_keys(country)
        destination_value = driver.find_element(By.XPATH, f'//li[@data-label="{country.capitalize()}"]')
        destination_value.click()

    def checkin_checkout(self):
        check_in = driver.find_element(By.XPATH, '//td[@data-date="2022-07-10"]')
        check_in.click()
        check_out = driver.find_element(By.XPATH, '//td[@data-date="2022-07-20"]')
        check_out.click()

    def number_of_people(self, adults=None):
        adults_div = driver.find_element(By.XPATH, '//div[@data-visible="accommodation,flights"]')
        adults_div.click()
        # adult_value = driver.find_element(By.XPATH, '//span[@data-bui-ref="input-stepper-value"]')
        adult_dec_btn = driver.find_element(By.XPATH, '//button[@aria-label="Decrease number of Adults"]')
        adult_dec_btn.click()

        for i in range(adults-1):
            adult_dec_btn = driver.find_element(By.XPATH, '//button[@aria-label="Increase number of Adults"]')
            adult_dec_btn.click()

    def number_of_children(self, age=None):
        child_dec_btn = driver.find_element(By.XPATH, '//button[@aria-label="Increase number of Children"]')
        child_dec_btn.click()

        child_age = driver.find_element(By.XPATH, '//select[@data-group-child-age="0"]')
        child_age.click()

        age_value = Select(driver.find_element(By.NAME, "age"))  # Dropdown Menu
        age_value.select_by_visible_text(f'{age} years old')

    def room_numbers(self, room=None):
        for i in range(room-1):
            room_btn = driver.find_element(By.XPATH, '//button[@aria-label="Increase number of Rooms"]')
            room_btn.click()

    def search_results(self):
        search_btn = driver.find_element(By.XPATH, '//button[@data-sb-id="main"]')
        search_btn.click()

    def filtration(self):
        filter_category = BookingFilter(driver)
        filter_category.ratings(3,4,5)
        driver.refresh()
        filter_category.destination_details()
        filter_category.convert_to_pdf()








