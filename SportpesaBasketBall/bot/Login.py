import json
import time
from datetime import datetime
import mysql.connector

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
import requests

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode without a GUI
# min_time_to_place = 160
time_to_place_over = 150

def get_quarter_info(quarter):
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
    nearest_second = None
    min_time_diff = float("inf")

    for item in dictionary_list:
        if "remaining_quarter_secs" in item:
            if item["remaining_quarter_secs"] < time_to_place_over:
                continue  # Skip dictionaries with "remaining_quarter_secs" between 170 and 260
            time_diff = abs(item["remaining_quarter_secs"] - time_to_place_over)
            if time_diff < min_time_diff:
                nearest_second = item
                min_time_diff = time_diff

    if nearest_second is not None:
        time_to_wait = nearest_second["remaining_quarter_secs"] - time_to_place_over
        if time_to_wait > 0:
            print(f"Waiting for {time_to_wait} seconds...")
            time.sleep(time_to_wait)
            return nearest_second  # Return the nearest to 260
        return None  # Return None if no suitable "remaining_quarter_secs" values found


def predict_over_under(current_scores, remaining_quarter_secs, bookies_total, total_quarter_secs):
    # Calculate the expected score per second by the bookie
    expected_score_per_sec = bookies_total / total_quarter_secs

    # Calculate the predicted total at the end of the current quarter
    predicted_total = current_scores + (expected_score_per_sec * remaining_quarter_secs)

    # Calculate the absolute difference between predicted and bookies' total
    score_difference = abs(predicted_total - bookies_total)

    # Calculate the confidence as a percentage based on the score difference
    max_possible_difference = max(predicted_total, bookies_total)
    confidence = min(1.0, 1 - (score_difference / max_possible_difference))
    confidence_percentage = int(confidence * 100)

    # Determine if the predicted total will be over or under the bookies' total
    if predicted_total > bookies_total:
        prediction = "Over"
    else:
        prediction = "Under"
    return prediction, confidence_percentage
#Function to find over / under odds from API


def prepare_bet(event_id, prediction, selections, sequence, market_id):
    # if prediction == "Over":
    #     prediction = "Under"
    # elif prediction == "Under":
    #     prediction = "Over"

    for odd in selections:
        selection_id = odd['id']
        odds = odd['odds']
        name = odd['name']
        outcome = odd['outcome']

        if name == prediction.capitalize():
            bet = [{"eventId": int(event_id), "marketId": int(market_id), "sequence": int(sequence),
                    "selectionId": int(selection_id), "odds": odds, "coeff": odds, "id": int(selection_id)}]
            print("This is my bet selection", bet)
            return bet, outcome


def report_module(event_id, home_team, away_team, remaining_quarter_seconds, prediction, quarter_scores,bookies_odds, quarter_no, percentage_win_ratio):
    try:
        # Replace with your actual database credentials
        db_config = {
            "host": "localhost",
            "user": "root",
            "database": "sportpesa",
            "password": None,  # Assuming no password
        }

        # Create a connection to the database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        current_time_eat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sample data to insert
        data_to_insert = {
            "event_id": event_id,
            "home_team": home_team,
            "away_team": away_team,
            "time_placed": current_time_eat,  # Replace with the actual time
            "remaining_quarter_seconds": remaining_quarter_seconds,
            "quarter_no": quarter_no,
            "prediction": prediction,
            "quarter_scores": quarter_scores,
            "percentage_win_ratio": percentage_win_ratio,  # Can be None if you don't have a value
            "bookies_odds": bookies_odds,
            "results": None,  # Can be None if you don't have a value
        }

        # SQL statement for insertion
        insert_query = """
        INSERT INTO live_basketball
        (event_id, home_team, away_team, time_placed, remaining_quarter_seconds, quarter_no, prediction, quarter_scores, percentage_win_ratio, bookies_odds, results)
        VALUES
        (%(event_id)s, %(home_team)s, %(away_team)s, %(time_placed)s, %(remaining_quarter_seconds)s, %(quarter_no)s, %(prediction)s, %(quarter_scores)s, %(percentage_win_ratio)s, %(bookies_odds)s, %(results)s)
        """

        # Execute the insertion query
        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Bet recorded successfully")
    except Exception as e:
        print("Not recorded", e)


