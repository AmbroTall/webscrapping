from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select
from prettytable import PrettyTable
import pandas as pd


class BookingFilter:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def ratings(self, *star_ratings):
        for value in star_ratings:
            star_div = self.driver.find_element(By.XPATH, f'//div[@data-filters-item="class:class={value}"]')
            star = star_div.find_element(By.CLASS_NAME, 'bbdb949247')
            star.click()
        print("Ambro")

    def destination_details(self):
        data = []
        search_results = self.driver.find_element(By.ID, 'search_results_table')
        container_div = search_results.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
        for x in container_div:
            header = x.find_element(By.XPATH, '//div[@data-testid="title"]')
            print(header.text)
            price = x.find_element(By.XPATH, '//span[@class="fcab3ed991 bd73d13072"]')
            print(price.text)
            loc = x.find_element(By.XPATH, '//span[@data-testid="address"]')
            print(loc.text)
            data.append(
                [header.text, loc.text, price.text]
            )
        return data

    def convert_to_pdf(self):
        x = self.destination_details()
        hotel_name = []
        loc = []
        price = []
        for i in x:
            hotel_name.append(i[0])
            loc.append(i[1])
            price.append(i[2])
        df = pd.DataFrame({'Hotel Name':hotel_name, 'Location':loc, 'Price':price})
        print(df)
        df.to_csv("bookings.csv")




        # return data




