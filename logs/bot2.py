import os
import re
import time
from io import BytesIO

import pandas as pd
import requests
from PIL import Image
from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = uc.Chrome()
# driver = webdriver.Chrome()
search_strings = ['electronics']
main_search_urls = [f"https://www.meesho.com/search?q={x}&searchType=manual&searchIdentifier=text_search" for x in search_strings]



# Create a directory to save images
image_directory = "/home/ambrose/PycharmProjects/WebScraping/webscrapping/meesho/assets"
csv_file = "/meesho/electronics.csv"
os.makedirs(image_directory, exist_ok=True)
max_name_length = 50  # Adjust as needed

# Create a Pandas DataFrame to store product information
data = {
    'Name': [],
    'Category': [],
    'Product_details': [],
    'Price': [],
    'Image_1': [],
    'Image_2': [],
    'Image_3': [],
    'Image_4': []
}

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=[
        'Name',
        'Category',
        'Product_details',
        'Price',
        'Image_1',
        'Image_2',
        'Image_3',
        'Image_4',
        'Url'
    ])
    df.to_csv(csv_file, index=False)
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
for url in main_search_urls:
    for i in range(1, 500):
        url_pages= f'{url}&page={i}'
        try:
            page_source = get_website_data(url_pages)
            main_search_page_soup = BeautifulSoup(page_source, 'html.parser')
            # Wait for the element with the specified XPath to be present
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'//div[@data-page={i}]'))
            )
            # Use the XPath //div[@data-page="1"] to find the first matching element
            element = main_search_page_soup.find(True, {'data-page': f'{i}'})

            links_to_product = element.find_all('a')
            absolute_product_links = [f"https://www.meesho.com{x.get('href')}" for x in links_to_product]

            # Scrape each product detail
            for link in absolute_product_links:
                existing_data = pd.read_csv(csv_file)

                if link in existing_data['Url'].values:
                    count += 1
                    print(count)
                    continue
                try:
                    product_page_source = get_website_data(link)
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/div/div[1]/div/div[1]'))
                    )
                    product_detail_page_soup = BeautifulSoup(product_page_source, 'html.parser')
                    image_container = product_detail_page_soup.select('#__next > div:nth-of-type(3) > div > div:nth-of-type(1) > div > div:nth-of-type(1)')
                    product_images = image_container[0].find_all('img')
                    image_urls = [x.get('src') for x in product_images]
                    product_details = product_detail_page_soup.select_one('#__next > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(3) > div')
                    p_tags = product_details.find_all('p')
                    # Extract and print the text within all <p> tags
                    product_details_container = []
                    for p_tag in p_tags:
                        product_details_container.append(p_tag.get_text(strip=True))
                    name = product_detail_page_soup.select_one('#__next > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(1) > span')
                    price = product_detail_page_soup.select_one(
                        '#__next > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h4')
                    image_paths = []
                    for i, image_info in enumerate(image_urls[:4]):
                        response = requests.get(image_info)
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
                            image_paths.append(image_name)

                    # Create a new dictionary with image paths
                    new_data = {
                        'Name': name.get_text(),
                        'Category': url,
                        'Product_details': f'{product_details_container}',
                        'Price': price.get_text(),
                        'Image_1': image_paths[0] if len(image_paths) >= 1 else '',
                        'Image_2': image_paths[1] if len(image_paths) >= 2 else '',
                        'Image_3': image_paths[2] if len(image_paths) >= 3 else '',
                        'Image_4': image_paths[3] if len(image_paths) >= 4 else '',
                        "Url": link
                    }
                    new_product_df = pd.DataFrame([new_data])

                    print("this is my daata",new_data)

                    # Check if the 'Name' already exists in the CSV, if not, append the data
                    combined_data = pd.concat([existing_data, new_product_df], ignore_index=True)

                    # Save the combined data to the CSV file
                    combined_data.to_csv(csv_file, index=False)

                    count += 1
                    print(f"Count {count} \n Image urls {image_urls} \n Name {name.get_text()} \n Price {price.get_text()} \n Product Details {product_details_container}")
                except Exception as e:
                    print("Product exception", e)
                    print("\nMissed", missed_products,"\n")
                    missed_products += 1
                    continue
        except Exception as e:
            print("Search exception", e)
            print("\nMissed", missed_products,"\n")
            missed_products += 1
            continue




