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


def get_quarter_info(quarter):

    print("This is my quarter", quarter)
    quarter_lower = quarter.lower().strip()
    if quarter_lower == "firstquarter":
        quarter_no = 1
        quarter_name = "1ST"
    elif quarter_lower == "secondquarter":
        quarter_no = 2
        quarter_name = "2ND"
    elif quarter_lower == "thirdquarter":
        quarter_no = 3
        quarter_name = "3RD"
    elif quarter_lower == "fourthquarter":
        quarter_no = 4
        quarter_name = "4TH"
    else:
        print("No match To Place")
        return None  # Handle the case where there's no match
    return quarter_no, quarter_name

def find_below_260_or_nearest_second(dictionary_list):
    print("Result function", dictionary_list)
    nearest_second = None
    min_time_diff = float("inf")

    for item in dictionary_list:
        if "remaining_quarter_secs" in item:
            if 170 < item["remaining_quarter_secs"] < 260:
                continue  # Skip dictionaries with "remaining_quarter_secs" between 170 and 260
            time_diff = abs(item["remaining_quarter_secs"] - 260)
            if time_diff < min_time_diff:
                nearest_second = item
                min_time_diff = time_diff

    if nearest_second is not None:
        time_to_wait = nearest_second["remaining_quarter_secs"] - 260
        if time_to_wait > 0:
            print(f"Waiting for {time_to_wait} seconds...")
            time.sleep(time_to_wait)
            return nearest_second  # Return the nearest to 260
        return None  # Return None if no suitable "remaining_quarter_secs" values found

def predict_over_under(current_scores, remaining_quarter_secs, overall_total, total_quarter_secs):
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


def configure_betslip(stake):
    # Find the element using WebDriverWait
    slip_bar = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "betslip-options-trigger"))
    )

    # Click the element after it's found
    slip_bar.click()

    accept_oddschange = driver.find_elements(By.XPATH, '//input[@type="radio"]')
    accept_oddschange[0].click()

    default_amount = driver.find_element(By.ID, 'amount-user')
    default_amount.clear()
    default_amount.send_keys(int(stake))

    direct_bet_mode = driver.find_elements(By.CLASS_NAME, 'material-toggle')[0]
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
        direct_bet_mode)
    direct_bet_mode.click()
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
        slip_bar)
    time.sleep(5)

    slip_bar.click()



def request_function(url, headers, payload):
    while True:
        response = requests.request("GET", url, headers=headers, data=payload)
        r = response.json()
        time.sleep(2)
        if r:
            return r
class Login:
    def __init__(self):
        self.driver = driver

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get('https://www.ke.sportpesa.com/en/live/events?sportId=4')

    def maximize_window(self):
        driver.maximize_window()

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

    def request_function(self, url, headers, payload):
        while True:
            response = requests.request("GET", url, headers=headers, data=payload)
            r = response.json()
            time.sleep(2)
            if r:
                return r

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

        r = self.request_function(url, headers, payload)
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

    def place_bet(self):
        try:
            place_bet = self.driver.find_element(By.XPATH, '//*[@id="$ctrl.form"]/div/div[3]/div/div[2]/a')
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", place_bet)
            time.sleep(1)
            place_bet.click()
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

    def confirm_bet_placed(self, home_team, away_team, event_id, quarter_no, market_selections, quarter_name, odds):
        try:
            betslip_anchor = self.driver.find_element(By.ID, 'betslip-anchor')
            betslip_list_container = betslip_anchor.find_element(By.ID, 'selected-bets')
            betslip_lists = betslip_list_container.find_elements(By.TAG_NAME, 'li')
            for x in betslip_lists:
                if home_team and away_team in x.text:
                    return True
        except:
            print("Replacing the bet ...")
            self.prediction_function(self, event_id, quarter_no, market_selections, quarter_name, odds)

    def live_games_display(self):
        url = "https://www.ke.sportpesa.com/api/live/sports/4/events?count=15&offset=0"

        payload = {}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Atrue%7D%7D; locale=en; spkessid=u9335e7ldusjlra39bufefmndl; _ga=GA1.1.619053130.1693297829; LPSID-85738142=oBtwahmWT_GruGrVRahInw; _ga_5KBWG85NE7=GS1.1.1694886035.34.0.1694886035.60.0.0',
            'Referer': 'https://www.ke.sportpesa.com/en/live/events?sportId=4',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-App-Timezone': 'Africa/Nairobi',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        r = self.request_function(url, headers, payload)
        events = r['events']
        all_games = []
        for index, x in enumerate(events, start=0):
            games = {}
            event_id = x["id"]
            quarter = x['state']['period']
            status = x['state']['status']
            if status == "STARTED":
                quarter_no, quarter_name = get_quarter_info(quarter)
                print("Hello quarter",quarter_no, quarter_name)
                time.sleep(2)
                _, _, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
                games['position'] = index
                games['event_id'] = event_id
                games['remaining_quarter_secs'] = int(remaining_quarter_secs)
                games['quarter_name'] = quarter_name
                games['quarter_no'] = quarter_no
                all_games.append(games)
        result = find_below_260_or_nearest_second(all_games)
        if result is not None:
            print("Found dictionary:")
            return result['event_id'], result['position'], result['quarter_name'], result['quarter_no']
        else:
            print("hello")
            return None

    def prediction_function(self, event_id, quarter_no,market_selections,quarter_name, odds):
        # Get real live scores
        quarter_scores, total_quarter_secs, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
        print("API", quarter_scores, total_quarter_secs, remaining_quarter_secs)
        prediction = predict_over_under(quarter_scores, int(remaining_quarter_secs), odds, int(total_quarter_secs))
        print(f"\n++++++++💰💰💰Signal (Stake High): \033[1m{prediction}\033[0m 💰💰💰")
        self.click_odd_prediction(market_selections, quarter_name, prediction)
        print(self.place_bet())
    def main_call(self):
        time.sleep(5)
        configure_betslip(50)
        i = 0
        while True:
            try:
                event_id, game_position, quarter_name, quarter_no = self.live_games_display()
                print(game_position)
                self.driver.refresh()
                all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
                no_of_games = len(all_teams_containers)
                if no_of_games == 0:
                    return "No games"
                x = all_teams_containers[int(game_position)]

                self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", x)
                # Disecting the data
                summary = x.text.split('\n')
                quater = summary[0]
                time_elapsed = summary[1]
                home_team = summary[2]
                away_team = summary[3]

                x.click()
                time.sleep(5)
                market_selections = self.driver.find_elements(By.CLASS_NAME, 'market-selections-2')

                # find market from site OVER/UNDER
                if market_selections:
                    odds = self.find_odd(market_selections, quarter_name)
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
                        self.prediction_function(event_id, quarter_no,market_selections,quarter_name, odds)

                        self.confirm_bet_placed(home_team, away_team, event_id, quarter_no, market_selections,quarter_name, odds)
                        # Get the current date and time
                        # current_datetime = datetime.now()
                        # Format the current date and time as "YYYY-MM-DD HH:MM:SS"
                        # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        # self.report_module({"Time Placed": formatted_datetime,"Home Team": home_team, "Away Team": away_team, "Quarter": quater, "Time Elapsed":(int(total_quarter_secs) - int(remaining_quarter_secs))/60,  "Current Totals":quarter_scores, "Odds": odds, "Bet Choice": prediction})
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






