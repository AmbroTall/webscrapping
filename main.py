import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
def my_scheduled_job():
	driver.maximize_window()
	driver.get('https://www.bbc.com/')
	all_links = driver.find_elements(By.XPATH, '//a[@class="media__link"]')

	links_homepage = []
	for link in all_links:
		links_homepage.append(link.get_attribute('href'))

	for x in links_homepage:
		scrap_news = get_news_info(x)
		print(scrap_news)

def get_news_info(url):
	driver.get(url)
	scrapped_data = []
	save_data = False
	try:
		# title = WebDriverWait(driver, 10).until(
		# 	EC.element_to_be_clickable(
		# 		(By.XPATH, '//h1[@id="main-heading"]'),
		# 	)
		# )
		# print(title.text)
		description_array = []
		descriptions = driver.find_elements(By.XPATH, '//div[@data-component="text-block"]')
		for x in descriptions:
			# print(x.text)
			description_array.append(x.text)

		time.sleep(3)

		description = ' '.join(description_array)
		print(description)
		save_data = True
	except:
		save_data = False


my_scheduled_job()
