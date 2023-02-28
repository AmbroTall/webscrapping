import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Teams import Teams

class SelectFilter:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def select_today(self):
        # Explicit Wait until input is visible
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'match-filter__button__label'),
            )
        )
        filter = self.driver.find_element(By.CLASS_NAME, 'match-filter__button__label')
        filter.click()

        sort_by = self.driver.find_elements(By.CLASS_NAME, 'match-filter__group__action')

        for filter in sort_by:
            if filter.text == "Highlights":
                filter.click()
            if filter.text == "Today":
                filter.click()

        apply_filters = self.driver.find_element(By.CLASS_NAME, 'match-filter__apply')
        apply_filters.click()

    def select_team(self):
        teams = Teams(self.driver)
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(2)
        teams.teams_to_analyse()
        placement = teams.wekelea()
        print(placement)
