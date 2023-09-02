# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:56:05 2022

@author: Asad Mehmood
"""

import requests
import time
from bs4 import BeautifulSoup as soup
# import random
import helper as h
from db import Mysql
import pandas as pd
from datetime import datetime

HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
global dev
dev = False

def read_website_with_requests(url, session=False):
    page = None
    page_url = None
    error_str = None
    try:
        if session:
            r = session.get(url, headers=HEADER, timeout=30)
        else:
            r = requests.get(url, headers=HEADER, timeout=30)
        if r.status_code == 200:
            page = r.text.strip()
            page_url = r.url
    except requests.exceptions.Timeout as errt:
        error_str = "{}: {}".format(str(type(errt).__name__), errt)
    except requests.exceptions.HTTPError as errh:
        error_str = "{}: {}".format(str(type(errh).__name__), errh)
    except requests.exceptions.ConnectionError as errc:
        error_str = "{}: {}".format(str(type(errc).__name__), errc)
    except requests.exceptions.TooManyRedirects as errtm:
        error_str = "{}: {}".format(str(type(errtm).__name__), errtm)
    except requests.exceptions.RequestException as e:
        error_str = "{}: {}".format(str(type(e).__name__), e)
    return page, page_url, error_str

def get_website_total(link, req_session):
    total_return = 0
    page_html, url, error_message = read_website_with_requests(link, req_session)
    h.print_log("\nFetching total records...")
    if not bool(page_html):
        error_url = link if not bool(url) else url
        message = "Page NOT found:\t{}".format(error_url) if not error_message else error_message
        h.print_log(message, True)
    else:
        count_soup = soup(page_html, "html.parser")
        # Total Records in search
        p_tag = count_soup.find('p', {'class': 'results-showing'})
        tag_count = p_tag.find('strong', {'class': 'results-total'})
        str_count = tag_count.text.strip()
        total_return = int(str_count)
    return total_return

def get_pages(web_site, limit, sess, database, source):
    ad_list = list()
    testing = False
    per_page = 100

    search_href = "/classifieds/community/announcements/legal/foreclosure/?l={}&sd=&s=&f=".format(per_page)
    search_link = web_site.format(search_href)

    # Get loggers information
    date_now, r_starts, r_finish = h.start_logger(testing, limit, database, source)
    num_fetch = r_finish

    n = 0
    while n < num_fetch:
        if n and n < num_fetch:
            wait_sec = h.wait_time()
            h.print_log("Waiting {} seconds...".format(wait_sec))
            time.sleep(wait_sec)

        #open website and grab the full page
        h.print_log("-" * 40)
        h.print_log("Reading: '{}'".format(search_link))
        page_html, url, error_message = read_website_with_requests(search_link, sess)
        h.print_log("\nWaiting for results to appear")
        if not bool(page_html):
            error_url = search_link if not bool(url) else url
            message = "Page NOT found:\t{}".format(error_url) if not error_message else error_message
            h.print_log(message, True)
        else:
            page_soup = soup(page_html, "html.parser")

            # Total Records in search
            p_tag = page_soup.find('p', {'class': 'results-showing'})
            tag_count = p_tag.find('strong', {'class': 'results-total'})
            str_count = tag_count.text.strip()
            total_return = int(str_count)

            container = page_soup.find('div', {'id': 'classifieds-results-container'})

            result_tags = container.find_all('article', {'class': 'product'})
            for article_tag in result_tags:
                type_tag = article_tag.find('div', {'class': 'card-labels'})
                post_type = type_tag.text.strip().upper()
                if post_type == 'FORECLOSURE':
                    a_tag = article_tag.h3.a
                    post_url = web_site.format(a_tag['href'])
                    ad_list.append(post_url)

            n = len(ad_list)
            pagination_tag = page_soup.find('ul', {'class': 'pagination'})
            if bool(pagination_tag):
                li_tags = pagination_tag.find_all('li')
                next_tag = li_tags[-1].a
                search_link = next_tag['href']

    ad_list = h.update_logger(testing, database, source, date_now, limit, r_starts, r_finish, total_return, ad_list, False)
    return ad_list

def get_Notice(sess, post, state, publisher):
    web_scrape = dict()
    post_html, url, error_message = read_website_with_requests(post, sess)

    wait_sec = h.wait_time()
    h.print_log("Waiting {} seconds...".format(wait_sec))
    time.sleep(wait_sec)

    if not bool(post_html):
        error_url = post if not bool(url) else url
        message = "Page NOT found:\t{}".format(error_url) if not error_message else error_message
        h.print_log(message, True)
    else:
        post_soup = soup(post_html, "html.parser")
        detail_tag = post_soup.find('section', {'id': 'details'})
        description_tag = detail_tag.find('div', {'itemprop': 'description'})
        notice = description_tag.text.strip()
        post_ID = post.split("/")[-1].replace('.html', '')

        web_scrape = h.parse_Address(notice, post_ID, state, publisher)
        time_dict = {'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        web_scrape.update(time_dict)
        if dev:
            for k, val in web_scrape.items():
                if k == 'Notice':
                    continue
                h.print_log("'{}': '{}'".format(k, val))
    return web_scrape

def main(param):
    h.print_log("--Starts--")
    starts = time.time()
    limited = param['limit']
    dev = param['env']
    parse = True

    website = "https://www.gwinnettdailypost.com{}"
    db_name = "Gwinnett"
    State = "GA"
    publish = "Gwinnett Daily Post"

    try:
        db = Mysql(dev)
        db.Connect_db(True)
    except:
        parse = False
        h.print_log("Unable to Connect Database Connected.", True)

    if parse:
        a_session = requests.Session()

        # Get all Notice urls from Search Pages
        posts = get_pages(website, limited, a_session, db, db_name)

        h.print_log("\nParsing {} Page(s)...".format(len(posts)))
        scrapped = list()
        for i, post_url in enumerate(posts, start=1):
            h.print_log("-" * 40)
            h.print_log("Loading # {}: '{}'".format(i, post_url))
            try:
                post_info = get_Notice(a_session, post_url, State, publish)
                scrapped.append(post_info)
            except Exception as e:
                error_str = "{}: {}".format(str(type(e).__name__), str(e))
                h.print_log("Cannot Parse: {}".format(post_url), True)
                h.print_log(error_str, True)
                post_info = dict()

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
