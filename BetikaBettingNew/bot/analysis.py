import time

from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Analyze:
    def __init__(self, driver: WebDriver, home_team, away_team, league):
        self.driver = driver
        self.home_team = home_team
        self.away_team = away_team
        self.league = league
        if len(self.away_team.split(" ")) > 1:
            self.away_team = self.away_team.split(" ")
            # self.away_team = max(self.away_team.split(" "), key=len)
        if len(self.home_team.split(" ")) > 1:
            self.home_team = self.home_team.split(" ")
            # self.home_team = max(self.home_team.split(" "), key=len)

        # print('----------------->**AwayTeam', self.away_team)
        # print('----------------->**HomeTeam', self.home_team)

    # navigate between tabs
    def switch_statarea(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        # print(self.driver.current_url)

    def check_team(self, team):
        # Explicit Wait until input is visible
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'tat_td1'),
            )
        )
        table = self.driver.find_element(By.ID, 'tat_table')
        team_options = table.find_elements(By.TAG_NAME, "td")

        perfect_match = None  # Initialize a variable to store the perfect match

        for x in team_options:
            team_names = x.text.split("(")[0].strip()
            table_league = x.text[x.text.find("(")+1:x.text.find(")")]
            # print("----->", x.text[x.text.find("(")+1:x.text.find(")")])
            for home_word in team:
                if home_word in team_names.split(" "):
                    perfect_match = x  # Store the perfect match
                    break  # Exit the inner loop if a match is found
            if perfect_match and self.league == table_league:  # Exit the outer loop if a perfect match is found
                return x.click()
            # if self.league == table_league:
            #     return x.click()

    def teams_to_analyze(self):
        # Explicit Wait until input is visible
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'h_team'),
            )
        )

        #Checking if incoming team names has more than two words
        if type(self.away_team) == list:
            away_team = max(self.away_team, key=len)
        else:
            away_team = self.away_team
        if type(self.home_team) == list:
            home_team = max(self.home_team, key=len)
        else:
            home_team = self.home_team
        try:
            h_team = self.driver.find_element(By.ID, 'h_team')
            h_team.send_keys(home_team)
            time.sleep(1)
            self.check_team(self.home_team)

            g_team = self.driver.find_element(By.ID, 'g_team')
            g_team.send_keys(away_team)
            time.sleep(1)
            self.check_team(self.away_team)

            get_info = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/form/table/tbody/tr[4]/td[4]/input')
            get_info.click()
        except:
            return "Not Found"

    def get_prediction(self):
        place = "X"
        try:
            # Over/Under 1.5
            over_one_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
            print(over_one_five.text.strip("%"))

            # under_one_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[7]/td[2]/span')
            # print(under_one_five.text.strip("%"))
            # Over/Under 2.5
            over_two_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/span')
            print(over_two_five.text.strip("%"))

            # under_two_five = self.driver.find_element(By.XPATH, '//*[@id="main_subbody"]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/table/tbody/tr[7]/td[2]/span')
            # print(under_two_five.text.strip("%"))

            # Check odds of winning by higher percantage
            if float(over_one_five.text.strip("%")) > 70:
                place = "Over 1.5"
            if float(over_two_five.text.strip("%")) > 80:
                place = "Over 2.5"
            return place
        except:
            return place


    def close_page(self):
        home_page = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/a/img')
        home_page.click()

        self.driver.refresh()
        time.sleep(1)

        home_p = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/a/img')
        home_p.click()

        # Explicit Wait until input is visible
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'h_team'),
            )
        )
        self.driver.switch_to.window(self.driver.window_handles[0])





