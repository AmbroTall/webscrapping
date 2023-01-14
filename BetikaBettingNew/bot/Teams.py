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
                time.sleep(2)

                # Explicit Wait until team is visible
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, 'prebet-match__teams__home'),
                    )
                )

                htmlelement = self.driver.find_element(By.TAG_NAME, 'html')
                htmlelement.send_keys(Keys.HOME)
                time.sleep(2)
                self.driver.execute_script("return arguments[0].scrollIntoView(true);",home_team)
                print("Nafika hapa", home_team.text)
                if place != "X":
                    home_team.click()
                    # time.sleep(2)
                    wekelea = PlaceBet(self.driver, place)
                    wekelea.goals_section()
                    wekelea.go_back()
                    # print(wekelea)
                time.sleep(2)

    def wekelea(self):
        try:
            amount_input = self.driver.find_element(By.XPATH, '//input[@placeholder="Enters stake"]')
            amount_input.clear()
            amount_input.send_keys(20)

            btn_div = self.driver.find_element(By.CLASS_NAME, "betslip__details__buttons")
            place_bet = btn_div.find_element(By.TAG_NAME, "span")
            place_bet.click()

            success = "\n******🤑💰 Bet Placed Successfully 💰🤑******\n"
        except:
            success = "\n🥲Sorry Market Dry🥲\n"

        return success


