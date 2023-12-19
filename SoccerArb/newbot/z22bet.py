import time

from SoccerArb.newbot.utils import map_teams, testing_function, request_function
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 400  # 2 minutes


def api_calls_events(code):
    url = f"https://22bet.co.ke/LineFeed/Get1x2_VZip?sports=1&champs={code}&count=50&lng=en&tf=3000000&tz=3&mode=4&country=87&partner=151&getEmpty=true"

    payload = {}
    headers = {
        'authority': '22bet.co.ke',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'SESSION=c6421ebc7fc3a518ebe8fdfa67565e44; fast_coupon=true; lng=en; flaglng=en; typeBetNames=full; coefview=0; auid=sv0vAWVIeee9vxkDA8TSAg==; tzo=3; _gcl_au=1.1.303186096.1699248639; sh.session.id=b9d25270-7d9f-419f-95dc-c4b784f85426; _hjSessionUser_1152929=eyJpZCI6IjhkYWQxMzkxLWJjMzItNTlkOS1hZWRhLWRhY2Y5M2EyYjBkZCIsImNyZWF0ZWQiOjE2OTkyNDg2MzUxODIsImV4aXN0aW5nIjp0cnVlfQ==; v3fr=1; _hjIncludedInSessionSample_1152929=0; _hjSession_1152929=eyJpZCI6IjFmYzMxYmZhLTQyYzUtNDY2Yi04ZTVlLTIzYjdkNGE5MDkyMCIsImNyZWF0ZWQiOjE2OTk1MzY4NDc4NDgsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; _gid=GA1.3.190949348.1699536861; dnb=1; _sp_srt_ses.74a2=*; _glhf=1699555378; ggru=181; _ga=GA1.1.969938612.1699248640; _gat_gtag_UA_136603334_1=1; _sp_srt_id.74a2=c51a3299-22f1-433d-9c60-926eda2e1a0a.1699248642.3.1699537615.1699450331.142a9d4b-71a7-403c-9deb-1c15de6179ff.6afa83fc-18f1-4d33-bc23-ddfd80418426...0; _ga_8BCZ5Q486W=GS1.1.1699536861.4.1.1699537637.18.0.0',
        'referer': 'https://22bet.co.ke/line/football/88637-england-premier-league',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="117.0.5938.149", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.149"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"5.15.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = request_function(url, headers, payload)
    return response['Value']

def api_call_odds(match_id):
    url = f"https://22bet.co.ke/LineFeed/GetGameZip?id={match_id}&lng=en&tzo=3&cfview=0&isSubGames=true&GroupEvents=true&countevents=4000&partner=151"

    payload = {}
    headers = {
        'authority': '22bet.co.ke',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'SESSION=c6421ebc7fc3a518ebe8fdfa67565e44; fast_coupon=true; lng=en; flaglng=en; typeBetNames=full; coefview=0; auid=sv0vAWVIeee9vxkDA8TSAg==; tzo=3; _gcl_au=1.1.303186096.1699248639; sh.session.id=b9d25270-7d9f-419f-95dc-c4b784f85426; _hjSessionUser_1152929=eyJpZCI6IjhkYWQxMzkxLWJjMzItNTlkOS1hZWRhLWRhY2Y5M2EyYjBkZCIsImNyZWF0ZWQiOjE2OTkyNDg2MzUxODIsImV4aXN0aW5nIjp0cnVlfQ==; v3fr=1; _hjIncludedInSessionSample_1152929=0; _gid=GA1.3.190949348.1699536861; dnb=1; _ga=GA1.1.969938612.1699248640; _sp_srt_id.74a2=c51a3299-22f1-433d-9c60-926eda2e1a0a.1699248642.3.1699538564.1699450331.142a9d4b-71a7-403c-9deb-1c15de6179ff.6afa83fc-18f1-4d33-bc23-ddfd80418426.1309bc64-f5e9-4778-b26a-187b4cbb02c8.1699538546570.2; _glhf=1699562763; _ga_8BCZ5Q486W=GS1.1.1699544990.5.0.1699544990.60.0.0; _hjSession_1152929=eyJpZCI6IjkwYWRkNWJlLTgzNDMtNGE0MS1iNGMwLTI5N2RkNGM2NTU1YyIsImNyZWF0ZWQiOjE2OTk1NDQ5OTkzODAsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; ggru=188',
        'referer': 'https://22bet.co.ke/line/football/88637-england-premier-league/189723128-wolverhampton-wanderers-tottenham-hotspur',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="117.0.5938.149", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.149"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"5.15.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = request_function(url, headers, payload)
    return response['Value']['GE']


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

    draw_no_bet_first_half = []
    fasthalf_dc = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_four_five = []
    over_five_five = []
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

    games['match_id'] = match['CI']
    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(match['O1'], match['O1'])
    games['away_team'] = team_mapping.get(match['O2'], match['O2'])

    games['time'] = match['S']


    odds_market = api_call_odds(match['CI'])

    for x in odds_market:
        market = x['G']
        if market == 1:
            home_draw_away = [ x['E'][0][0]['C'],x['E'][1][0]['C'], x['E'][2][0]['C']]
            wager_types.append({"1X2": home_draw_away})
        elif market == 8:
            double_chance.append(x['E'][0][0]['C'])
            double_chance.append(x['E'][1][0]['C'])
            double_chance.append(x['E'][2][0]['C'])
        elif market == 19:
            gg.append(x['E'][0][0]['C'])
            gg.append(x['E'][1][0]['C'])
        elif market == 49:
            draw_no_bet.append(x['E'][0][0]['C'])
            draw_no_bet.append(x['E'][1][0]['C'])
        elif market == 17:
            over_two_five.append(x['E'][0][4]['C'])
            over_two_five.append(x['E'][1][4]['C'])
            over_one_five.append(x['E'][0][2]['C'])
            over_one_five.append(x['E'][1][2]['C'])
            over_three_five.append(x['E'][0][6]['C'])
            over_three_five.append(x['E'][1][6]['C'])

    # wager_types.append({"draw_no_bet": draw_no_bet})
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
        # wager_types.append({"21X": away2_home1X})
        # wager_types.append({"12X": home1_awayX2})
        # wager_types.append({"X12": X_away12})
    except:
        pass
    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        home_team = match_detail['O1']
        away_team = match_detail['O2']

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
    bookie_name = '22bet'
    leagues = [
        {"England Premier League": 88637},
        {"England Championship": 105759},
        {"England League One": 13709},
        {"England League Two": 24637},
        {"Scotland Premiership": 13521},
        {"Scotland Championship": 281713},
        {"Scotland League One": 281719},
        {"Scotland League Two": 281717}
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
                try:
                    league_wager_dic = exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)
                except:
                    continue
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("22bet", bookmaker_data)
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
