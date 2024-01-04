import pytz
from datetime import datetime, timedelta

from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes

def api_calls_events(code):
    url = f"https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/{code}/0/0"

    payload = {}
    headers = {
        'authority': 'sportsapicdn-desktop.betking.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.betking.com',
        'referer': 'https://www.betking.com/',
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
        return response["AreaMatches"][0]["Items"]
    except:
        return None
def api_call_odds(match_id):
    url = f"https://sportsapicdn-desktop.betking.com/api/feeds/prematch/lite/event/ungrouped/en/4/{match_id}/531"

    payload = {}
    headers = {
        'authority': 'sportsapicdn-desktop.betking.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.betking.com',
        'referer': 'https://www.betking.com/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response["AM"][0]['IT'][0]['OC']

def exctract_odds(match, league, bookie_name):
    games = {}

    wager_types = []
    handicap1 = [] # -1.5 / 1.5

    first_team_to_score_first_half = []  # hometeam, draw, away_team


    games['match_id'] = match['ItemID']
    teams = match['ItemName'].split(" - ")

    # # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)
    #
    #
    # # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(teams[0], teams[0])
    # games['away_team'] = team_mapping.get(teams[-1], teams[-1])
    games['home_team'] = teams[0]
    games['away_team'] = teams[-1]

    # Parse the timestamp string
    dt = datetime.fromisoformat( match['ItemDate'])
    # Convert to UTC
    dt_utc = dt.astimezone(pytz.utc)
    # Convert to Unix timestamp
    timestamp_unix = int(dt_utc.timestamp())
    games['time'] = timestamp_unix

    odds_collection = match['OddsCollection']
    for market in odds_collection:
        market_name = market['OddsType']['OddsTypeName']
        match_odds = market['MatchOdds']
        if market_name == "1X2":
            home_odd = match_odds[0]['Outcome']['OddOutcome']
            draw_odd = match_odds[1]['Outcome']['OddOutcome']
            away_odd = match_odds[2]['Outcome']['OddOutcome']
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})
        if market_name == "Double Chance":
            home_odd1X = match_odds[0]['Outcome']['OddOutcome']
            draw_odd12 = match_odds[1]['Outcome']['OddOutcome']
            away_oddX2 = match_odds[2]['Outcome']['OddOutcome']
            double_chance = [home_odd1X, draw_odd12, away_oddX2]
            wager_types.append({"double_chance": double_chance})
        if market_name == "Total Goals 2.5":
            over25 = match_odds[0]['Outcome']['OddOutcome']
            under25 = match_odds[1]['Outcome']['OddOutcome']
            over_two_five = [over25, under25]
            wager_types.append({"over_two_five": over_two_five})
        if market_name == "GG/NG":
            ggyes = match_odds[0]['Outcome']['OddOutcome']
            ggno = match_odds[1]['Outcome']['OddOutcome']
            gg = [ggyes, ggno]
            wager_types.append({"gg": gg})
        if market_name == "Draw No Bet":
            dnbyes = match_odds[0]['Outcome']['OddOutcome']
            dnbno = match_odds[1]['Outcome']['OddOutcome']
            draw_no_bet = [dnbyes, dnbno]
            wager_types.append({"draw_no_bet": draw_no_bet})
        if market_name == "Home To Win Either Half":
            homeyes = match_odds[0]['Outcome']['OddOutcome']
            homeno = match_odds[1]['Outcome']['OddOutcome']
            draw_no_bet = [homeyes, homeno]
            wager_types.append({"home_to_win_either_half": draw_no_bet})

        if market_name == "Away To Win Either Half":
            awayyes = match_odds[0]['Outcome']['OddOutcome']
            awayno = match_odds[1]['Outcome']['OddOutcome']
            draw_no_bet = [awayyes, awayno]
            wager_types.append({"away_to_win_either_half": draw_no_bet})


    market_ids = [531 ,16]
    odds_market = api_call_odds(match['ItemID'])
    # print(odds_market)

    for market in odds_market:
        market_name = market['OT']['ON']
        match_odds = market['MO']
        if market_name == "Total Goals 1.5":
            over15 = match_odds[0]['OT']['OO']
            under15 = match_odds[1]['OT']['OO']
            over_one_five = [over15, under15]
            wager_types.append({"over_one_five": over_one_five})
        if market_name == "Total Goals 3.5":
            over35 = match_odds[0]['OT']['OO']
            under35 = match_odds[1]['OT']['OO']
            over_three_five = [over35, under35]
            wager_types.append({"over_three_five": over_three_five})
        if market_name == "Total Goals 0.5":
            over05 = match_odds[0]['OT']['OO']
            under05 = match_odds[1]['OT']['OO']
            over_05_five = [over05, under05]
            wager_types.append({"over_ofive_five": over_05_five})
        if market_name == "Total Goals 4.5":
            over45 = match_odds[0]['OT']['OO']
            under45 = match_odds[1]['OT']['OO']
            over_four_five = [over45, under45]
            wager_types.append({"over_four_five": over_four_five})
        if market_name == "Total Goals 5.5":
            over55 = match_odds[0]['OT']['OO']
            under55 = match_odds[1]['OT']['OO']
            over_five_five = [over55, under55]
            wager_types.append({"over_five_five": over_five_five})
        if market_name == "Odd/Even Goals":
            odd = match_odds[0]['OT']['OO']
            even = match_odds[1]['OT']['OO']
            odd_even = [odd, even]
            wager_types.append({"odd_even": odd_even})
        if market_name == "First Team Goal":
            home = match_odds[0]['OT']['OO']
            draw = match_odds[1]['OT']['OO']
            away = match_odds[2]['OT']['OO']
            first_team_to_score = [home, draw, away]
            wager_types.append({"first_team_to_score": first_team_to_score})
        if market_name == "Last Team Goal":
            home = match_odds[0]['OT']['OO']
            draw = match_odds[2]['OT']['OO']
            away = match_odds[1]['OT']['OO']
            last_team_to_score = [home, draw, away]
            wager_types.append({"last_team_to_score": last_team_to_score})


        if market_name == "1st Half - 1X2":
            home = match_odds[0]['OT']['OO']
            draw = match_odds[1]['OT']['OO']
            away = match_odds[2]['OT']['OO']
            fasthalf1X2 = [home, draw, away]
            wager_types.append({"fasthalf1X2": fasthalf1X2})

        if market_name == "1st Half - Double Chance":
            home = match_odds[0]['OT']['OO']
            draw = match_odds[1]['OT']['OO']
            away = match_odds[2]['OT']['OO']
            fasthalf_dc = [home, draw, away]
            wager_types.append({"fasthalf_dc": fasthalf_dc})

        if market_name == "Home Total Goals 0.5":
            over05 = match_odds[0]['OT']['OO']
            under05 = match_odds[1]['OT']['OO']
            home_team_overunder05 = [over05,under05]
            wager_types.append({"home_team_overunder05": home_team_overunder05})
        if market_name == "Home Total Goals 1.5":
            over15 = match_odds[0]['OT']['OO']
            under15 = match_odds[1]['OT']['OO']
            home_team_overunder15 = [over15,under15]
            wager_types.append({"home_team_overunder15": home_team_overunder15})
        if market_name == "Home Total Goals 2.5":
            over25 = match_odds[0]['OT']['OO']
            under25 = match_odds[1]['OT']['OO']
            home_team_overunder25 = [over25,under25]
            wager_types.append({"home_team_overunder25": home_team_overunder25})
        if market_name == "Away Total Goals 0.5":
            over05 = match_odds[0]['OT']['OO']
            under05 = match_odds[1]['OT']['OO']
            away_team_overunder05 = [over05,under05]
            wager_types.append({"away_team_overunder05": away_team_overunder05})
        if market_name == "Away Total Goals 1.5":
            over15 = match_odds[0]['OT']['OO']
            under15 = match_odds[1]['OT']['OO']
            away_team_overunder15 = [over15,under15]
            wager_types.append({"away_team_overunder15": away_team_overunder15})
        if market_name == "Away Total Goals 2.5":
            over25 = match_odds[0]['OT']['OO']
            under25 = match_odds[1]['OT']['OO']
            away_team_overunder25 = [over25,under25]
            wager_types.append({"away_team_overunder25": away_team_overunder25})

        if market_name == "1st Half - Both Teams to Score":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            gg_firsthalf = [ggy,ggn]
            wager_types.append({"gg_firsthalf": gg_firsthalf})

        if market_name == "1st Half - Draw No Bet":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            draw_no_bet_first_half = [ggy,ggn]
            wager_types.append({"draw_no_bet_first_half": draw_no_bet_first_half})

        if market_name == "1st Half - Odd/Even Goals":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            odd_even_firsthalf = [ggy,ggn]
            wager_types.append({"odd_even_firsthalf": odd_even_firsthalf})

        if market_name == "1st Half - Total Goals 0.5":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            over_ofive_five_first_half = [ggy,ggn]
            wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})
        if market_name == "1st Half - Total Goals 1.5":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            over_one_five_first_half = [ggy,ggn]
            wager_types.append({"over_one_five_first_half": over_one_five_first_half})
        if market_name == "1st Half - Total Goals 2.5":
            ggy = match_odds[0]['OT']['OO']
            ggn = match_odds[1]['OT']['OO']
            over_two_five_first_half = [ggy,ggn]
            wager_types.append({"over_two_five_first_half": over_two_five_first_half})

    handicap1 = []  # -1.5 / 1.5

    # away2_home1X = [away_odd, double_chance[0]]
    # home1_awayX2 = [home_odd, double_chance[2]]
    # X_away12 = [draw_odd, double_chance[1]]
    #
    # wager_types.append({"21X": away2_home1X})
    # wager_types.append({"12X": home1_awayX2})
    # wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        teams = match_detail['ItemName'].split(" - ")

        home_team = teams[0]
        away_team = teams[-1]

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

