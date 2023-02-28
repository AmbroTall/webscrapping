from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class PlaceBet:
    def __init__(self, driver:WebDriver, place):
        self.driver = driver
        self.place = place

    def goals_section(self):
        try:
            # Explicit Wait until goals btn is visible
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'market-btn'),
                )
            )

            filter_by_goals = self.driver.find_elements(By.CLASS_NAME, "market-btn")
            for x in filter_by_goals:
                if x.text == "Goals":
                    x.click()

            total_market = self.driver.find_elements(By.CLASS_NAME, 'market')
            odds_container = total_market[0].find_element(By.XPATH, '//div[@multi="2"]')
            odds_elements = odds_container.find_elements(By.CLASS_NAME, 'odd')

            for x in odds_elements:
                if self.place in x.text:
                    x.click()
        except:
            print("Market not found")

    def go_back(self):
        back_btn = self.driver.find_element(By.CLASS_NAME, "markets-header__nav__back")
        back_btn.click()
