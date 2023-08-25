import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .placebet import Teams
class SelectFilter:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def select_live_games(self):
        # Locate and click live games
        live_links = self.driver.find_elements(By.TAG_NAME, 'a')
        for link in live_links:
            print("AMBroo")
            href = link.get_attribute("href")
            if href == 'https://www.betika.com/en-ke/live':
                link.click()
                break
        time.sleep(2)
        # Select category basketball in the live section
        live_sports = self.driver.find_elements(By.CLASS_NAME, 'sports-list__item')
        for link in live_sports:
            print("Ndone")
            if "basketball" in link.text.lower():
                link.click()
                break

    def select_team(self):
        main_call = Teams(self.driver)
        main_call.main_call()

