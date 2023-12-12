from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes

def api_calls_events(code):
    url = f"https://www.ps3838.com/sports-service/sv/search/odds?_g=1&btg=1&c=&cl=3&d=&ec=&ev=&g=&hle=true&l=3&lg={code}&lv=&mk=3&more=false&o=1&ot=1&pa=0&pimo=0%2C1%2C8%2C39%2C3%2C6%2C7%2C4%2C5&pn=-1&sp=29&tm=0&v=0&wm=&locale=en_US&_=1700750630496&withCredentials=true"

    payload = {}
    headers = {
        'authority': 'www.ps3838.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'skin=ps3838; _sig=Bcy1NVFJqTTJZME9EVmpOV1F3WmpjMFpBOm8xamtTY0JLSlljTTRpNjdsaWtQMml6Vno6LTcwNTI4NjA1ODo2OTg4NDM5MDk6bm9uZTpXb2U1NlZ6M3Uw; dxaI8=3Qn; _cfuvid=FSUb_JdbgvuUcwibNS8U5fF25DKky5nBOaNQL1FVX54-1700648994911-0-604800000; _gid=GA1.2.1117177808.1700649007; lang=en_US; _vid=fa46d547df8036788fb95f1d4c816238; _ga_DXNRHBHDY9=GS1.1.1700750506.11.1.1700750522.44.0.0; _ga_1YEJQEHQ55=GS1.1.1700750506.11.1.1700750522.44.0.0; _ga=GA1.2.1519450307.1698843901',
        'referer': 'https://www.ps3838.com/en/search/england-premier-league',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    try:
        return response['el'][0][2][0][2]
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
    gg = []

    games['match_id'] = match[0]
    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)


    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match[1], match[1])
    games['away_team'] = team_mapping.get(match[2], match[2])
    games['time'] = match[4]

    home_away_draw = match[8]['0'][-10]
    away = home_away_draw[0]
    home = home_away_draw[1]
    draw = home_away_draw[2]
    home_draw_away = [home, draw, away]

    fast1X2 = match[8]['1'][-10]
    away1 = fast1X2[0]
    home1 = fast1X2[1]
    draw1 = fast1X2[2]
    fasthalf1X2 = [home1,draw1,away1]


    # odds_market = api_call_odds(match[0])
    # print(odds_market)

    handicap1 = []  # -1.5 / 1.5
    # over_one_five = [over_one_five_o, over_one_five_u]
    # over_two_five = [over_two_five_o, over_two_five_u]
    # over_three_five = [over_three_five_o, over_three_five_u]
    # gg = [ggyes, ggno]
    # away2_home1X = [away_odd, double_chance[0]]
    # home1_awayX2 = [home_odd, double_chance[2]]
    # X_away12 = [draw_odd, double_chance[1]]

    wager_types.append({"1X2": home_draw_away})
    # wager_types.append({"draw_no_bet": draw_no_bet})
    # wager_types.append({"double_chance": double_chance})
    # wager_types.append({"over_one_five": over_one_five})
    # wager_types.append({"over_two_five": over_two_five})
    # wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"fasthalf1X2": fasthalf1X2})
    # wager_types.append({"gg": gg})
    # wager_types.append({"21X": away2_home1X})
    # wager_types.append({"12X": home1_awayX2})
    # wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        home_team = match_detail[0]
        away_team = match_detail[1]

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
    bookie_name = 'ps3838'


    leagues = [
        {"England Premier League": 1980},
        {"England Championship": 1977},
        {"England League One": 1957},
        {"England League Two": 1958},
        {"Scotland Premiership": 2421},
        {"Scotland Championship": 2417},
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

