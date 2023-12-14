import json

from SoccerArb.newbot.utils import map_teams, testing_function, request_function_post,request_function
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes


def api_calls_events(code):
    url = "https://www.sportybet.com/api/gh/factsCenter/pcEvents"

    payload = json.dumps([
        {
            "sportId": "sr:sport:1",
            "marketId": "1,18,10,29,11,26,36,14",
            "tournamentId": [
                [
                    f"sr:tournament:{code}"
                ]
            ]
        }
    ])
    headers = {
        'authority': 'www.sportybet.com',
        'accept': '*/*',
        'accept-language': 'en',
        'clientid': 'web',
        'content-type': 'application/json',
        'cookie': 'redirect_to_int=1; locale=en; device-id=95fb391a-9399-4636-9640-8a95d84c1294; sb_country=gh; _gcl_au=1.1.288315298.1697995873; sb_fs_id=65f47e60-5ccf-43b1-abec-dca56dbd7a2d; sb_fs_flag=false; _fbp=fb.1.1697995879478.1103147264; _gid=GA1.2.1892397113.1699616927; _gat=1; _ga_HTPQ490VV2=GS1.2.1699616934.5.0.1699616934.60.0.0; _dc_gtm_UA-113009458-1=1; _ga_00HZ52K43N=GS1.1.1699616927.16.1.1699616967.20.0.0; _ga=GA1.2.373478744.1697995878',
        'operid': '3',
        'origin': 'https://www.sportybet.com',
        'platform': 'web',
        'referer': 'https://www.sportybet.com/gh/sport/football/sr:category:1/sr:tournament:17',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = request_function_post(url, headers, payload)
    return response['data'][0]['events']

def api_call_odds(match_id):
    url = f"https://www.sportybet.com/api/gh/factsCenter/event?eventId={match_id}&productId=3&_t=1699620536150"

    payload = {}
    headers = {
        'authority': 'www.sportybet.com',
        'accept': '*/*',
        'accept-language': 'en',
        'clientid': 'web',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'redirect_to_int=1; locale=en; device-id=95fb391a-9399-4636-9640-8a95d84c1294; sb_country=gh; _gcl_au=1.1.288315298.1697995873; sb_fs_id=65f47e60-5ccf-43b1-abec-dca56dbd7a2d; sb_fs_flag=false; _fbp=fb.1.1697995879478.1103147264; _gid=GA1.2.1892397113.1699616927; _ga_HTPQ490VV2=GS1.2.1699616934.5.0.1699616934.60.0.0; _ga=GA1.2.373478744.1697995878; _ga_00HZ52K43N=GS1.1.1699616927.16.1.1699620532.60.0.0',
        'operid': '3',
        'platform': 'web',
        'referer': 'https://www.sportybet.com/gh/sport/football/Scotland/League_2/East_Fife_FC_vs_Dumbarton_FC/sr:match:42025673',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response['data']['markets']


def exctract_odds(match, league, bookie_name):
    games = {}
    wager_types = []
    draw_no_bet = []
    double_chance = []
    handicap1 = [] # -1.5 / 1.5
    over_one_five = []
    over_two_five = []
    over_three_five = []
    fasthalf1X2 = []
    gg = []

    games['match_id'] = match['eventId']
    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match['homeTeamName'], match['homeTeamName'])
    games['away_team'] = team_mapping.get(match['awayTeamName'], match['awayTeamName'])

    games['time'] = match['estimateStartTime']

    odds_market = api_call_odds(match['eventId'])

    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    for market in odds_market:
        if (market['desc'] == "1X2"):
            home_odd = float(market['outcomes'][0]['odds'])
            away_odd = float(market['outcomes'][2]['odds'])
            draw_odd = float(market['outcomes'][1]['odds'])
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if (market['desc'] == "Double Chance"):
            double_chance.extend((float(market['outcomes'][0]['odds']),float(market['outcomes'][1]['odds']), float(market['outcomes'][2]['odds'])))

        if (market['desc'] == "Over/Under" and market['specifier'] == "total=2.5"):
            over_two_five.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))

        if (market['desc'] == "Over/Under" and market['specifier'] == "total=1.5"):
            over_one_five.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))

        if (market['desc'] == "Over/Under" and market['specifier'] == "total=3.5"):
            over_three_five.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))

        if (market['desc'] == "Draw No Bet"):
            draw_no_bet.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))

        if (market['desc'] == "1st Half - 1X2"):
            fasthalf1X2.extend((float(market['outcomes'][0]['odds']),float(market['outcomes'][1]['odds']),  float(market['outcomes'][2]['odds'])))

        if (market['desc'] == "GG/NG"):
            gg.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))

    wager_types.append({"draw_no_bet": draw_no_bet})
    wager_types.append({"double_chance": double_chance})
    wager_types.append({"over_one_five": over_one_five})
    wager_types.append({"over_two_five": over_two_five})
    wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"fasthalf1X2": fasthalf1X2})
    wager_types.append({"gg": gg})
    try:
        for x in wager_types:
            for key, value in x.items():
                if key == "1X2":
                    away_odd = value[-1]
                    home_odd = value[0]
                    draw_odd = value[1]
                if key == "double_chance":
                    double_chance1X = value[0]
                    double_chance12 = value[1]
                    double_chanceX2 = value[2]
        away2_home1X = [away_odd, double_chance1X]
        home1_awayX2 = [home_odd, double_chanceX2]
        X_away12 = [draw_odd, double_chance12]
        wager_types.append({"21X": away2_home1X})
        wager_types.append({"12X": home1_awayX2})
        wager_types.append({"X12": X_away12})
    except:
        pass
    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()

    for match_detail in match_details:
        home_team = match_detail['homeTeamName']
        away_team = match_detail['awayTeamName']

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



def main():
    bookie_name = 'sportybet'
    # leagues = [{"England Premier League": 17} ]
    leagues = [{"England Premier League": 17},{"England Championship": 18}, {"England League One": 24}, {"England League Two": 25}, {"Scotland Premiership": 36}, {"Scotland Championship":206}, {"Scotland League One":207}, {"Scotland League Two":209} ]

    bookmaker_data = []
    for league in leagues:
        try:

            print(league)
            league_name, league_id = process_league(league)
            match_details = api_calls_events(f"{league_id}")

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
                    league_wager_dic =  exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print(bookmaker_data)
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
