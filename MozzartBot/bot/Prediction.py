import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By   #find_element(By.ID)


class Predictions:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.driver.implicitly_wait(5)

    def analysis_function(self, home_team, away_team):
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        score = 'Not Safe'

        if len(home_team) > 10:
            home_team = home_team[0:10]
        if len(away_team) > 10:
            away_team = away_team[0:10]

        try:
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

            time.sleep(5)

            over_one_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
            lower = over_one_five.text
            print(f'Over 1.5 : {lower}')
            over_one = float(lower.strip("%"))

            over_two_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
            upper = over_two_five.text.strip()
            print(f'Over 2.5 : {upper}')
            over_two = float(upper.strip("%"))

            if over_one > 80:
                score = 'Over 1.5'

            if over_two > 85:
                score = 'Over 2.5'

            print(f'HomeTeam: {home_team}  AwayTeam: {away_team} PICK: {score}')
        except:
            print("Ignoring Team................")

        self.driver.refresh()

        print('ambro')

        home_page = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/a/img')
        home_page.click()

        print('mbithi')

        self.driver.switch_to.window(self.driver.window_handles[0])

        return score









