import json
import time

from SoccerArb.newbot.utils import map_teams, testing_function,request_function, converting_time_string



def api_calls_events(code):
    url = f"https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/{code}/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1699627900080&useCombined=true&useCombinedLive=true"

    payload = {}
    headers = {
        'authority': 'eu-offering-api.kambicdn.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.sunbet.co.za',
        'referer': 'https://www.sunbet.co.za/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = request_function(url, headers, payload)
    return response['events']

def api_call_odds(match_id):
    url = f"https://eu-offering-api.kambicdn.com/offering/v2018/siwc/betoffer/event/{match_id}.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1699630296819&includeParticipants=true"

    payload = {}
    headers = {
        'authority': 'eu-offering-api.kambicdn.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.sunbet.co.za',
        'referer': 'https://www.sunbet.co.za/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response['betOffers']

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

    games['match_id'] = match['event']['id']
    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match['event']['homeName'], match['event']['homeName'])
    games['away_team'] = team_mapping.get(match['event']['awayName'], match['event']['awayName'])

    games['time'] = converting_time_string(match['event']['start'])

    odds_market = api_call_odds(match['event']['id'])

    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    for market in odds_market:
        if (market['criterion']['label'] == "Full Time"):
            home_odd = float(market['outcomes'][0]['odds']) / 1000
            away_odd = float(market['outcomes'][2]['odds']) / 1000
            draw_odd = float(market['outcomes'][1]['odds']) / 1000
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if (market['criterion']['label'] == "Double Chance"):
            double_chance.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000))

        if (market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 2500):
            over_two_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))

        if (market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 1500):
            over_one_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))

        if (market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 3500):
            over_three_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))

        if (market['criterion']['label'] == "Draw No Bet"):
            draw_no_bet.extend((market['outcomes'][0]['odds'] / 1000, market['outcomes'][1]['odds'] / 1000))

        if (market['criterion']['label'] == "Half Time"):
            fasthalf1X2.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000,  float(market['outcomes'][2]['odds'])/1000))

        if (market['criterion']['label'] == "Both Teams To Score"):
            gg.extend((float(market['outcomes'][0]['odds']) / 1000, float(market['outcomes'][1]['odds']) / 1000))

    wager_types.append({"draw_no_bet": draw_no_bet})
    wager_types.append({"double_chance": double_chance})
    wager_types.append({"over_one_five": over_one_five})
    wager_types.append({"over_two_five": over_two_five})
    wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"fasthalf1X2": fasthalf1X2})
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
    wager_types.append({"gg": gg})

    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match dbookies_oddsetails
    team_names_from_matches = set()

    for match_detail in match_details:
        home_team = match_detail['event']['homeName']
        away_team = match_detail['event']['awayName']

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
    bookie_name = 'sunbet'
    # leagues = [{"England Premier League": "england/premier_league"} ]
    leagues = [{"England Premier League": "england/premier_league"},{"England Championship": "england/the_championship"}, {"England League One": "england/league_one"}, {"England League Two": "england/league_two"}, {"Scotland Premiership": "scotland/scottish_premiership"}, {"Scotland Championship":"scotland/championship"}, {"Scotland League One":"scotland/league_one"}, {"Scotland League Two":"scotland/league_two"} ]

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
            print("sunbet", bookmaker_data)
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
