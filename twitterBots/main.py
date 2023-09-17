import time

import undetected_chromedriver as uc
import json


profile_path ="/home/ambrose/.config/google-chrome/Profile 1"
options = uc.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode if needed
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
options.add_argument(f"user-data-dir={profile_path}")
driver = uc.Chrome(options=options, use_subprocess=True)
# Initialize WebDriver

# Load cookies from the JSON file
with open("/home/ambrose/PycharmProjects/WebScraping/webscrapping/twitterBots/bot/ambrose.json", "r") as file:
    cookies = json.load(file)

# Open Twitter and set cookies
driver.get("https://twitter.com")
time.sleep(555)
for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh the page to apply cookies
driver.refresh()

# The page should now show Twitter as if you were logged out

# Close the browser
driver.quit()
