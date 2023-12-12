import json
import os

import pytz
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

def get_jwt():
    while True:
        try:
            # Create a new instance of the Chrome driver (you can use other browsers as well)
            # Set up Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            # Navigate to the desired webpage
            driver.get("https://sports.sbk-188bet.com/en-gb/sports/?c=22&u=https://www.188bet.com")
            time.sleep(3)
            # Execute JavaScript to get the JWT token from session storage
            jwt_token = driver.execute_script("return window.sessionStorage.getItem('JWT');")
            if jwt_token is not None:
                print("Driver", jwt_token)
                driver.quit()
                return jwt_token
            else:
                driver.quit()
                continue
        except:
            print("Jwt Restarting")
            continue
def api_calls_events(code, jwt):
    url = f"https://landing-sports-api.sbk-188bet.com/api/v2/en-gb/ROW/sport/1/mop/competition/{code}/premium"
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {jwt}',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'sb-188cshapilv=1210846986.20480.0000',
        'DeviceType': 'Web',
        'Origin': 'https://sports.sbk-188bet.com',
        'Referer': 'https://sports.sbk-188bet.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'SessionID': '2c2cede2-e176-4836-bfd0-cce48c9af84e',
        'TabId': '844948',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }


    response = request_function(url, headers, payload)

    try:
        return response['d']['s']['c'][0]['e']
    except:
        return None

def api_call_odds(match_id, jwt):
    url = f"https://landing-sports-api.sbk-188bet.com/api/v2/en-gb/ROW/parlay/event/{match_id}"

    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {jwt}',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'sb-188cshapilv=1261178634.20480.0000',
        'DeviceType': 'Web',
        'Origin': 'https://sports.sbk-188bet.com',
        'Referer': 'https://sports.sbk-188bet.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'SessionID': '2c2cede2-e176-4836-bfd0-cce48c9af84e',
        'TabId': '46323',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    response = request_function(url, headers, payload)
    return response['d']['e']['ml']

def exctract_odds(match, league, bookie_name, jwt):
    games = {}

    wager_types = []
    draw_no_bet = []
    handicap1 = [] # -1.5 / 1.5


    draw_no_bet_first_half = []
    fasthalf_dc = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_four_five = []
    over_five_five = []
    gg_firsthalf = []
    odd_even = []
    odd_even_firsthalf = []
    first_team_to_score = []  # hometeam, draw, away_team
    first_team_to_score_first_half = []  # hometeam, draw, away_team
    home_team_overunder15 = []
    home_team_overunder25 = []
    home_team_overunder05 = []
    away_team_overunder15 = []
    away_team_overunder25 = []
    away_team_overunder05 = []

    games['match_id'] = match['id']

    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)


    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match['h'], match['h'])
    games['away_team'] = team_mapping.get(match['a'], match['a'])

    games['time'] = match['edt']

    odds_market = api_call_odds(match['id'], jwt)
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    for market in odds_market:
        if market['t'] == "FT_1X2" and market['n'] == "1 X 2":
            home_odd = market['o'][0]['v']
            draw_odd = market['o'][2]['v']
            away_odd = market['o'][1]['v']
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if market['t'] == "HT_1X2" and market['n'] == "1 X 2 - 1st Half":
            home_odd1 = market['o'][0]['v']
            draw_odd2 = market['o'][2]['v']
            away_odd3 = market['o'][1]['v']
            fasthalf1X2 = [home_odd1, draw_odd2, away_odd3]
            wager_types.append({"fasthalf1X2": fasthalf1X2})

        if market['t'] == "BothTeamsToScore" and market['n'] == "Both Teams to Score":
            ggyes = market['o'][0]['v']
            ggno = market['o'][1]['v']
            gg = [ggyes, ggno]
            wager_types.append({"gg": gg})

        if market['t'] == "DoubleChance" and market['n'] == "Double Chance":
            dnbhome = market['o'][0]['v']
            dnbdraw = market['o'][2]['v']
            dnbaway = market['o'][1]['v']
            double_chance = [dnbhome, dnbdraw, dnbaway]
            wager_types.append({"double_chance": double_chance})

        if market['t'] == "FT_OU_1p5" and market['n'] == "Total Goals - Over / Under 1.5":
            over15 = market['o'][0]['v']
            under15 = market['o'][1]['v']
            over_one_five = [over15, under15]
            wager_types.append({"over_one_five": over_one_five})

    handicap1 = []  # -1.5 / 1.5
    # away2_home1X = [wager_types[0]['1X2'][2], double_chance[0]]
    # home1_awayX2 = [wager_types[0]['1X2'][0], double_chance[2]]
    # X_away12 = [wager_types[0]['1X2'][1], double_chance[1]]
    #
    # wager_types.append({"21X": away2_home1X})
    # wager_types.append({"12X": home1_awayX2})
    # wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    print("ambrose")
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        home_team = match_detail['h']
        away_team = match_detail['a']

        if home_team and isinstance(home_team, str):
            team_names_from_matches.add(home_team.strip())
        if away_team and isinstance(away_team, str):
            team_names_from_matches.add(away_team.strip())

    # Filter out non-string items from the team_names list
    team_names = [team.strip() for team in team_names if isinstance(team, str)]
    # Check if all team names are present in the extracted names
    missing_teams = [team for team in team_names if team not in team_names_from_matches]
    return missing_teams