class Login:
    def __init__(self):
        session = requests.Session()
        driver = webdriver.Chrome(options=chrome_options)
        self.driver = driver
        self.session = session

    def quit_automation(self):
        self.driver.quit()

    def start_site(self):
        self.driver.get('https://www.ke.sportpesa.com/en/live/events?sportId=4')

    def maximize_window(self):
        self.driver.maximize_window()

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

        time.sleep(5)
        # Get the cookies
        cookies = self.driver.get_cookies()

        # Print the cookies
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        print("Logging in successfully ...")
        self.quit_automation()


    def go_back(self):
        back_btn = self.driver.find_element(By.CLASS_NAME, "icon-back-button")
        self.scroll_element_into_view(back_btn)
        time.sleep(2)
        back_btn.click()

    def configure_betslip(self, stake):
        # Find the element using WebDriverWait
        slip_bar = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "betslip-options-trigger"))
        )

        # Click the element after it's found
        slip_bar.click()

        accept_oddschange = self.driver.find_elements(By.XPATH, '//input[@type="radio"]')
        accept_oddschange[0].click()

        default_amount = self.driver.find_element(By.ID, 'amount-user')
        default_amount.clear()
        default_amount.send_keys(int(stake))

        direct_bet_mode = self.driver.find_elements(By.CLASS_NAME, 'material-toggle')[0]
        self.scroll_element_into_view(direct_bet_mode)
        direct_bet_mode.click()
        self.scroll_element_into_view(slip_bar)
        time.sleep(5)

        slip_bar.click()

    def markets_odds(self, event_id, quarter_name):
        url = f"https://www.ke.sportpesa.com/api/live/event/markets?eventId={event_id}"

        payload = {}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Afalse%7D%7D; locale=en; LPSID-85738142=PiTQAsNOTja-Jw7EGS48yg; spkessid=nh4kp7d721dm3t3mugrd2rva7g; _hjSession_1199008=eyJpZCI6IjhkYzhlMjE2LTliMzEtNDhkNC05NDkyLTE4MTAxY2Q1YTNjYiIsImNyZWF0ZWQiOjE2OTUxNTIyMjk5MjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _ga=GA1.1.619053130.1693297829; _ga_5KBWG85NE7=GS1.1.1695152217.60.1.1695153113.60.0.0; visited=1',
            'Referer': 'https://www.ke.sportpesa.com/en/live/events/10499188/markets?sportId=4&paginationOffset=0',
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
        markets = r['markets']
        for market in markets:
            market_name = market['name']
            sequence = market['sequence']
            market_id = market['id']
            status = market['status']  # Suspended/Open
            selections = market['selections']
            outcome = int(float(market['handicap']))

            if market_name == f"{quarter_name.lower()} Quarter Total Points Over/Under" and status == "Open":
                print("Found a market")
                return selections[0]['odds'], selections, sequence, market_id, status, outcome
        print("Market Not Found ...")
        return None

    def check_placed_bets(self):
        url = "https://www.ke.sportpesa.com/api/live/bets"

        payload = {}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://www.ke.sportpesa.com/en/live/events/10349415/markets?sportId=4',
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
        response = self.session.get(url, headers=headers, data=payload)
        r = response.json()
        bets_placed = r['bets']
        return bets_placed

    def place_bet_api(self, bet, stake):
        url = "https://www.ke.sportpesa.com/api/live/place"

        # Create a Python dictionary for your payload
        payload = {
            "stake": f"{stake}.00",
            "amount": f"{stake}.00",
            "selections": bet,
            "bets": bet,
            "acceptOdds": True,
            "betSpinner": -2
        }

        # Convert the dictionary to a JSON string
        payload_json = json.dumps(payload)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.ke.sportpesa.com',
            'Referer': 'https://www.ke.sportpesa.com/en/live/events/10393000/markets?sportId=4&paginationOffset=0',
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
        print("Session", self.session)
        print(f"Payload \n {payload} \n")
        response = self.session.post(url, headers=headers, data=payload_json)
        r = response.json()
        print("Bet response", r)
        print("Place bet status code", response.status_code)
        return r

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
        # Quarter Scores
        total_scores = int(home_team_quarter_scores) + int(away_team_quarter_scores)
        game_total_scores = int(total_home) + int(total_away)
        return total_scores, total_quarter_secs, remaining_quarter_secs, game_total_scores

    def find_odd(self, market_selections, quarter_name):
        for x in market_selections:
            market_title = x.find_element(By.CLASS_NAME, "event-market-name")
            self.scroll_element_into_view(x)
            if f"{quarter_name} QUARTER TOTAL POINTS OVER/UNDER" in market_title.text:
                odds_selection = x.find_elements(By.CLASS_NAME, 'event-text')
                for b in odds_selection:
                    try:
                        close_modal = self.driver.find_elements(By.CLASS_NAME, 'help-alert-close')[1]
                        self.scroll_element_into_view(close_modal)
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
            self.scroll_element_into_view(market_title)
            if f"{quarter_name} QUARTER TOTAL POINTS OVER/UNDER" in market_title.text:
                odds_selection = x.find_elements(By.CLASS_NAME, 'event-text')
                for x in odds_selection:
                    if f'{prediction.upper()} (' in x.text:
                        x.click()

    def place_bet(self):
        try:
            place_bet = self.driver.find_element(By.XPATH, '//*[@id="$ctrl.form"]/div/div[3]/div/div[2]/a')
            self.scroll_element_into_view(place_bet)
            time.sleep(1)
            place_bet.click()
            time.sleep(5)
            return "\n******🤑💰 Bet Placed Successfully 💰🤑******\n"
        except:
            return "\n🥲Sorry Market Dry🥲\n"

    def error_function(self):
        print("Reaching error function")
        try:
            self.go_back()
        except:
            pass


    def live_games_display(self):
        print("Starting games...")
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
        try:
            r = self.request_function(url, headers, payload)
            events = r['events']
            print("Live games = ", events)
        except:
            return None

        all_games = []

        for index, x in enumerate(events, start=0):
            games = {}
            event_id = x["id"]
            home_team = x["competitors"][0]['name']
            away_team = x["competitors"][1]['name']
            quarter = x['state']['period']
            status = x['state']['status']
            if status == "STARTED":
                quarter_no, quarter_name = get_quarter_info(quarter)
                print("Hello quarter", quarter_no, quarter_name)
                _, _, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
                games['position'] = index
                games['event_id'] = event_id
                games['remaining_quarter_secs'] = int(remaining_quarter_secs)
                games['quarter_name'] = quarter_name
                games['quarter_no'] = quarter_no
                games['away_team'] = away_team
                games['home_team'] = home_team
                all_games.append(games)

        result = find_below_260_or_nearest_second(all_games)
        if result is not None:
            print("Found dictionary:")
            return result
        elif len(events) == 0:
            return None
        else:
            print("Waiting for 5 min (Teams on Break) ... ")
            time.sleep(300)

    def prediction_function(self, event_id, quarter_no, market_selections, quarter_name):
        # Get real live scores
        try:
            odds = self.find_odd(market_selections, quarter_name)
        except:
            self.driver.refresh()
            time.sleep(3)
            odds = self.find_odd(market_selections, quarter_name)

        quarter_scores, total_quarter_secs, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
        print("API", quarter_scores, total_quarter_secs, remaining_quarter_secs)
        prediction,_ = predict_over_under(quarter_scores, int(remaining_quarter_secs), odds, int(total_quarter_secs))
        print(f"\n++++++++💰💰💰Signal (Stake High): \033[1m{prediction}\033[0m 💰💰💰")
        self.click_odd_prediction(market_selections, quarter_name, prediction)
        print(self.place_bet())


    def scroll_element_into_view(self, x):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", x)


    def placing_bet_logic_api(self, event_id, quarter_no, quarter_name, home_team, away_team):
        i = 0
        while True:
            if i > 10:
                return False
            try:
                confirm_betslip = self.check_placed_bets()
                print(confirm_betslip)
                if len(confirm_betslip) > 0:
                    # Iterate through the selections in the 'bets' data
                    for bet in confirm_betslip:
                        selections = bet['selections']
                        for selection in selections:
                            if selection['eventId'] == event_id:
                                print("\n******🤑💰 Bet Placed Successfully 💰🤑******\n")
                                return None
                print("Betting logic")
                quarter_scores, total_quarter_secs, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
                if remaining_quarter_secs < 120:
                    return None
                print("2")
                odds, selections, sequence, market_id, status, outcome = self.markets_odds(event_id, quarter_name)
                print("3")
                prediction, percentage = predict_over_under(quarter_scores, int(remaining_quarter_secs), outcome, int(total_quarter_secs))

                print("4")
                bet, bet_placed_outcome = prepare_bet(event_id, prediction, selections, sequence, market_id)

                print("5")
                weka_kitu = self.place_bet_api(bet, 20)
                print("This is my bet", outcome, odds, prediction, bet_placed_outcome)
                report_module(event_id, home_team, away_team, remaining_quarter_secs, bet_placed_outcome, quarter_scores, odds,quarter_no, percentage)
            except Exception as e:
                i += 1
                print("Retrying to place after missing on first ...", e)
                time.sleep(3)

    def loop_till_time_is_reached(self,event_id, quarter_no):
        print("Looping to find time")
        while True:
            _, _, remaining_quarter_secs, _ = self.quater_scores_api(event_id, quarter_no)
            if remaining_quarter_secs > time_to_place_over:
                time_to_sleep = remaining_quarter_secs - time_to_place_over
                print(f"Waiting seconds : {time_to_sleep}")
                time.sleep(time_to_sleep)
            else:
                print("Awakening")
                return True

    def main_call(self):
        while True:
            try:
                result = self.live_games_display()
                if result is None:
                    break
                event_id = result['event_id']
                home_team = result['home_team']
                away_team = result['away_team']
                quarter_name = result['quarter_name']
                quarter_no = result['quarter_no']
                print("1")
                self.loop_till_time_is_reached(event_id, quarter_no)
                self.placing_bet_logic_api(event_id, quarter_no, quarter_name, home_team, away_team)
            except Exception as e:
                print(f"Restarting function {e} \n")
                pass