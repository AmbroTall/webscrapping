from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.common.keys import Keys
import time

path = '/home/ambrose/Documents/chromedriver'
options = webdriver.ChromeOptions()
# options.add_argument('proxy-server=197.237.83.202:3128')
options.add_argument(r'--user-data-dir=/home/ambrose/.config/google-chrome/Default')

driver = uc.Chrome(use_subprocess=True)
driver.maximize_window()

# navigate to Gmail's sign-in page
driver.get('https://www.gmail.com')
time.sleep(2) # wait for page to load
truth_email = "cashhomebuyersincusa@gmail.com"
truth_password = "tech6491"
# enter email address and click next button
email_input = driver.find_element(By.ID,'identifierId')
email_input.send_keys(truth_email)
next_button = driver.find_element(By.XPATH,"//span[text()='Next']")
time.sleep(2)
next_button.click()
time.sleep(5) # wait for next page to load

# enter password and click sign in button
password_input = driver.find_element(By.XPATH, "//input[@type='password']")
password_input.send_keys(truth_password)
signin_button = driver.find_element(By.XPATH, "//span[text()='Next']")
time.sleep(2)
signin_button.click()
time.sleep(5) # wait for sign-in to complete

conversation_link = driver.find_element(By.XPATH, "(//span[@class='bog'])[1]")
conversation_link.click()
time.sleep(5) # wait for conversation to load

# click the first hyperlink in the conversation
verify_link = driver.find_element(By.XPATH,"//a[text()='VERIFY ACCOUNT']")
verify_link.click()


time.sleep(555)

# close the browser window
driver.quit()
