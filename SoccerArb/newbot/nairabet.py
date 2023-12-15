from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes

def api_calls_events(code):
    url = f"https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId={code}&limit=20"

    payload = {}
    headers = {
        'authority': 'sports-api.nairabet.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.nairabet.com',
        'referer': 'https://www.nairabet.com/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    try:
        return response['data']['categories'][0]['competitions'][0]['events']
    except:
        return None
def api_call_odds(match_id):
    url = f"https://sports-api.nairabet.com/v2/events/{match_id}?country=NG&locale=en&group=g3&platform=desktop"

    payload = {}
    headers = {
        'authority': 'sports-api.nairabet.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.nairabet.com',
        'referer': 'https://www.nairabet.com/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response['marketGroups']


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

    games['match_id'] = match['id']
    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)


    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match['eventNames'][0], match['eventNames'][0])
    games['away_team'] = team_mapping.get(match['eventNames'][-1], match['eventNames'][-1])
    games['time'] = match['startTime']

    odds_market = api_call_odds(match['id'])
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    for marketgroup in odds_market:
        if (marketgroup['name'] == 'Main'):
            markets = marketgroup['markets']
            for market in markets:
                if (market['name'] == "1x2"):
                    home_odd = float(market['outcomes'][0]['value'])
                    draw_odd = float(market['outcomes'][1]['value'])
                    away_odd = float(market['outcomes'][2]['value'])

                if (market['name'] == "Draw No Bet" and len(market['outcomes']) == 2):
                    draw_no_bet.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))

                if (market['name'] == "Double Chance" and len(market['outcomes']) == 3):
                    double_chance.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value']),
                               float(market['outcomes'][2]['value'])))

                if market['entityName'] == "Total Goals - Total Goals 1.5" and (league == "England-Premier League" or league == "England-EFL Cup" or league == "England-League One" or league == "Scotland-Premiership" or league == "England-League Two"):
                    over_one_five_o = float(market['outcomes'][1]['value'])
                    over_one_five_u = float(market['outcomes'][0]['value'])

                if market['entityName'] == "Total Goals - Total Goals 2.5" and (league == "England-Premier League" or league == "England-EFL Cup" or league == "England-League One" or league == "Scotland-Premiership" or league == "England-League Two"):
                    over_two_five_o = float(market['outcomes'][1]['value'])
                    over_two_five_u = float(market['outcomes'][0]['value'])

                if market['entityName'] == "Total Goals - Total Goals 3.5" and (league == "England-Premier League" or league == "England-EFL Cup" or league == "England-League One" or league == "Scotland-Premiership" or league == "England-League Two"):
                    over_three_five_o = float(market['outcomes'][1]['value'])
                    over_three_five_u = float(market['outcomes'][0]['value'])

                if market['name'] == "Total Goals - Over/Under" and (league == "Scotland-Championship" or league == "Scotland-League One" or league == "Scotland-League Two"):
                    outcomes = market['outcomes']
                    for name in outcomes:
                        if name['name'] == "Over 1.5":
                            over_one_five_o = float(name['value'])
                        if name['name'] == "Under 1.5":
                            over_one_five_u = float(name['value'])
                        if name['name'] == "Over 2.5":
                            over_two_five_o = float(name['value'])
                        if name['name'] == "Under 2.5":
                            over_two_five_u = float(name['value'])
                        if name['name'] == "Over 3.5":
                            over_three_five_o = float(name['value'])
                        if name['name'] == "Under 3.5":
                            over_three_five_u = float(name['value'])

                if market['name'] == "Both Teams to Score":
                    ggno = float(market['outcomes'][0]['value'])
                    ggyes = float(market['outcomes'][-1]['value'])

        if (marketgroup['name'] == '1st Half'):
            markets2 = marketgroup['markets']
            for market in markets2:
                if (market['entityName'] == "First Half Result" and len(market['outcomes']) == 3):
                    fasthalf1X2.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value']),
                               float(market['outcomes'][2]['value'])))


    home_draw_away = [home_odd, draw_odd, away_odd]
    handicap1 = []  # -1.5 / 1.5
    over_one_five = [over_one_five_o, over_one_five_u]
    over_two_five = [over_two_five_o, over_two_five_u]
    over_three_five = [over_three_five_o, over_three_five_u]
    gg = [ggyes, ggno]
    away2_home1X = [away_odd, double_chance[0]]
    home1_awayX2 = [home_odd, double_chance[2]]
    X_away12 = [draw_odd, double_chance[1]]

    wager_types.append({"1X2": home_draw_away})
    wager_types.append({"draw_no_bet": draw_no_bet})
    wager_types.append({"double_chance": double_chance})
    wager_types.append({"over_one_five": over_one_five})
    wager_types.append({"over_two_five": over_two_five})
    wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"fasthalf1X2": fasthalf1X2})
    wager_types.append({"gg": gg})
    wager_types.append({"21X": away2_home1X})
    wager_types.append({"12X": home1_awayX2})
    wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        home_team = match_detail['eventNames'][0]
        away_team = match_detail['eventNames'][-1]

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
    bookie_name = 'nairabet'


    leagues = [
        {"England Premier League": "EN_PR"},
        {"England Championship": "EN_D1"},
        {"England League One": "EN_D2"},
        {"England League Two": "EN_D3"},
        {"Scotland Premiership": "LD_SP"},
        {"Scotland Championship": "SCOTLAND_CHAMPIONSHIP"},
        {"Scotland League One": "SCOTLAND_LEAGUE_ONE"},
        {"Scotland League Two": "SCOTLAND_LEAGUE_TWO"}
    ]
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
            print("nairabet", bookmaker_data)
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

