# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:56:05 2022

@author: Asad Mehmood
"""

import requests
import time
import helper as h
from db import Mysql
from gwinnett import get_pages, get_Notice
import pandas as pd

global dev
dev = False

def main(param):
    h.print_log("--Starts--")
    starts = time.time()
    limited = param['limit']
    dev = param['env']
    parse = True

    website = "https://www.news-daily.com{}"
    db_name = "Clayton"
    State = "GA"
    publish = "Clayton News-Daily"

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

            h.print_log("Working on {:,} rows with {} columns".format(*df.shape))
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
