from selenium.webdriver.common.keys import Keys  #Special Keys like F1, F2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = '/home/ambrose/Documents/chromedriver'
driver=webdriver.Chrome(path)

# Explicit Wait until (e.g Loading 0%-100%)
WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.ID, 'id-name'),   # Element filtration
        'Value to be' # Value to be
    )
)

# Handle form inputs
input = driver.find_element(By.ID, 'id')
input.send_keys(15)   #send value to the input
input.send_keys(Keys.ENTER)   #send special keys in the input