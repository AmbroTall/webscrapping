# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:36:21 2018

@author: Asad Mehmood
"""

from db import Mysql
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import os
import random
import logging
import helper as h
from datetime import datetime
import pandas as pd

global dev
dev = False
# dev = True

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

# Current Directory
current_directory = os.getcwd()

def init_driver():
    driver_dir = os.path.join(current_directory, 'drivers')
    options = Options()
    if not dev:
        options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    if not dev:
        options.add_argument('--headless')

    chrome_exe = "chromedriver.exe"
    # path = '/home/ambrose/Documents/chromedriver'
    try:
        path_to_driver = os.path.join(driver_dir, chrome_exe)
        browser = webdriver.Chrome(options=options)
    except:
        path_to_driver = os.path.join(driver_dir, chrome_exe.replace(".exe", ""))
        browser = webdriver.Chrome(options=options)
    if dev:
        browser.set_window_size(1300, 1000)
    return browser

def wait_loader(driver):
    loader_id = "ctl00_ContentPlaceHolder1_UpdateProgress1"
    waits = True
    h.print_log("Loading...")
    while waits:
        try:
            ww = random.randint(2, 5)
            WebDriverWait(driver, ww).until(EC.presence_of_element_located((By.XPATH, '//div[@id="{}" and @aria-hidden="false"]'.format(loader_id))))
        except:
            pass
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="{}" and @aria-hidden="true"]'.format(loader_id))))
            waits = False
        except:
            waits = True

def get_all_pages(link, driver, limited, database, source, env):
    pages = list()
    web_data = list()

    h.print_log("Page Loaded...")
    keyword_field = WebDriverWait(driver, 30).until(lambda x: x.find_element(By.ID,'ctl00_ContentPlaceHolder1_as1_txtSearch'))
    keyword_field.send_keys('fore')
    w = random.randint(2, 5)
    time.sleep(w)
    keyword_field.send_keys('closure\n')

    select_tag = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage")))
    select_PerPage = Select(select_tag)

    options = select_tag.find_elements(By.TAG_NAME,"option")
    all_options = [opt.get_property("value") for opt in options]
    num_str = all_options[-1]
    w = random.randint(1, 3)
    time.sleep(w)
    select_PerPage.select_by_value(num_str)
    wait_loader(driver)

    try:
        search_grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
        w = h.wait_time()
        h.print_log("\nWaiting {} seconds for Search Grid...".format(w))
        time.sleep(w)
    except:
        search_grid = None
        pass

    if bool(search_grid):
        page_current = 0
        num_records = 0

        testing = False
        # # Get loggers information
        date_now, r_starts, r_finish = h.start_logger(testing, limited, database, source)

        curr_tot_tag = WebDriverWait(search_grid, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblTotalPages")))
        current_total_str = curr_tot_tag.text.strip()
        page_last = int(current_total_str.split()[1])
        h.print_log("There are {} Total Search Pages...\n".format(page_last))

        while not page_current == page_last:
            curr_tag = WebDriverWait(search_grid, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblCurrentPage")))
            page_current = int(curr_tag.text)
            h.print_log("Working on Page # {}".format(page_current))

            WebDriverWait(search_grid, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")))
            button_list = search_grid.find_elements(By.XPATH,"//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")


            for x in range(1, len(button_list) + 1):
                h.print_log("-" * 40)
                h.print_log("Row # {}".format(x))

                page_url = driver.current_url

                an_id = 2 + x
                if an_id < 10:
                    an_id = f'0{an_id}'

                t = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
		                (By.XPATH,f'//*[@id="ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl{an_id}_btnView2"]')
	                )
                )

                WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
                        (By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblTotalPages")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView();", t)
                t.click()

                has_data = False
                try:
                    driver, data = get_data(driver, 'GA')
                    web_data.append(data)
                    has_data = True
                except:
                    h.print_log("Cannot Parse: {}".format(page_url), True)

                has_data = False
                if has_data:
                    try:
                        database.gapub(data)
                    except:
                        h.print_log("Unable to insert: {}".format(page_url), True)

                back = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBodyTop"]')
                    )
                )
                back.click()
                num_records = len(web_data)
                if num_records >= limited:
                    break

            if not env and num_records >= limited:
                break

            if page_current == page_last:
                break

            next_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_btnNext")))
            h.print_log("Click Next Page...")
            next_button.click()

            wait_loader(driver)

            search_grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
            w = h.wait_time()
            h.print_log("-" * 80)
            h.print_log("Waiting {} seconds for Search Grid...".format(w))
            time.sleep(w)

        pages = h.update_logger(testing, database, source, date_now, limited, r_starts, r_finish, num_records, pages, False)

    return driver, web_data

def get_data(driver, state_name):
    url = driver.current_url
    w = h.wait_time()
    h.print_log("Waiting for {} seconds...".format(w))
    time.sleep(w)

    move = False
    try:
        # Resolving recapture
        sitekey = driver.find_element(By.XPATH, '//*[@id="recaptcha"]').get_attribute('outerHTML')
        sitekey_clean = sitekey.split('" id')[0].split('data-sitekey="')[1]
        h.print_log("Solving Recaptcha: '{}'".format(sitekey_clean))
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key('dd32a7594766a876e1a80ebcdf16f840')
        solver.set_website_url(url)
        solver.set_website_key(sitekey_clean)

        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            h.print_log("G_Response = {}".format(g_response))
        else:
            h.print_log("Task finished with error: {}".format(solver.error_code))

        driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

        driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""",
            g_response)
        driver.execute_script(
            'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
        move = True

        btn = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice"]')
        btn.click()
    except NoSuchElementException:
        h.print_log("Recaptcha did not appear we can move")
        move = True

    except Exception as e:
        error_str = "{}: {}".format(str(type(e).__name__), str(e))
        h.print_log(error_str)
        move = False

    web_scrape = dict()
    if move:
        w = random.randint(2, 5)
        h.print_log("Waiting for {} seconds...".format(w))
        time.sleep(w)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content-sub")))

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName")))
        pub_tag = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName")
        publisher = pub_tag.text.strip()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_pnlNoticeContent")))
        pub_notice_tag = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_pnlNoticeContent")
        text_tag = pub_notice_tag.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblContentText")
        notice = text_tag.text.strip()

        the_ID = url.split('=')[-1]
        web_scrape = h.parse_Address(notice, the_ID, state_name, publisher)
        time_dict = {'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        web_scrape.update(time_dict)

        if dev:
            for k, val in web_scrape.copy().items():
                if k == 'Notice':
                    continue
                if isinstance(val, str):
                    web_scrape[k] = val.strip()
                    h.print_log("'{}': '{}'".format(k, val.strip()))
                else:
                    h.print_log("'{}': {}".format(k, val))

    return driver, web_scrape

def main(param):
    h.print_log("--Starts--")
    starts = time.time()

    limit = param['limit']
    dev = param['env']
    prod = param['prod']
    parse = True
    db_name = "GaPub"

    if limit >= 200:
        prod = True

    site_link = "https://www.georgiapublicnotice.com/"

    h.print_log("Initializing webdriver...")
    browser = init_driver()
    h.print_log('Loading: "{}"'.format(site_link))
    browser.get(site_link)

    try:
        db = Mysql(dev)
        db.Connect_db(True)
    except:
        parse = False
        h.print_log("Unable to Connect Database Connected.", True)

    if parse:
        browser, all_notices = get_all_pages(site_link, browser, limit, db, db_name, prod)
        if bool(all_notices):
            df = pd.DataFrame(all_notices)
            df.dropna(subset=['Notice'], inplace=True)
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

    browser.quit()
    h.print_log("\nBrowser Closed.")

    ends = time.time()
    h.print_log("--Finish--")
    elapsed = h.time_elapsed_str(starts, ends)
    h.print_log(elapsed)

if __name__ == '__main__':
    args = dict(limit=2000, env=True, prod=False)
    dev = args['env']
    main(args)