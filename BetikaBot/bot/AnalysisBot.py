from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from prettytable import PrettyTable
# import pandas as pd
import time

class Analysis:
    def __init__(self, driver:WebDriver, team_collection):
        self.driver = driver
        self.team_collection = team_collection
        self.driver.implicitly_wait(20)

    def open_site(self):
        self.driver.switch_to.new_window()
        self.driver.get('http://old.statarea.com/')

    def enter_teams(self):
        for i in self.team_collection:
            home_team = i[0]
            away_team = i[1]

            if len(home_team.split(" ")) > 1:
                home_team = max(home_team.split(" "))
            elif len(away_team.split(" ")) > 1:
                away_team = max(away_team.split(" "))
            else:
                home_team = home_team
                away_team = away_team

            home_team_input = self.driver.find_element(By.ID, 'h_team')
            home_team_input.send_keys(home_team)
            time.sleep(1)
            select_home_team = self.driver.find_element(By.ID, "tat_tr1")
            select_home_team.click()

            away_team_input = self.driver.find_element(By.ID, 'g_team')
            away_team_input.send_keys(away_team)
            time.sleep(1)

            select_away_team = self.driver.find_element(By.ID, "tat_tr1")
            select_away_team.click()

            get_information_btn = self.driver.find_element(By.XPATH, '//input[@alt="GetResults"]')
            get_information_btn.click()

            time.sleep(10)

            try:
                over_one_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
                lower = over_one_five.text
                print(f'Over 1.5 : {lower}')
                over_one = float(lower.strip("%"))

                over_two_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
                upper = over_two_five.text.strip()
                print(f'Over 2.5 : {upper}')
                over_two = float(upper.strip("%"))

                score = 'Not Safe'
                if over_one > 70:
                    score = 'Over 1.5'
                elif over_two > 80:
                    score = 'Over 2.5'
                elif over_one > 70 and over_two > 80:
                    score = 'Over 2.5'
                else:
                    print(score)

                print(f'HomeTeam: {home_team}  AwayTeam: {away_team} PICK: {score}')

            except:
                pass

            time.sleep(2)
            self.driver.refresh()

            home_page = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/a/img')
            home_page.click()

            # print(add_close.text)


