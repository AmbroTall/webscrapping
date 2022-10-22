import time
from selenium import webdriver
from selenium.webdriver.common.by import By   #find_element(By.ID)
from selenium.webdriver.support.ui import Select
from .Select_team import Teams

path = '/home/ambrose/Documents/chromedriver'
driver = webdriver.Chrome(path)
driver.execute_script("window.open('http://old.statarea.com/');")
driver.implicitly_wait(5)
# driver.maximize_window()

class Login:
    def __init__(self):
        pass

    def quit_automation(self):
        driver.quit()

    def start_site(self):
        driver.get('https://www.mozzartbet.co.ke/en?gclid=Cj0KCQjw_7KXBhCoARIsAPdPTfjnuRzPSBsaSQPG1pKigOOjRu3rlfY18IC9dhLe2ZWJhDucx2FSiTIaAt8sEALw_wcB#/promo/chachimbitisha-/62ebb19145954075abd34860')

    def login(self, tel_no, password):
        login = driver.find_element(By.CLASS_NAME, 'login-link')
        login.click()

        phone_input = driver.find_element(By.XPATH,'//*[@id="pageWrapper"]/div[1]/header/section[1]/article[2]/section/article/div[2]/div/form/input[1]')
        phone_input.send_keys(tel_no)

        password_input = driver.find_element(By.XPATH,'//*[@id="pageWrapper"]/div[1]/header/section[1]/article[2]/section/article/div[2]/div/form/input[2]')
        password_input.send_keys(password)

        login_btn = driver.find_element(By.XPATH,'//*[@id="pageWrapper"]/div[1]/header/section[1]/article[2]/section/article/div[2]/div/form/div[2]/button')
        login_btn.click()

        betting = driver.find_elements(By.CLASS_NAME,'offer-link')
        for x in betting:
            if x.text == "BETTING":
                time.sleep(2)
                x.click()

    def betting(self):
        x = Teams(driver)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        x.select_team()









