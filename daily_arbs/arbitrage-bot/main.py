import csv
import pickle
import time
import os
from typing import Any
from bs4 import BeautifulSoup
import openpyxl

import datetime
from colorama import Fore

from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class BetikaBot():
    def __init__(self, phoneNumber=None, password=None):
        self.browserProfile = Options()
        # self.browserProfile.add_argument("--headless")  # Run in headless mode
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browserProfile.add_argument("--disable-blink-features=AutomationControlled") 
        self.browserProfile.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        self.browserProfile.add_experimental_option("useAutomationExtension", False) 
        self.browser = webdriver.Chrome(options=self.browserProfile)
        self.browser.maximize_window()

        self.phoneNumber = phoneNumber
        self.password = password
        self.cookies_file_path = "cookies_.pkl"
        self.max_retries = 15

        self.wait = WebDriverWait(self.browser, 2)

        self.error = Fore.RED
        self.success = Fore.GREEN
        self.info = Fore.CYAN

        self.errorIcon = "❌"
        self.successIcon = "✅"
        self.infoIcon = "ℹ️ "

        self.filename = "extracted_odds.csv"
        self.output_filename = "arbitrage_results.csv"
        self.sort = ["Highlights", "Start time", "Top leagues"]
        self.day = [
            "Today", "Next 48hrs", "Tomorrow", "Wednesday", 
            "Thursday", "Friday", "Saturday", "Sunday", "Monday"
        ]
        self.markets = ["1x2 / Winner", "Double Chance", "1st Half 1x2", "Both Teams To Score"]
    
    def save_cookies(self):
        cookies = self.browser.get_cookies()
        pickle.dump(cookies, open(self.cookies_file_path, "wb"))

    def load_cookies(self):
        self.browser.get('https://www.betika.com/')

        with open(self.cookies_file_path, 'rb') as f:
            cookies = pickle.load(f)

        # Check if any cookies are expired
        now = datetime.datetime.now()
        expired_cookies = []
        for cookie in cookies:
            expiration = cookie.get('expiry')
            if expiration:
                expiration_date = datetime.datetime.fromtimestamp(expiration)
                if expiration_date < now:
                    expired_cookies.append(cookie)
                    print("Cookie has expired:", cookie)
                    os.remove(self.cookies_file_path)
                    return

        if expired_cookies:
            print("[*] One or more cookies have expired. Deleting the cookies file and restarting the login process.")
            os.remove(self.cookies_file_path)
            self.signIn()
        else:
            # Add the cookies to the browser instance
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        # Refresh the page to apply the cookies
        self.browser.refresh()

        
    def signIn(self):
        # Check if cookies file exists
        
        retry_flag = False

        for retry in range(self.max_retries):
            try:
                if not os.path.exists(self.cookies_file_path):
                    self.browser.get("https://www.betika.com/en-ke/login")
                    time.sleep(2)
                    phoneNumberInput = self.browser.find_element('css selector', 'input[type="text"]')
                    passwordInput = self.browser.find_element('css selector', 'input[type="password"]')
                    phoneNumberInput.send_keys(self.phoneNumber)
                    passwordInput.send_keys(self.password)
                    # passwordInput.send_keys(Keys.ENTER)
                    # time.sleep(getRandomTime())

                    try:
                        """Close Notifications"""
                        self.browser.find_element(By.XPATH, '//button[contains(text(), "Not Now")]').click()
                    except NoSuchElementException:
                        pass

                    # Save cookies
                    self.save_cookies()
                else:
                    # if previous logged in Load cookies from file
                    self.load_cookies()

                    time.sleep(60)

            except WebDriverException as e:
                print(self.error + f'{self.errorIcon} Retry {retry + 1} failed: {str(e)}')
                retry_flag = True
            
            if not retry_flag:
                break

            if retry == self.max_retries - 1:
                print(self.info + f'{self.infoIcon} Maximum retries exceeded. Exiting.')

    def sortGames(self, sort_by="Highlights", which_day="Today", market=None):
        if sort_by not in self.sort or which_day not in self.day or market not in self.markets:
            print("Invalid input values.")
            return
        
        filter_btns = [sort_by, which_day, market]
                
        self.browser.get("https://www.betika.com/en-ke/")
        filter_button_xpath = '//button[contains(@class, "match-filter__button")]'
        # wait for button to be visible
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, filter_button_xpath)))
        self.browser.find_element(By.XPATH, filter_button_xpath).click()

        # wait for dilter modal to open
        filter_modal_class = "modal__container"
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, filter_modal_class)))

         # Loop through the combined list and click buttons based on the text
        for btn in filter_btns:
            # Construct XPath based on the values
            xpath_text = f'//button[contains(text(), "{btn}")]'
            try:
                # Click the button
                self.browser.find_element(By.XPATH, xpath_text).click()
            except Exception as e:
                print(f"Failed to click the button with XPath: {xpath_text}. Error: {e}")
        
        # completed filtering - now close the modal
        apply_changes_xpath = '//button[contains(text(), "Apply")]'
        self.browser.find_element(By.XPATH, apply_changes_xpath).click()
        time.sleep(5)
    
    def getMatchInformation(self, market):
        # Wait for the data to load
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prebet-match')))

        # Create a CSV file
        with open('odds.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write the header to the CSV file
            if market == "Both Teams To Score":
                csv_writer.writerow(['League', 'Date', 'Home', 'Away', '1', '2'])
            else:
                csv_writer.writerow(['League', 'Date', 'Home', 'Away', '1', 'X', '2'])

            # Set a limit on the number of scrolls to avoid an infinite loop
            scroll_limit = 10
            scroll_count = 0

            while scroll_count < scroll_limit:
                # Find all prebet matches
                prebet_matches = self.browser.find_elements(By.CLASS_NAME, 'prebet-match')

                # Iterate through prebet matches
                for match in prebet_matches:
                    # Extract information from each match
                    # Find the element with the class 'time'
                    time_element = match.find_element(By.CLASS_NAME, 'time')
                    # Extract the league and date text from the 'time' element
                    league_and_date = time_element.text
                    # Split the text to separate the league and date
                    league, date = [part.strip() for part in league_and_date.split('\n')]

                    # teams = match.find_element(By.CLASS_NAME, 'prebet-match__teams').text.strip()
                    teams_element = match.find_element(By.CLASS_NAME, 'prebet-match__teams')

                    # Find both spans within the 'prebet-match__teams' element
                    home_team = teams_element.find_element(By.CLASS_NAME, 'prebet-match__teams__home').text.strip()
                    away_team = teams_element.find_element(By.XPATH, './span[2]').text.strip()

                    odds_elements = match.find_elements(By.CLASS_NAME, 'prebet-match__odd__odd-value')
                    # odds = [odd.text.strip() for odd in odds_elements]
                    odds = [odd.text.strip() for odd in odds_elements]


                    # Write the data to the CSV file
                    # Check if all odds are available and not "-"
                    if all(odds) and all(odd != "-" for odd in odds):
                        # Write the data to the CSV file
                        csv_writer.writerow([league, date, home_team, away_team] + odds)

                # Scroll down to load more content
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for the new content to load
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prebet-match')))

                scroll_count += 1

        # Close the browser
        self.browser.quit()

    def calculate_arbitrage_bet(self, odds, total_stake):
        prob = [1 / odd for odd in odds]
        total_prob = sum(prob)

        stakes = [(total_stake * p / total_prob) for p in prob]
        winnings = [stake * odd for stake, odd in zip(stakes, odds)]
        guaranteed_profit = (total_stake / total_prob) - total_stake

        stake1 = round(stakes[0], 2)
        stake2 = round(stakes[1], 2)
        
        return {
                "total_desired_stake": total_stake,
                "stake1": stake1,
                "stake1_winning": round(winnings[0]),
                "stake2": stake2,
                "stake2_winning": round(winnings[1]),

                "total_suggested_stake": stake1 + stake2,
                "guaranteed_profit": round(guaranteed_profit, 2)
            }

    def analyzeArbitrageOpprtunity(self, filename, total_stake):
        with open(filename, 'r', newline='') as infile, open(self.output_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['stake1', 'stake1_winning', 'stake2', 'stake2_winning', 'total_desired_stake', 'total_suggested_stake', 'guaranteed_profit']

            # Write the headers to the output CSV file
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Process each row in the input CSV file
            for row in reader:
                # odds1 = float(row['1'])
                # odds2 = float(row['2'])
                try:
                    odds1 = float(row['1'])
                    odds2 = float(row['2'])
                except ValueError:
                    odds1 = 0
                    odds2 = 0 

                # Calculate arbitrage using your function
                result = self.calculate_arbitrage_bet([odds1, odds2], total_stake)

                # Add the calculated values or "N/A" to the row
                if result is not None:
                    row.update(result)

                writer.writerow(row)
            



bot = BetikaBot("phone number", "username")
# bot.signIn()
bot.sortGames("Start time", "Tomorrow", "Both Teams To Score") 
bot.getMatchInformation(market="Both Teams To Score")
bot.analyzeArbitrageOpprtunity("odds.csv", 1000)
