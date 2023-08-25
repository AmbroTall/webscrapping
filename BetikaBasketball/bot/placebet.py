import time
import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Teams:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def basket_ball_live(self):
        url = "https://live.betika.com/v1/uo/matches?page=1&limit=1000&sub_type_id=1,186,340&sport=30&sort=1"
        payload = {}
        headers = {
            'authority': 'live.betika.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'if-modified-since': 'Mon, 12 Jun 2023 15:32:39 GMT',
            'origin': 'https://www.betika.com',
            'referer': 'https://www.betika.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Cookie': '__cf_bm=1A6uQ.ALku5Rhdj4tpWiJBagmqJMBU1ZdiEZckhm9f4-1686585725-0-AfQjMLar5lMoeHIdXJmBkppYCl2xK7D/C3wPwEIAG3LMJCm/AFC9yyftqnvMr4W2x4fOm1Rhv3+5prfL1J6EBUM='
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        r = response.json()
        data = r['data']
        live_teamdata = []
        for team in data:
            info = {}
            info['home_team'] = team['home_odd_key']
            info['away_team'] = team['away_team']
            scores = team['set_score'][-1]['score'].split(":")
            info['scores'] = [int(num) for num in scores]
            live_teamdata.append(info)
        return live_teamdata

    def go_back(self):
        back_btn = self.driver.find_element(By.CLASS_NAME, "markets-header__nav__back")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", back_btn)
        time.sleep(2)
        back_btn.click()

    def place_bet(self, predict, overall_total, odds_div):

        for b in odds_div[0]:
            over_under = b.find_element(By.CLASS_NAME, 'text-left').text
            odd_value = b.find_element(By.CLASS_NAME, 'odd__value').text
            if predict == "Over" and f'Over {overall_total}' in over_under:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", b)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", b)
                # status = self.wekelea()
                return f"Successfully places Over {overall_total} : {odd_value} \n {status}"
            elif predict == "Under" and f'Under {overall_total}' in over_under:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", b)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", b)
                # status = self.wekelea()
                return f"Successfully places Under {overall_total} : {odd_value} \n {status}"

    def wekelea(self):
        try:
            amount_input = self.driver.find_element(By.XPATH, '//input[@placeholder="Enters stake"]')
            amount_input.clear()
            amount_input.send_keys(50)

            btn_div = self.driver.find_element(By.CLASS_NAME, "betslip__details__buttons")
            place_bet_btn = btn_div.find_element(By.TAG_NAME, "span")
            place_bet_btn.click()

            return "\n******🤑💰 Bet Placed Successfully 💰🤑******\n"
        except:
            return "\n🥲Sorry Market Dry🥲\n"


    def get_scores_api(self,live_games, home_team, away_team):
        home_team = home_team.rstrip('.')
        away_team = away_team.rstrip('.')
        print("Home Team :", home_team)
        print("Away Team :", away_team)
        for match in live_games:
            if home_team.lower() in match['home_team'].lower() and away_team.lower() in match['away_team'].lower():
                return match['scores']
        return None

    def predict_over_under(self,current_scores, time_passed, overall_total):
        # Calculate the expected score per minute by the bookie
        expected_score_per_minute = overall_total / 10

        # Calculate the remaining total score needed to reach the overall total
        remaining_total = overall_total - sum(current_scores)

        # Calculate the remaining minutes in the current quarter
        remaining_minutes = 10 - (time_passed % 10)

        # Calculate the predicted total at the end of the current quarter
        predicted_total = sum(current_scores) + (expected_score_per_minute * remaining_minutes)

        # Determine if the predicted total will be over or under the overall total
        if predicted_total > overall_total:
            prediction = "Over"
        else:
            prediction = "Under"
        return prediction

    def find_highest_over(self, odds):
        highest_over = 0.0
        for odd in odds:
            over_under = odd['over_under']
            if over_under.startswith('Over'):
                numeric_value = float(over_under.split(' ')[1])
                if numeric_value > highest_over:
                    highest_over = numeric_value
        return highest_over

    def find_lowest_over(self, odds):
        lowest_over = float('inf')  # Initialize with a high value
        for odd in odds:
            over_under = odd['over_under']
            if over_under.startswith('Over'):
                numeric_value = float(over_under.split(' ')[1])
                if numeric_value < lowest_over:
                    lowest_over = numeric_value

        return lowest_over

    def find_total_section(self, quarter):
        time.sleep(2)
        markets = self.driver.find_elements(By.CLASS_NAME, "market")
        odds = []
        odds_div = []
        for x in markets:
            market_title = x.find_element(By.TAG_NAME, 'span')
            collapsed_vid = x.find_elements(By.TAG_NAME, 'div')[0]
            if f'{quarter} Quarter - Total' in market_title.text:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", market_title)
                time.sleep(2)
                if "collapsed" in collapsed_vid.get_attribute("class"):
                    self.driver.execute_script("arguments[0].click();", market_title)
                odds_divs = x.find_elements(By.CLASS_NAME, 'odd')
                odds_div.append(odds_divs)
                for b in odds_divs:
                    odd = {'over_under': b.find_element(By.CLASS_NAME, 'text-left').text, 'odd_value': b.find_element(By.CLASS_NAME, 'odd__value').text}
                    odds.append(odd)
        return odds, odds_div

    def report_module(self,result):
        # Open the file in append mode
        with open('betika.txt', 'a') as file:
            file.write(f'{result}\n')  # Append a newline character to separate each result

        # File is automatically closed after exiting the `with` block
        print("Bet recorded successful")

    def main_call(self):
        all_teams_containers = self.driver.find_element(By.CLASS_NAME, 'live__matches')
        all_teams_container = all_teams_containers.find_elements(By.CLASS_NAME, 'live-match')

        i = 0
        while True:
            time.sleep(10)
            if i >= len(all_teams_container):
                i = 0
            teamdiv = all_teams_container[i]
            WebDriverWait(teamdiv, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'live-match__teams__home')))
            league = teamdiv.text.split(" ")[0]
            quarter = teamdiv.find_element(By.CLASS_NAME, 'live-match__details__right__status').text.split(" ")[0]
            clock = teamdiv.find_element(By.CLASS_NAME, 'live-match__details__right__clock').text.split(":")[0]
            home = teamdiv.find_element(By.CLASS_NAME, 'live-match__teams__home')
            home_team = home.find_elements(By.TAG_NAME, 'span')[1].text
            away = teamdiv.find_element(By.CLASS_NAME, 'live-match__teams__away')
            away_team = away.find_elements(By.TAG_NAME, 'span')[1].text
            if clock == 'Live' or float(clock) % 10 >= 7 or float(clock) % 10 <= 5 or league.lower() == "college" or league.lower() == "nba":
                print(clock)
                print("Not good for placing")
                all_teams_containers = self.driver.find_element(By.CLASS_NAME, 'live__matches')
                all_teams_container = all_teams_containers.find_elements(By.CLASS_NAME, 'live-match')
                i += 1
                continue
            else:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", home)
                time.sleep(2)
                home.click()
                time.sleep(5)
                # Find the totals for a particular quarter from betika
                try:
                    odds, odds_div = self.find_total_section(quarter)
                    if len(odds) == 0:
                        self.go_back()
                        time.sleep(2)
                        all_teams_containers = self.driver.find_element(By.CLASS_NAME, 'live__matches')
                        all_teams_container = all_teams_containers.find_elements(By.CLASS_NAME, 'live-match')
                        i += 1
                        continue
                    else:
                        overall_total = self.find_highest_over(odds)
                        lowest_over = self.find_lowest_over(odds)
                        live_games = self.basket_ball_live()
                        current_scores = self.get_scores_api(live_games, home_team, away_team)
                        print(odds, current_scores, overall_total)
                        predict = self.predict_over_under(current_scores, float(clock), overall_total)
                        if predict == "Over":
                            overall_total = lowest_over
                        print("Hello this is overall total", overall_total)
                        bet = self.place_bet(predict, overall_total, odds_div)
                        time.sleep(2)
                        self.report_module({"League": league, "Home Team": home_team, "Away Team": away_team, "Current Totals":overall_total, "Odds": odds, "Bet Choice": predict, "Statement": bet})
                        print("Hello ", bet, "\n")
                        self.go_back()
                        time.sleep(5)
                        all_teams_containers = self.driver.find_element(By.CLASS_NAME, 'live__matches')
                        all_teams_container = all_teams_containers.find_elements(By.CLASS_NAME, 'live-match')
                        i += 1
                except Exception as e:
                    print(e)
                    self.go_back()
                    time.sleep(5)
                    all_teams_containers = self.driver.find_element(By.CLASS_NAME, 'live__matches')
                    all_teams_container = all_teams_containers.find_elements(By.CLASS_NAME, 'live-match')
                    i += 1
                    continue




