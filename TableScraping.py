from selenium import webdriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select  #Drop down menu selection (line-17)
import pandas as pd
import time

website = 'https://adamchoi.co.uk/overs/detailed'
path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)

driver.implicitly_wait(5)

all_matches_btn = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')   #Xpath
# all_matches_btn = driver.find_element(By.CSS_SELECTOR, 'button[onclick="All matches()"]')   #Css Selector
all_matches_btn.click()

country = Select(driver.find_element(By.ID, 'country'))  #Dropdown Menu
country.select_by_visible_text("Spain")

all_rows = driver.find_elements(By.TAG_NAME, 'tr')

date=[]
homeTeam=[]
scores=[]
awayTeam=[]

for row in all_rows:
    table_data = row.find_elements(By.TAG_NAME, 'td')
    date.append(table_data[0].text)
    homeTeam.append(table_data[1].text)
    scores.append(table_data[2].text)
    awayTeam.append(table_data[3].text)

df = pd.DataFrame({"date":date, "HomeTeam":homeTeam, "Results":scores, "awayTeam":awayTeam})
# df.to_csv("FootballScraped.csv", index=False)
print(df)


# api_key = BFyLtYVc1FALLtqH68TgX8m6e
# api_key_secret = y7ngTcE5Yg94YvcQ3y91bsfJXmlTcdwUZd3rzhzBT4JDxWjBqZ
# access_token = 895702399968587777-aOk2qkLdT7BGLQppZh8ukZEmNcyXHbe
# access_token_secret = FwWMGwDW33qaSFN6tIBxmY0vFR1GGMNTzpGVaLwnvTDBk

driver.quit()