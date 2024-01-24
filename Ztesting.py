import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")  # Run in headless mode if needed

options.headless = False
url = 'https://mantrivip.com/'
# url = 'https://google.com/'

driver = uc.Chrome(options=options)
print(f"openining {url}" )

driver.get(url)

time.sleep(3333)

# initialize(url)
    
    
    
    

    