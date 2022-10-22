from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from prettytable import PrettyTable
from .AnalysisBot import Analysis
import pandas as pd
import time

class Teams:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.driver.implicitly_wait(20)

    def filter_by_country(self):
        country_btn = self.driver.find_elements(By.CLASS_NAME, "prematch-nav__item")
        for x in country_btn:
            if x.text == "Countries":
                x.click()

        time.sleep(2)

    def select_country(self):
        select_country = self.driver.find_element(By.CLASS_NAME, "countries__list")
        select_country_btns = self.driver.find_elements(By.TAG_NAME, "button")
        print(select_country)
        # select_country[0].click()
        # for x in select_country:
        #     if x.text == "England":
        #         x.click()

        select_country_league = self.driver.find_elements(By.CLASS_NAME, "countries__detail")
        select_country_league[0].click()

    def filter_top_league(self):
        filter_btn = self.driver.find_element(By.CLASS_NAME, "match-filter__button__label")
        filter_btn.click()

        top_league_btn = self.driver.find_elements(By.CLASS_NAME, "match-filter__group__action")
        for x in top_league_btn:
            if x.text == "Top league":
                x.click()

        apply_btn = self.driver.find_element(By.CLASS_NAME, "match-filter__apply")
        apply_btn.click()

    def filter_today(self):
        today_filter = self.driver.find_element(By.CLASS_NAME, "match-filter__button__label")
        today_filter.click()

        today = self.driver.find_elements(By.CLASS_NAME, "match-filter__group__action")
        for x in today:
            if x.text == "Today":
                x.click()

        apply_btn = self.driver.find_element(By.CLASS_NAME, "match-filter__apply")
        apply_btn.click()

    def team_data(self):
        teams_collection = []
        team_boxes = self.driver.find_elements(By.CLASS_NAME, 'prebet-match')
        print(len(team_boxes))
        for i in team_boxes:
            time_header = i.find_element(By.CLASS_NAME, 'time')
            league = time_header.text.split(" ")[0]
            print(league)
            if "International" in time_header.text:
                continue
            else:
                teams = i.find_element(By.CLASS_NAME, 'prebet-match__teams')
                team = teams.find_elements(By.TAG_NAME, 'span')
                home_team = team[0].text
                away_team = team[1].text
                print(home_team)
                print(away_team)

                analyzed = self.analysis_function(home_team, away_team)
                print(analyzed,"\n")

                if analyzed == 'Not Safe':
                    continue

                self.place_bet(analyzed,i)
                # print(place_bet)

                teams_collection.append(
                    [home_team, away_team, analyzed]
                )

        placement = self.wekelea()
        print(teams_collection)
        print(placement)
        return teams_collection

    def analysis_function(self, home_team, away_team):
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        score = 'Not Safe'

        if len(home_team) > 10:
            home_team=home_team[0:10]
        if len(away_team) > 10:
            away_team = away_team[0:10]

        try:
            home_team_input = self.driver.find_element(By.ID, 'h_team')
            home_team_input.send_keys(home_team)
            time.sleep(1)
            select_home_team = self.driver.find_element(By.ID, "tat_tr1")
            select_home_team.click()

            # table = self.driver.find_element(By.ID, "tat_table")
            # displayed_home_teams = table.find_elements(By.TAG_NAME, "td")
            # for select_home_team in displayed_home_teams:
            #     filt_league = select_home_team.text.split("(")[1][0:-1]
            #     print("home",select_home_team.text)
            #     if filt_league == league:
            #         time.sleep(1)
            #         select_home_team.click()

            away_team_input = self.driver.find_element(By.ID, 'g_team')
            away_team_input.send_keys(away_team)
            time.sleep(1)
            select_away_team = self.driver.find_element(By.ID, "tat_tr1")
            select_away_team.click()

            # away_table = self.driver.find_element(By.ID, "tat_table")
            # displayed_away_teams = away_table.find_elements(By.TAG_NAME, "td")
            # for select_away_team in displayed_away_teams:
            #     filt_league = select_away_team.text.split("(")[1][0:-1]
            #     print("away", select_away_team.text)
            #     if filt_league == league:
            #         time.sleep(1)
            #         select_away_team.click()

            get_information_btn = self.driver.find_element(By.XPATH, '//input[@alt="GetResults"]')
            get_information_btn.click()

            time.sleep(10)

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

        home_page = self.driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/a/img')
        home_page.click()

        self.driver.switch_to.window(self.driver.window_handles[0])
        return score

    def place_bet(self, score, i):
        markets = i.find_element(By.CLASS_NAME, "prebet-match__markets")
        time.sleep(1)
        self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", markets)
        time.sleep(5)
        # print(markets.text)
        markets.click()

        filter_by_goals = self.driver.find_elements(By.CLASS_NAME, "market-btn")
        for x in filter_by_goals:
            if x.text == "Goals":
                x.click()

        total_market = self.driver.find_elements(By.CLASS_NAME, 'market')
        odds_container = total_market[0].find_element(By.XPATH, '//div[@multi="2"]')
        odds_elements = odds_container.find_elements(By.CLASS_NAME, 'odd')

        if score == 'Over 1.5':
            for x in odds_elements:
                if "Over 1.5" in x.text:
                    x.click()
        elif score == 'Over 2.5':
            for x in odds_elements:
                if "Over 2.5" in x.text:
                    x.click()
        else:
            print("Not Safe For betting")

        time.sleep(2)

        back_btn = self.driver.find_element(By.CLASS_NAME, "markets-header__nav__back")
        back_btn.click()

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








    # def analysis_site(self, driver):
    #     analysis = Analysis(driver, self.team_data())
    #     analysis.open_site()
    #     analysis.enter_teams()






