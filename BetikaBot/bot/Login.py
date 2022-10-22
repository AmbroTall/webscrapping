import time
from selenium import webdriver
from .BettingTeams import Teams
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select
from .constants import WEBSITE

path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
driver.execute_script("window.open('http://old.statarea.com/');")
driver.implicitly_wait(15)
driver.maximize_window()

class Login:
    def __init__(self):
        pass

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get(WEBSITE)

    def login(self, tel_no, password):
        login = driver.find_element(By.XPATH, '//a[@class="top-session-button button button__secondary outline link"]')
        login.click()

        phone_input = driver.find_element(By.XPATH,'//input[@placeholder="e.g. 0712 234567"]')
        phone_input.send_keys(tel_no)

        password_input = driver.find_element(By.XPATH,'//input[@type="password"]')
        password_input.send_keys(password)

        login_btn = driver.find_element(By.XPATH,'//button[@class="button account__payments__submit session__form__button login button button__secondary"]')
        login_btn.click()

    def Betting(self):
        betting = Teams(driver)
        # betting.filter_by_country()
        # betting.select_country()
        # time.sleep(2)
        betting.filter_top_league()
        time.sleep(2)
        betting.filter_today()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  #scrollbar till end of page
        time.sleep(5)
        betting.team_data()
        # betting.analysis_site(driver)



