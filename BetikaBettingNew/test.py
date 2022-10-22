import time

from selenium.webdriver.common.keys import Keys  #Special Keys like F1, F2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = '/home/ambrose/Documents/chromedriver'
driver=webdriver.Chrome(path)
driver.get('http://old.statarea.com/results.php?team_host=Manchester+Utd+%28England%29&team_guest=Manchester+City+%28England%29&x=82&y=17')

# Over/Under 1.5
over_one_five = driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
print(over_one_five.text.strip("%"))

under_one_five = driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[7]/td[2]/span')
print(under_one_five.text.strip("%"))

# Over/Under 2.5
over_two_five = driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
print(over_two_five.text.strip("%"))

under_two_five = driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[7]/td[2]/span')
print(under_two_five.text.strip("%"))
# http://old.statarea.com/results.php?team_host=Manchester+Utd+%28England%29&team_guest=Manchester+City+%28England%29&x=82&y=17


