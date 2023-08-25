import time
from selenium.webdriver.common.by import By  # find_element(By.ID)
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlparse, parse_qs
import requests

tor_browser_path = '/home/ambrose/Documents/tor/tor-browser/Browser/firefox'

# Configure Firefox WebDriver options
options = Options()
options.binary_location = tor_browser_path

# Configure proxy settings to use Tor
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', '127.0.0.1')
options.set_preference('network.proxy.socks_port', 9150)

# Instantiate a new WebDriver instance with Tor Browser configuration
driver = webdriver.Firefox(options=options)
# options = ChromeOptions()
# path = '/home/ambrose/Documents/chromedriver'

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(path, chrome_options=options)

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
		back_btn = self.driver.find_element(By.XPATH, "//*[@id='mainview']/div/div/div[1]/div[2]/div[4]/event-markets/section/div[1]/div[1]/div[1]/div[1]")
		self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", back_btn)
		time.sleep(2)
		back_btn.click()

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
		home_team_quarter_scores = data['FirstDisplayed']['QuarterScores'][quater-1]['Value']
		away_team_quarter_scores = data['SecondDisplayed']['QuarterScores'][quater-1]['Value']
		print(home_team_quarter_scores, away_team_quarter_scores)
		total_scores = int(home_team_quarter_scores) + int(away_team_quarter_scores)
		return total_scores

	def main_call(self):
		time.sleep(5)
		all_teams_containers = self.driver.find_elements(By.CLASS_NAME, 'event-row-live')
		for x in all_teams_containers:
			if "to start" and "end of" in x.text.lower():
				print("Lefting 1")
				continue
			summary = x.text.split('\n')
			quater = summary[0]
			time_elapsed = summary[1]
			home_team = summary[2]
			away_team = summary[3]
			print(quater)
			print(time_elapsed)
			print(home_team)
			print(away_team)
			x.click()
			time.sleep(3)
			url = driver.current_url
			parsed_url = urlparse(url)
			event_id = parsed_url.path.split("/")[4]
			print(event_id)
			if quater.lower() == "third quarter":
				quarter_no = 3
			elif quater.lower() == "fourth quarter":
				quarter_no = 4
			elif quater.lower() == "first quarter":
				quarter_no = 1
			elif quater.lower() == "second quarter":
				quarter_no = 2
			else:
				print("Lefting 2")
				continue
			#Get real live scores
			quarter_scores = self.quater_scores_api(event_id, quarter_no)
			print(quarter_scores)
			market_selections = self.driver.find_elements(By.CLASS_NAME, 'market-selections-2 ')
			for x in market_selections:
				market_title = x.find_element(By.CLASS_NAME,"event-market-name")
				odds_selection = x.find_elements(By.TAG_NAME, 'div')
				# print(market_title.text)
				for b in odds_selection:
					b.click()
					print(b.text)




		time.sleep(333)