def process_league(league_dict):
    for league_name, league_id in league_dict.items():
        return  league_name, league_id

def generate_date_params():
    # Get today's date
    today = datetime.now().date()

    # Calculate the end date (today + 3 weeks)
    end_date = today + timedelta(weeks=3)

    # Format the dates as strings in the desired format
    start_date_str = today.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return {"start_date": start_date_str, "end_date": end_date_str}

# Function to save JWT to a file
def save_jwt_to_file(token, file_path='jwt_token.txt'):
    with open(file_path, 'w') as file:
        file.write(json.dumps(token))

# Function to load JWT from a file
def load_jwt_from_file(file_path='jwt_token.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return None
def main():
    bookie_name = 'bet188'
    # Check if JWT exists in the file
    jwt_token = load_jwt_from_file()
    if jwt_token is None:
        # If JWT is not available, obtain it and save it to the file
        jwt_token = get_jwt()
        save_jwt_to_file(jwt_token)

    leagues = [
        {"England Premier League": 26726},
        {"England Championship": 26326},
        {"England League One": 27325},
        {"England League Two": 26470},
        {"Scotland Premiership": 29042},
        {"Scotland Championship": 23420},
        {"Scotland League One": 25530},
        {"Scotland League Two": 25531}
    ]
    bookmaker_data = []
    for league in leagues:
        try:
            print(league)
            league_name, league_id = process_league(league)
            match_details = api_calls_events(f"{league_id}", jwt_token)

            league_mapping = {
                "England Premier League": "England-Premier League",
                "England Championship": "England-EFL Cup",
                "England League One": "England-League One",
                "England League Two": "England-League Two",
                "Scotland Premiership": "Scotland-Premiership",
                "Scotland Championship": "Scotland-Championship",
                "Scotland League One": "Scotland-League One",
                "Scotland League Two": "Scotland-League Two",
            }
            # Check if the league_name is in the mapping dictionary, if yes, update it
            if league_name in league_mapping:
                league_name = league_mapping[league_name]

            # Testing Function To See if teams are correctly named
            testing = testing_function(bookie_name, league_name)
            missing_names = check_team_names_in_match_details(testing, match_details)
            print("**** This are the missing matches", missing_names)

            liga = {}
            league_data = []

            for match in match_details:
                try:
                    league_wager_dic =  exctract_odds(match, league_name, bookie_name, jwt_token)
                    league_data.append(league_wager_dic)
                except:
                    continue
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("bet188", bookmaker_data)
        except Exception as e:
            print("Ambrose", e)
            continue
    return bookmaker_data

if __name__ == '__main__':
    start_time = time.time()
    games = main()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60

    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)

