import json
import time

from .GoogleLogin import GmailLogin
class Login:
    def __init__(self, driver, By):
        self.driver = driver
        self.By = By
        self.email = "ambrosetall@gmail.com"
        self.pwd = "ambroseTall3436"
    def quit_automation(self):
        self.driver.quit()

    def open_gmail(self):
        self.driver.get('https://www.gmail.com')
        self.add_cookies()
        time.sleep(5)

    def login_to_gmail(self):
        gmail = GmailLogin(self.driver, self.By)
        gmail.login_to_email(self.email, self.pwd)

    def maximize_window(self):
        self.driver.maximize_window()

    def start_twitter(self):
        username = self.driver.fin

    def add_cookies(self):
        # Load cookies from the JSON file
        with open("/home/ambrose/PycharmProjects/WebScraping/webscrapping/twitterBots/bot/ambrose.json", "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                print(e)

        self.driver.refresh()






