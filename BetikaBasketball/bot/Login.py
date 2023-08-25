import time

from selenium import webdriver
from selenium.webdriver.common.by import By  # find_element(By.ID)
from .FilterGames import SelectFilter
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions

options = ChromeOptions()
path = '/home/ambrose/Documents/chromedriver'

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome()
#
# path = '/home/ambrose/Documents/chromedriver'
# driver = uc.Chrome(use_subprocess=True)


class Login:
	def __init__(self):
		# print("Ambro1")
		pass

	def quit_automation(self):
		driver.quit()

	def start_site(self):
		# print("Ambro1")
		driver.get('https://www.betika.com/en-ke/?utm_medium=pop_under&utm_source=propeller-ads&utm_campaign=pop-under_ke_acq_en_sb')

	def maximize_window(self):
		driver.maximize_window()

	def login(self, tel_no, password):
		driver.switch_to.window(driver.window_handles[0])
		# Explicit Wait until login button is clickable
		WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable(
				(By.XPATH, '//a[@class="top-session-button button button__secondary outline link"]'),  # Element filtration
			)
		)
		login = driver.find_element(By.XPATH, '//a[@class="top-session-button button button__secondary outline link"]')
		login.click()

		# Explicit Wait until input is visible
		WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable(
				(By.XPATH, '//input[@placeholder="e.g. 0712 234567"]'),  # Element filtration
			)
		)

		phone_input = driver.find_element(By.XPATH, '//input[@placeholder="e.g. 0712 234567"]')
		phone_input.send_keys(tel_no)

		password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
		password_input.send_keys(password)

		login_btn = driver.find_element(By.XPATH, '//button[@class="button account__payments__submit session__form__button login button button__secondary"]')
		login_btn.click()

	def betting(self):
		filter = SelectFilter(driver)
		time.sleep(5)
		filter.select_live_games()
		filter.select_team()

