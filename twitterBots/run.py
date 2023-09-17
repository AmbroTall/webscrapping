import undetected_chromedriver as uc
from bot.login import Login
from selenium.webdriver.common.by import By

import time

profile_path ="/home/ambrose/.config/google-chrome/Profile 1"
options = uc.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode if needed
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
# options.add_argument(f"user-data-dir={profile_path}")
driver = uc.Chrome(options=options, use_subprocess=True)
driver.execute_script("window.open('https://twitter.com');")

bot = Login(driver, By)
bot.maximize_window()
bot.open_gmail()
bot.login_to_gmail()
time.sleep(3333)



# bot.login(tel_no='0722808670', password='ambroseTall3436')
time.sleep(3333)
# bot.main_call()
# bot.quit_automation()
