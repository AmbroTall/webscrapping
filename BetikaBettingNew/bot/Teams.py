import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from .analysis import Analyze
from .PlaceBet import PlaceBet
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Teams:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def teams_to_analyse(self):
        all_teams_container = self.driver.find_elements(By.CLASS_NAME, 'prebet-match')
        print(len(all_teams_container))

        for teamdiv in all_teams_container:
            league = teamdiv.text.split(" ")[0]
            print(league)
            all_teams = teamdiv.find_elements(By.CLASS_NAME, 'prebet-match__teams')
            # print(len(all_teams))
            for teams in all_teams:
                home_team = teams.find_element(By.CLASS_NAME, 'prebet-match__teams__home')
                away_team = teams.find_elements(By.TAG_NAME, 'span')[1]
                print(home_team.text, away_team.text)
                analyze = Analyze(self.driver, home_team.text, away_team.text, league)
                analyze.switch_statarea()
                time.sleep(2)
                x = analyze.teams_to_analyze()
                if x != "Not found":
                    time.sleep(3)
                    place = analyze.get_prediction()
                    print(place)
                analyze.close_page()
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", home_team)

                if place != "X":
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'start', inline: 'nearest', offsetTop: -arguments[0].offsetHeight * 0.05}); arguments[0].click();",
                        home_team)

                    wekelea = PlaceBet(self.driver, place)
                    wekelea.goals_section()
                    wekelea.go_back()
                    # print(wekelea)
                time.sleep(2)
                print("Nafika hapa", home_team.text)
    def wekelea(self):
        try:
            amount_input = self.driver.find_element(By.XPATH, '//input[@placeholder="Enters stake"]')
            amount_input.clear()
            amount_input.send_keys(50)

            btn_div = self.driver.find_element(By.CLASS_NAME, "betslip__details__buttons")
            place_bet = btn_div.find_element(By.TAG_NAME, "span")
            place_bet.click()

            success = "\n******🤑💰 Bet Placed Successfully 💰🤑******\n"
        except:
            success = "\n🥲Sorry Market Dry🥲\n"

        return success