def main():
    bookie_name = 'betking'
    leagues = [
        {"England Premier League": 841},
        {"England Championship": 863},
        {"England League One": 909},
        {"England League Two": 939},
        {"Scotland Premiership": 1522762},
        {"Scotland Championship": 1522766},
        {"Scotland League One": 1982205},
        {"Scotland League Two": 4794385},
        {"Northern Ireland": 1522772},
        {"France League One": 1104},
        {"France League Two": 1179},
        {"Laliga": 1108},
        {"Laliga 2": 6274},
        {"Copa del Ray": 16156},
        {"German Bundesliga": 1007},
        {"German Bundesliga 2": 1025},
        {"Italy Serie A": 3775},
        {"Italy Serie B": 3776},
        {"Italy Coppa Italia": 3092},
        {"Netherlands Eredivisie": 1522637},
        {"Greece Super League 1": 1522629},
        {"Superatten": 23144},
        {"England FA": 20647}
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
            # if league_name in league_mapping:
            #     league_name = league_mapping[league_name]
            #
            # # Testing Function To See if teams are correctly named
            # testing = testing_function(bookie_name, league_name)
            # missing_names = check_team_names_in_match_details(testing, match_details)
            # print("**** This are the missing matches", missing_names)

            liga = {}
            league_data = []

            for match in match_details:
                try:
                    league_wager_dic =  exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)
                except:
                    continue

            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("betking", bookmaker_data)
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

