import json
import time

from SoccerArb.newbot.utils import map_teams, testing_function,request_function, converting_time_string



def api_calls_events(code):
    url = f"https://www.merrybet.com/rest/market/categories/multi/{code}/events"

    payload = {}
    headers = {
        'authority': 'www.merrybet.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=utf-8',
        'cookie': 'lsn=web3; smuuid=18b82b201a2-d9af52be717e-3f5cb093-a309ab8f-4db0b2ed-d5a43d14650f; Language=en; _fw_crm_v=242840fe-2d6d-474a-f6ef-998b0a7d1757; _fbp=fb.1.1698704790415.264628022; _gid=GA1.2.525981970.1699616949; smvr=eyJ2aXNpdHMiOjUsInZpZXdzIjoxMiwidHMiOjE2OTk2MTY5NTExMjksIm51bWJlck9mUmVqZWN0aW9uQnV0dG9uQ2xpY2siOjAsImlzTmV3U2Vzc2lvbiI6ZmFsc2V9; _sp_srt_id.0da9=95a20563-45cb-4d46-9f33-ebe86e1f61f0.1698704784.4.1699616952.1699436716.73f0a011-f99b-4544-a8a7-88ee9e9f0323.50ed84e5-6439-49c6-8c9e-2541218ef9e5...0; _smvs=DIRECT; X-ODDS-SESSION=fdbbe690-481c-4695-b4f0-0f719d8ec4d7.oddsapi4; _ga_N4Z80CV99E=GS1.1.1699632525.6.1.1699632536.49.0.0; _ga=GA1.1.195919543.1698704786',
        'referer': 'https://www.merrybet.com/sports/events/Soccer/1060/1',
        'request-language': 'en',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-odds-session': 'fdbbe690-481c-4695-b4f0-0f719d8ec4d7.oddsapi4',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = request_function(url, headers, payload)
    return response['data']

def api_call_odds(match_id):
    url = f"https://www.merrybet.com/rest/market/events/{match_id}"

    payload = {}
    headers = {
        'authority': 'www.merrybet.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json; charset=utf-8',
        'cookie': 'lsn=web3; smuuid=18b82b201a2-d9af52be717e-3f5cb093-a309ab8f-4db0b2ed-d5a43d14650f; Language=en; _fw_crm_v=242840fe-2d6d-474a-f6ef-998b0a7d1757; _fbp=fb.1.1698704790415.264628022; _gid=GA1.2.525981970.1699616949; smvr=eyJ2aXNpdHMiOjUsInZpZXdzIjoxMiwidHMiOjE2OTk2MTY5NTExMjksIm51bWJlck9mUmVqZWN0aW9uQnV0dG9uQ2xpY2siOjAsImlzTmV3U2Vzc2lvbiI6ZmFsc2V9; _sp_srt_id.0da9=95a20563-45cb-4d46-9f33-ebe86e1f61f0.1698704784.4.1699616952.1699436716.73f0a011-f99b-4544-a8a7-88ee9e9f0323.50ed84e5-6439-49c6-8c9e-2541218ef9e5...0; _smvs=DIRECT; X-ODDS-SESSION=fdbbe690-481c-4695-b4f0-0f719d8ec4d7.oddsapi4; _ga_N4Z80CV99E=GS1.1.1699632525.6.1.1699632536.49.0.0; _ga=GA1.1.195919543.1698704786',
        'referer': 'https://www.merrybet.com/sports/events/Soccer/1060/1',
        'request-language': 'en',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-odds-session': 'fdbbe690-481c-4695-b4f0-0f719d8ec4d7.oddsapi4',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = request_function(url, headers, payload)
    return response['data']['eventGames']

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
    name = match['eventName'].split(" - ")

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(name[0].strip(), name[0].strip())
    games['away_team'] = team_mapping.get(name[1].strip(), name[1].strip())

    games['time'] = match['eventStart']

    #Odds
    eventgames = api_call_odds(match['eventId'])

    home_odd = float(eventgames[0]['outcomes'][0]['outcomeOdds'])
    away_odd = float(eventgames[0]['outcomes'][2]['outcomeOdds'])
    draw_odd = float(eventgames[0]['outcomes'][1]['outcomeOdds'])
    home_draw_away = [home_odd, draw_odd, away_odd]
    wager_types.append({"1X2": home_draw_away})

    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    for eventgame in eventgames:
        if (eventgame['gameName'] == "Double chance"):
            double_chance.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 2.5 goals"):
            over_two_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 1.5 goals"):
            over_one_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 3.5 goals"):
            over_three_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Draw no bet"):
            draw_no_bet.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "1st half - 1x2"):
            fasthalf1X2.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))
        if (eventgame['gameName'] == "Both teams to score"):
            gg.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

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
        name = match_detail['eventName'].split(" - ")
        home_team = name[0].strip()
        away_team = name[1].strip()

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
    bookie_name = 'merrybet'
    # leagues = [{"England Premier League": 1060} ]
    leagues = [{"England Premier League": 1060},{"England Championship": 352}, {"England League One": 1088}, {"England League Two": 1090}, {"Scotland Premiership": 1091}, {"Scotland Championship":1092}, {"Scotland League One":1093}, {"Scotland League Two":1094} ]

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
                    # Filtering out unwanted matched from this bookie
                    # if "Home Teams vs Away Teams" in match['eventName']:
                    #     continue
                    league_wager_dic =  exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)

            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("merrybet", bookmaker_data)
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
