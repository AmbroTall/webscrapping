import random
import time
from datetime import datetime, timezone

import pytz
import requests
from pytz import timezone
import pandas as pd
from datetime import datetime, timezone


max_requests_per_ip = 5  # Change IP after this number of requests
request_count = 0


countries = ['mk', 'si', 'me', 'rs', 'bg', 'hr']#al
proxies = {
    "http": '',
    "https": '',
    'no_proxy': 'localhost,127.0.0.1'
}
https_proxies = {
    #"http": '',
    "https": '',
    'no_proxy': 'localhost,127.0.0.1'
}
def convert_date_string_to_unix(date_string):
    date_format = '%Y-%m-%d %H:%M:%S'

    # Convert string to datetime object
    dt_object = datetime.strptime(date_string, date_format)

    # Convert datetime object to Unix timestamp
    unix_timestamp = int(dt_object.replace(tzinfo=timezone.utc).timestamp())

    return unix_timestamp

def convert_to_unix_timestamp_utc(input_time):
    # Define the source timezone
    from_zone = timezone('UTC')

    # Convert input_time to a datetime object with the source timezone
    input_time = datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    input_time = from_zone.localize(input_time)

    # Convert the datetime to a Unix timestamp
    unix_timestamp = int(input_time.timestamp())

    return unix_timestamp

def testing_function(bookie_name, league_title):
    excel_file = "/home/ambrose/PycharmProjects/WebScraping/webscrapping/SoccerArb/TeamNames//combined_data.xlsx"  # Provide the path to your Excel file

    # Load the Excel file with all bookie worksheets
    excel_file = pd.ExcelFile(excel_file)

    # Check if the specified bookie worksheet exists
    if bookie_name in excel_file.sheet_names:
        # Read the bookie's worksheet into a DataFrame
        bookie_df = excel_file.parse(bookie_name)

        # Ensure that the league title exists as a column in the bookie DataFrame
        if league_title in bookie_df.columns:
            # Return an array of all team names from the bookie's DataFrame
            return bookie_df[league_title].tolist()
        else:
            return []  # Return an empty list when the league title is not found in the bookie DataFrame
    else:
        return []  # Return an empty list when the bookie worksheet is not found

def map_teams(bookie_name, league_title):
    excel_file = "/home/ambrose/PycharmProjects/WebScraping/webscrapping/SoccerArb/TeamNames//combined_data.xlsx"  # Provide the path to your Excel file

    # Load the Excel file with all bookie worksheets
    excel_file = pd.ExcelFile(excel_file)

    # Check if the specified bookie worksheet exists
    if bookie_name in excel_file.sheet_names:
        # Read the bookie's worksheet into a DataFrame
        bookie_df = excel_file.parse(bookie_name)

        # Read the default worksheet into a DataFrame
        default_df = excel_file.parse('default')

        # Ensure that the league title exists as a column in both DataFrames
        if league_title in bookie_df.columns and league_title in default_df.columns:
            # Create a mapping dictionary from the bookie's team names to default names
            team_mapping = dict(zip(bookie_df[league_title], default_df[league_title]))
            return team_mapping
        else:
            return "League title not found in one or both DataFrames."
    else:
        return "Bookie worksheet not found in the Excel file."


def change_proxy():
    global request_count
    random_country = random.choice(countries)
    proxies['http'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    proxies['https'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    https_proxies['https'] = f'http://phscrapingtest:strongzerocola_country-{random_country}_streaming-1@geo.iproyal.com:12321'
    request_count = 0

def request_function(url, headers, payload, proxy_type = 'mixed'):
    while True:
        try:
            # global request_count
            # if request_count == max_requests_per_ip:
            #     change_proxy()
            #
            # if proxy_type == 'mixed':
            #     proxies_to_use = proxies
            # elif proxy_type == 'https':
            #     proxies_to_use = https_proxies

            # response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies_to_use)
            response = requests.request("GET", url, headers=headers, data=payload)
            # request_count += 1
            # response.raise_for_status()
            r = response.json()
            time.sleep(1)
            if isinstance(r, list) and len(r) == 0:
                return None
            if r:
                return r
        except Exception as e:
            print("Restarting Request Function, Lazima Points Ambrose", e)
def request_function_bs4(url, headers, payload):
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            time.sleep(1)
            if response:
                return response
        except Exception as e:
            print("Restarting Request Function, Lazima Points Ambrose", e)
def request_function_post(url, headers, payload, proxy_type = 'mixed'):
    while True:
        try:
            # global request_count
            # if request_count == max_requests_per_ip:
            #     change_proxy()
            #
            # if proxy_type == 'mixed':
            #     proxies_to_use = proxies
            # elif proxy_type == 'https':
            #     proxies_to_use = https_proxies

            # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies_to_use)
            response = requests.request("POST", url, headers=headers, data=payload)
            # request_count += 1
            # response.raise_for_status()
            r = response.json()
            time.sleep(1)
            if r:
                return r
        except Exception as e:
            print("Restarting Request Function, Lazima Points Ambrose", e)

def converting_time_string(timestamp_string):
    # Convert string to datetime object
    dt_object = datetime.fromisoformat(timestamp_string[:-1]).replace(tzinfo=timezone.utc)  # remove 'Z' for proper conversion
    # Convert datetime object to Unix timestamp
    unix_timestamp = int(dt_object.timestamp())
    return unix_timestamp



