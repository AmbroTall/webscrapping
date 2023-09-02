# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 17:58:17 2022

@author: Asad Mehmood
"""

import time
from bs4 import BeautifulSoup as soup
import helper as h
from db import Mysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os
import pandas as pd
import numpy as np
from datetime import datetime

global dev
dev = True

# Current Directory
current_directory = os.getcwd()

def init_driver():
    driver_dir = os.path.join(current_directory, 'drivers')
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')

    chrome_exe = "chromedriver.exe"
    try:
        path_to_driver = os.path.join(driver_dir, chrome_exe)
        browser = webdriver.Chrome(path_to_driver, options=options)
    except:
        path_to_driver = os.path.join(driver_dir, chrome_exe.replace(".exe", ""))
        browser = webdriver.Chrome(path_to_driver, options=options)
    if dev:
        browser.set_window_size(1300, 1000)
    return browser

def get_dates(date_start, date_end):
    date_range_first = pd.date_range(start=date_start, end=date_end, freq='MS')
    date_range_last = pd.date_range(start=pd.Timestamp(date_start) + pd.DateOffset(months=1), end=pd.Timestamp(date_end) + pd.DateOffset(months=1), freq='MS')

    date_first_day = date_range_first[::-1]
    date_last_day = date_range_last[::-1]
    dates = [(day_f, day_l - np.timedelta64(1, 'D')) for day_f, day_l in zip(date_first_day, date_last_day)]
    return dates

def get_Notice(tag_content, state, publisher):
    web_scrape = dict()
    br_tag = "<br/>"
    b_tag = "<b>"
    info_tags = [tag.extract() for tag in tag_content.find_all('h6')]
    post_ID = info_tags[-1].text.strip()

    h2_tag = tag_content.find('h2', {'class': 'dbr-title'})
    h2_text = h2_tag.text.strip()
    text_len = len(h2_text)

    if text_len > 100:
        content = h2_text.strip()
        if b_tag in str(h2_tag):
            h2_tag = soup(str(h2_tag).replace(b_tag, " ").replace(b_tag.replace("<", "</"), " "), "html.parser")
            h2_text = h2_tag.text.strip()
            content = h2_text.strip()
    else:
        content = tag_content.text.strip()
        if b_tag in str(tag_content):
            tag_content = soup(str(tag_content).replace(b_tag, " ").replace(b_tag.replace("<", "</"), " "), "html.parser")
        if br_tag in str(tag_content):
            next_line = "\n"
            tag_content = soup(str(tag_content).replace(br_tag, next_line), "html.parser")
            content_raw = tag_content.text.strip()
            content_split = [t.strip() for t in content_raw.split(next_line)]
            content = next_line.join(content_split)

    notice = content.strip()

    web_scrape = h.parse_Address(notice, post_ID, state, publisher)
    time_dict = {'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    web_scrape.update(time_dict)
    return web_scrape

def search_pages(limited, state, publisher, database, source):
    all_notices = list()
    process = True
    try:
        h.print_log("Initializing webdriver...\n")
        driver = init_driver()
    except Exception as e:
        error_str = "{}: {}".format(str(type(e).__name__), str(e))
        h.print_log(error_str, True)
        process = False
        h.print_log("ERROR: Unable to Initialize webdriver", True)

    if process:
        per_page = 100
        
        testing = False
        # Get loggers information
        date_now, r_starts, r_finish = h.start_logger(testing, limited, database, source)
        n_items = limited // per_page
        n_item = 1 if not n_items else n_items

        month_offset = n_item * (r_finish // limited)
        time_now = datetime.now()
        start_back = time_now - pd.DateOffset(months=month_offset)

        starting_date = start_back.date()
        ending_date = time_now.date()
        month_dates = get_dates(starting_date, ending_date)

        n = 0
        init = 1
        while n < r_finish and bool(month_dates):
            dates = month_dates[0]
            m_first_date, m_last_date = dates
            month_dates.remove(dates)

            from_data = str(m_first_date.date())
            from_date = m_first_date.strftime("%m/%d/%Y")
            to_data = str(m_last_date.date())
            to_date = m_last_date.strftime("%m/%d/%Y")

            params = "&fromData={}&from={}&toData={}&to={}".format(from_data, from_date, to_data, to_date)
            search_link = "https://www.law.com/dailyreportonline/public-notices/?atex-class=FDR-30102&keyword={}".format(params)

            if n and n < r_finish:
                wait_sec = h.wait_time()
                h.print_log("\nWaiting {} seconds...".format(wait_sec))
                time.sleep(wait_sec)

            h.print_log("-" * 80)
            h.print_log('Loading # {}: "{}"'.format(init, search_link))
            driver.get(search_link)

            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "hp-events")))
                init += 1
            except TimeoutException:
                h.print_log("No Search Result Found")
                break

            h.print_log("Parsing with Notice From {} to {}".format(from_data, to_data))
            page_html = driver.page_source
            page_soup = soup(page_html, "html.parser")

            all_events = page_soup.find_all('div', {'class': 'hp-events'})
            for an_event in all_events:
                all_li = an_event.find_all('li', {'class': 'announcement-item'})
                for li_tag in all_li:
                    tag_date = li_tag.find('div', {'class': 'dbr-date'})
                    notice_tag = tag_date.find_next_sibling()

                    post_data = get_Notice(notice_tag, state, publisher)
                    all_notices.append(post_data)
            n = len(all_notices)
            # h.print_log("Found {} Record(s)".format(n))

        driver.quit()
        h.print_log("\nBrowser Closed.")

        all_notices = h.update_logger(testing, database, source, date_now, limited, r_starts, r_finish, n, all_notices, False)
    return all_notices

def main(param):
    h.print_log("--Starts--")
    starts = time.time()
    limit = param['limit']
    dev = param['env']
    parse = True

    State = "GA"
    publish = "LAW.COM"
    db_name = "Fulton"

    try:
        db = Mysql(dev)
        db.Connect_db(True)
    except:
        parse = False
        h.print_log("Unable to Connect Database Connected.", True)

    if parse:
        scrapped = search_pages(limit, State, publish, db, db_name)
        if bool(scrapped):
            df = pd.DataFrame(scrapped)
            df.dropna(subset='Notice', inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.fillna(value='', inplace=True)

            h.print_log("\nWorking on {:,} rows with {} columns".format(*df.shape))
            df['Parse'] = False
            for index, row in df.iterrows():
                street, city = row['Street'], row['City']
                if bool(street) and bool(city):
                    df_address = df.loc[(df['Street'] == street) & (df['City'] == city), :]
                    if df_address.shape[0] > 1:
                        index_latest = df_address.sort_values(by='Date_Added', ascending=False).index[0]
                        df.at[index_latest, 'Parse'] = True
                    else:
                        df.at[index, 'Parse'] = True
                else:
                    notice = row['Notice']
                    df_notices = df.loc[df['Notice'] == notice, :]
                    if df_notices.shape[0] > 1:
                        index_latest = df_notices.sort_values(by='Date_Added', ascending=False).index[0]
                        df.at[index_latest, 'Parse'] = True
                    else:
                        df.at[index, 'Parse'] = True

            df_parse = df.loc[df['Parse'], df.columns].copy()
            df_parse.drop(columns='Parse', inplace=True)

            all_data = df_parse.to_dict(orient="records")

            db.update_rows(db_name, all_data)

        db.Close_db()

    h.print_log("\n--Finish--")
    ends = time.time()
    elapsed = h.time_elapsed_str(starts, ends)
    h.print_log(elapsed)

if __name__ == '__main__':
    args = dict(limit=10, env=True)
    dev = args['env']
    main(args)
