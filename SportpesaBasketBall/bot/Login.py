import time
from selenium import webdriver
import re
from datetime import datetime
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from urllib.parse import urlparse, parse_qs
import requests

driver = webdriver.Chrome()


class Login:
    def __init__(self):
        self.driver = driver

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get('https://www.ke.sportpesa.com/en/live/events?sportId=4')

    def maximize_window(self):
        driver.maximize_window()

        # # Accept Cookies
        # cookies_bar = self.driver.find_element(By.ID, 'cookies-law-info-content')
        # cookie_btn = cookies_bar.find_element(By.TAG_NAME, "button")
        # cookie_btn.click()

    def login(self, tel_no, password):
        # Explicit Wait until login button is clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'username'),  # Element filtration
            )
        )

        phone_input = self.driver.find_element(By.ID, 'username')
        phone_input.send_keys(tel_no)

        # Accept Cookies
        cookies_bar = self.driver.find_element(By.ID, 'cookies-law-info-content')
        cookie_btn = cookies_bar.find_element(By.TAG_NAME, "button")
        cookie_btn.click()

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        login_btn = self.driver.find_element(By.XPATH, '//*[@id="secondary_login"]/input[4]')
        login_btn.click()

    def go_back(self):
        back_btn = self.driver.find_element(By.CLASS_NAME, "icon-back-button")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", back_btn)
        time.sleep(2)
        back_btn.click()

    def extract_integer_from_text(self, value):

        text = value
        match = re.search(r"\d+", text)

        if match:
            number = match.group()
            return int(number)

    def quater_scores_api(self, event_id, quater):
        url = f"https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/json?eventId={event_id}&cb=1688197270322"

        payload = {}
        headers = {
            'authority': 'sportpesa.betstream.betgenius.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'referer': f'https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/html?eventId={event_id}',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        r = response.json()
        data = r['Scoreboard']
        league = data['CompetitionName']
        teams_playing = data['DisplayName']
        total_home = data['FirstDisplayed']['GameScore']
        total_away = data['SecondDisplayed']['GameScore']
        home_team_quarter_scores = data['FirstDisplayed']['QuarterScores'][quater - 1]['Value']
        away_team_quarter_scores = data['SecondDisplayed']['QuarterScores'][quater - 1]['Value']
        total_quarter_secs = data['Clock']['NumberOfQuarterSeconds']
        remaining_quarter_secs_static = data['Clock']['SecondsRemainingInQuarter']
        remaining_secs = r['Commentary']['Actions'][0]['Action']['QuarterTimeRemaining']
        remaining_quarter_secs = int(remaining_secs) / 1000
        #Quarter Scores
        total_scores = int(home_team_quarter_scores) + int(away_team_quarter_scores)
        game_total_scores = int(total_home) + int(total_away)
        return total_scores, total_quarter_secs, remaining_quarter_secs, game_total_scores
    def find_odd(self, market_selections, quarter_name):
        for x in market_selections:
            market_title = x.find_element(By.CLASS_NAME, "event-market-name")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                x)
            if f"{quarter_name} QUARTER TOTAL POINTS OVER/UNDER" in market_title.text:
                odds_selection = x.find_elements(By.CLASS_NAME, 'event-text')
                for b in odds_selection:
                    try:
                        close_modal = self.driver.find_elements(By.CLASS_NAME, 'help-alert-close')[1]
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                            close_modal)
                        close_modal.click()
                        print("Modal Closed")
                    except:
                        print("No modal")
                        # print(b.text.split("\n"))
                        if "OVER (" in b.text.split("\n")[0]:
                            odd = self.extract_integer_from_text(b.text)
                            return odd + 1
        return False
    def click_odd_prediction(self, market_selections, quarter_name, prediction):
        for x in market_selections:
            market_title = x.find_element(By.CLASS_NAME, "event-market-name")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                x)
            if f"{quarter_name} QUARTER TOTAL POINTS OVER/UNDER" in market_title.text:
                odds_selection = x.find_elements(By.CLASS_NAME, 'event-text')
                for x in odds_selection:
                    if f'{prediction.upper()} (' in x.text:
                        x.click()

    def predict_over_under(self, current_scores, remaining_quarter_secs, overall_total, total_quarter_secs):
        # Calculate the expected score per minute by the bookie
        expected_score_per_sec = overall_total / total_quarter_secs
        # Calculate the predicted total at the end of the current quarter
        predicted_total = current_scores + (expected_score_per_sec * remaining_quarter_secs)
        # Determine if the predicted total will be over or under the overall total
        if predicted_total > overall_total:
            prediction = "Over"
        else:
            prediction = "Under"
        return prediction

    def place_bet(self,stake):
        try:
            amount = self.driver.find_element(By.ID, 'amount-live')
            time.sleep(1)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", amount)

            amount.clear()
            amount.send_keys(stake)

            place_bet = self.driver.find_element(By.XPATH, '//*[@id="$ctrl.form"]/div/div[3]/div/div[2]/a')
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", place_bet)
            time.sleep(1)
            place_bet.click()
            print("Hello Bot")
            time.sleep(1)
            confirm = self.driver.find_element(By.CLASS_NAME, 'confirm')
            confirm.click()
            time.sleep(2)
            print(confirm)
            return "\n******🤑💰 Bet Placed Successfully 💰🤑******\n"
        except:
            return "\n🥲Sorry Market Dry🥲\n"

    def report_module(self,result):
        # Open the file in append mode
        with open('sportpesa_live.txt', 'a') as file:
            file.write(f'{result}\n')  # Append a newline character to separate each result
        # File is automatically closed after exiting the `with` block
        print("Bet recorded successful")

    def error_function(self, i):
        self.go_back()
        self.driver.refresh()
        time.sleep(5)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
        all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
        i += 1
        return i, all_teams_containers

    def main_call(self):
        time.sleep(5)
        all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')

        i = 0
        while True:
            if i >= len(all_teams_containers):
                i = 0

            x = all_teams_containers[i]

            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", x)
            # Disecting the data
            summary = x.text.split('\n')
            quater = summary[0]
            time_elapsed = summary[1]
            home_team = summary[2]
            away_team = summary[3]
            print(quater)
            print(time_elapsed)
            print(home_team)
            print(away_team)
            remaining_time = self.extract_integer_from_text(time_elapsed)
            print("remaining time", remaining_time)
            if "to start" and "end of" in x.text.lower() :
                print("No match To Place")
                i += 1
                continue
            try:
                if quater.lower() == "third quarter":
                    quarter_no = 3
                    quarter_name = "3RD"
                elif quater.lower() == "fourth quarter":
                    quarter_no = 4
                    quarter_name = "4TH"
                    # print("4th quarter")
                    # i += 1
                    # continue
                elif quater.lower() == "first quarter":
                    quarter_no = 1
                    quarter_name = "1ST"
                elif quater.lower() == "second quarter":
                    quarter_no = 2
                    quarter_name = "2ND"
                else:
                    print("No match To Place")
                    i += 1
                    continue
                x.click()
                time.sleep(3)
                url = driver.current_url
                parsed_url = urlparse(url)
                event_id = parsed_url.path.split("/")[4]
                print(event_id)
                _, _, remaining_quarter_secs, _= self.quater_scores_api(event_id, quarter_no)
                print("This are the remaining sec", remaining_quarter_secs)
                # print("This is clock ", self.driver.find_element(By.CLASS_NAME, 'bg-clock-selector-live').text)
                if int(remaining_quarter_secs) > 250:
                    try:
                        i, all_teams_containers = self.error_function(i)
                        continue
                    except:
                        self.driver.refresh()
                        WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
                        all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')

                # driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(5)
                market_selections = self.driver.find_elements(By.CLASS_NAME, 'market-selections-2')

                # find market from site OVER/UNDER
                if market_selections:
                    odds = self.find_odd(market_selections, quarter_name)
                    print("Odds", odds)
                    if odds == False:
                        try:
                            i, all_teams_containers = self.error_function(i)
                            continue
                        except:
                            self.driver.refresh()
                            WebDriverWait(self.driver, 30).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
                            all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
                    else:
                        # Get real live scores
                        quarter_scores, total_quarter_secs, remaining_quarter_secs,_ = self.quater_scores_api(event_id, quarter_no)
                        print("API", quarter_scores, total_quarter_secs, remaining_quarter_secs)
                        prediction = self.predict_over_under(quarter_scores, int(remaining_quarter_secs), odds, int(total_quarter_secs))
                        print(f"\n++++++++💰💰💰Signal (Stake High): \033[1m{prediction}\033[0m 💰💰💰")
                        self.click_odd_prediction(market_selections, quarter_name, prediction)
                        if prediction == "Over":
                            print(self.place_bet(200))
                        else:
                            print(self.place_bet(150))

                        # Get the current date and time
                        current_datetime = datetime.now()
                        # Format the current date and time as "YYYY-MM-DD HH:MM:SS"
                        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        self.report_module({"Time Placed": formatted_datetime,"Home Team": home_team, "Away Team": away_team, "Quarter": quater, "Time Elapsed":(int(total_quarter_secs) - int(remaining_quarter_secs))/60,  "Current Totals":quarter_scores, "Odds": odds, "Bet Choice": prediction})
                        # time.sleep(3)
                        try:
                            i, all_teams_containers = self.error_function(i)
                            continue
                        except:
                            self.driver.refresh()
                            WebDriverWait(self.driver, 30).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
                            all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
                else:
                    try:
                        i, all_teams_containers = self.error_function(i)
                        continue
                    except:
                        self.driver.refresh()
                        WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
                        all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
            except:
                try:
                    i, all_teams_containers = self.error_function(i)
                    continue
                except:
                    self.driver.refresh()
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'event-row-live')))
                    all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')


        time.sleep(333)




