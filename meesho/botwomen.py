import os
import re
import time
from io import BytesIO
import multiprocessing

import pandas as pd
import requests
from PIL import Image
from selenium import webdriver
# import undetected_chromedriver as uc

from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()
# driver = webdriver.Chrome()

# Create a directory to save images
image_directory = "/home/ambrose/PycharmProjects/WebScraping/webscrapping/meesho/assets"
csv_file = "bot_3.csv"
os.makedirs(image_directory, exist_ok=True)
max_name_length = 50  # Adjust as needed

# Read the CSV file to get the main_search_urls
df = pd.read_csv(csv_file)
main_search_urls = df['Url'].tolist()
main_search_urls.reverse()

def get_website_data(url):
    # Navigate to the website
    time.sleep(1)
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    page_source = driver.page_source
    return page_source

count = 0
missed_products = 0

for link in main_search_urls:
    try:
        product_page_source = get_website_data(link)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/div/div[1]/div/div[1]'))
        )
        product_detail_page_soup = BeautifulSoup(product_page_source, 'html.parser')
        image_container = product_detail_page_soup.select('#__next > div:nth-of-type(3) > div > div:nth-of-type(1) > div > div:nth-of-type(1)')
        product_images = image_container[0].find_all('img')
        image_urls = [x.get('src') for x in product_images]
        print(image_urls)
        name = product_detail_page_soup.select_one('#__next > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(1) > span')
        for i, image_info in enumerate(image_urls[:4]):
            image_info = image_info.replace("64", "512")
            response = requests.get(image_info)
            print(response)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                cleaned_name = re.sub(r'[\\/*?:"<>|&]', '_', name.get_text())
                # Truncate the image name if it exceeds the maximum length
                if len(cleaned_name) > max_name_length:
                    cleaned_name = cleaned_name[:max_name_length]
                image_name = f"{cleaned_name}_image_{i + 1}.jpg"
                image_path = os.path.join(image_directory, image_name)
                image.save(image_path)

        count += 1
        print(f"Count {count} \n")
    except Exception as e:
        print("Product exception", e)
        print("\nMissed", missed_products,"\n")
        missed_products += 1
        continue


