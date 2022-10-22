from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd

website = 'https://adamchoi.co.uk/overs/detailed'
path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)

driver.implicitly_wait(5)

all_matches = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches.click()

country = Select(driver.find_element(By.ID, 'country'))
country.select_by_visible_text('Germany')


table_data = driver.find_elements(By.TAG_NAME, 'tr')

date = []
homeTeam = []
scores = []
awayTeam = []
for data in table_data:
    col = data.find_elements(By.TAG_NAME, 'td')
    team = col[1].text
    if team == "Augsburg":
        print(col[0].text, col[1].text, col[2].text)
        # date.append(col[0].text)
        # homeTeam.append(col[1].text)
        # scores.append(col[2].text)
        # awayTeam.append(col[3].text)
    # print(col[0].text)


# df = pd.DataFrame({"date": date, "Home Team":homeTeam, "Scores": scores, "Away Team": awayTeam })
# print(df)
# df.to_csv("Testing.csv", index=False)