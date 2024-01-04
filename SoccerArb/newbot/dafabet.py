import pytz
from datetime import datetime, timedelta

from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes

def api_calls_events(code):
    url = f"https://als.dafabet.co.ke/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&liveOnly=false&eventPathIds={code}&page=1&eventsPerPage=70&l=ke"

    payload = {}
    headers = {
        'authority': 'als.dafabet.co.ke',
        'accept': 'application/json',
        'accept-language': 'en-KY',
        'cookie': 'PHPSESSID=oe266e4ij8kkerkcgiif0tqfkh; user_accept_higher_odds=true; _session=ajVOTnc5bzlqaXNhUGVKWFlNNFFVV0pmeURra2Y1RHQ1R3M0Ty9FSnUydWU2THBsOGJaWnVZeUFiNkJLaHA1QXk5L0ZBbHNPMkI0OVFlU2xla2I2MmZzUEUvUEFqbWxUWXA1WWFtam1zdENPOE4wdThMOG9RWCtkTU94WFlxbGQzZU5QUkkzalJXeFNZVHozT01oL1VFYk5tZkxDY0ZoS2pUVzZQSGRrT1pZelJYQXF5N3hpTk9VZVdWbUgvRjVUODhFOSt5Rm5xUHB2Wjl5aWFtVGlYZDRSQUJUbVRkM1dwZUtwbzk4SWFIaWlUcnZ3YWpRRTJqQ2djT2dZbjl2a2RmVE0wUnVKem9STWFTWXVlNnI2MVM0dHROcjZybGNmQXZoZFArMFJRZlF1c0ZRdEZTUmJKZE1ucFBYTDNsaklCak5pTVhNRDg0ZzJkWVBLWjFSWjAxcTdVSndFc01DZEo4Z1l4eUYrU2N4dmpLcG5NZGhEYUVLNVFvSEx5YU5ocHZtQXYvWGRsNUM1a0M5RU44RlhJNUpSNmhzNkpzQnB5U0NQZ0RBVGRCWUN1LzhDcWRERjk0N1VEMnFzZXFGTmNyOHpjaEJ0NlV2VmFOek5KZzRGTU1PZXMwQmllbWFBbzB2TE5wZEZxNFY4c1UzOU1wWTRTNVArK21pemYxK200Q2Y0Q1dmTjF3SStYV21tVjQyY3RrcUxXNVJ2MDllV2hpR3JvZEphNHVlVjBuTmxCVC81ZDJqaVVRS0hyWGhYWUpBbGxMbFByRXJ4eGd5dmJKR1Nmb2NCOVJTR1RnQ0k2OTRrVU51UElYQ2VLZzcxRG9LYTBraFNrb09oeGlQT1IvakZMT1p1V0MyVHRjbFNUN05heUd0emV2ak5yUTRCWlRZTUN0RU9qb3hLVTU4aVExMG1waS9oYkFtMTI4WUFXQU5XSU9sWVNGd0pLbTJhVWZ1b1RieU50UStuUHBWVnd3eURBaHJDdjZBPS0tMmpaNXdEUjk4V3VoYjNLRU1wbHlXdz09--b183014967ee4abe9d81efc2687e589981cc8936; _gid=GA1.3.1106755070.1700382714; ADRUM=s=1700382819168&r=https%3A%2F%2Fwww.dafabet.co.ke%2Fke%2Fsports%2F240-football%2F23025-england%2F23132-premier-league%3F0; _ga_6Z74534FVC=GS1.1.1700382705.11.1.1700382825.0.0.0; _gat_gtag_UA_68935376_5=1; _ga_VQ8X4Z2HV5=GS1.1.1700382714.11.1.1700382826.0.0.0; _ga=GA1.1.1315461629.1698700249; _ga_S5WHEF6PM5=GS1.1.1700382709.12.1.1700382828.0.0.0',
        'if-none-match': '"1323701467"',
        'referer': 'https://als.dafabet.co.ke/proxy?master=www.dafabet.co.ke?bv=175.1.0',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-accept-language': 'en-KY',
        'x-custom-lb-geoip-country': 'KE',
        'x-lvs-hstoken': 'jjN8XlgTOzRDCmT9xrqXK7qg6o8xLoawrzcq8rxy5CyrhBDuWiqiR2nPffbb2hW1Z3shsXSJ5NchSP0i8h75QeC72p-ZiwR8p3olsEVy6m1gFWQ-klhmdyrcyq9KKbd0',
        'x-requested-with': 'XMLHttpRequest',
        'x-sb-brand': 'DAFAKENYA',
        'x-sb-origin': 'WEB',
        'x-sb-portalid': '71'
    }

    response = request_function(url, headers, payload)
    return response

def api_call_odds(match_id):
    url = f"https://als.dafabet.co.ke/xapi/rest/events/{match_id}?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&lightWeightResponse=true&maxMarketPerEvent=1000&l=ke"

    payload = {}
    headers = {
        'authority': 'als.dafabet.co.ke',
        'accept': 'application/json',
        'accept-language': 'en-KY',
        'cookie': 'PHPSESSID=oe266e4ij8kkerkcgiif0tqfkh; user_accept_higher_odds=true; _session=ajVOTnc5bzlqaXNhUGVKWFlNNFFVV0pmeURra2Y1RHQ1R3M0Ty9FSnUydWU2THBsOGJaWnVZeUFiNkJLaHA1QXk5L0ZBbHNPMkI0OVFlU2xla2I2MmZzUEUvUEFqbWxUWXA1WWFtam1zdENPOE4wdThMOG9RWCtkTU94WFlxbGQzZU5QUkkzalJXeFNZVHozT01oL1VFYk5tZkxDY0ZoS2pUVzZQSGRrT1pZelJYQXF5N3hpTk9VZVdWbUgvRjVUODhFOSt5Rm5xUHB2Wjl5aWFtVGlYZDRSQUJUbVRkM1dwZUtwbzk4SWFIaWlUcnZ3YWpRRTJqQ2djT2dZbjl2a2RmVE0wUnVKem9STWFTWXVlNnI2MVM0dHROcjZybGNmQXZoZFArMFJRZlF1c0ZRdEZTUmJKZE1ucFBYTDNsaklCak5pTVhNRDg0ZzJkWVBLWjFSWjAxcTdVSndFc01DZEo4Z1l4eUYrU2N4dmpLcG5NZGhEYUVLNVFvSEx5YU5ocHZtQXYvWGRsNUM1a0M5RU44RlhJNUpSNmhzNkpzQnB5U0NQZ0RBVGRCWUN1LzhDcWRERjk0N1VEMnFzZXFGTmNyOHpjaEJ0NlV2VmFOek5KZzRGTU1PZXMwQmllbWFBbzB2TE5wZEZxNFY4c1UzOU1wWTRTNVArK21pemYxK200Q2Y0Q1dmTjF3SStYV21tVjQyY3RrcUxXNVJ2MDllV2hpR3JvZEphNHVlVjBuTmxCVC81ZDJqaVVRS0hyWGhYWUpBbGxMbFByRXJ4eGd5dmJKR1Nmb2NCOVJTR1RnQ0k2OTRrVU51UElYQ2VLZzcxRG9LYTBraFNrb09oeGlQT1IvakZMT1p1V0MyVHRjbFNUN05heUd0emV2ak5yUTRCWlRZTUN0RU9qb3hLVTU4aVExMG1waS9oYkFtMTI4WUFXQU5XSU9sWVNGd0pLbTJhVWZ1b1RieU50UStuUHBWVnd3eURBaHJDdjZBPS0tMmpaNXdEUjk4V3VoYjNLRU1wbHlXdz09--b183014967ee4abe9d81efc2687e589981cc8936; _gid=GA1.3.1106755070.1700382714; ADRUM=s=1700385286458&r=https%3A%2F%2Fwww.dafabet.co.ke%2Fke%2Fsports%2F240-football%2F23025-england%2F23132-premier-league%3F0; _ga_6Z74534FVC=GS1.1.1700385289.12.1.1700385297.0.0.0; _ga_VQ8X4Z2HV5=GS1.1.1700385289.12.1.1700385301.0.0.0; _ga=GA1.1.1315461629.1698700249; _ga_S5WHEF6PM5=GS1.1.1700382709.12.1.1700385728.0.0.0',
        'referer': 'https://als.dafabet.co.ke/proxy?master=www.dafabet.co.ke?bv=175.1.0',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-accept-language': 'en-KY',
        'x-custom-lb-geoip-country': 'KE',
        'x-lvs-hstoken': 'jjN8XlgTOzRDCmT9xrqXK7qg6o8xLoawrzcq8rxy5CyrhBDuWiqiR2nPffbb2hW1Z3shsXSJ5NchSP0i8h75QeC72p-ZiwR8p3olsEVy6m1gFWQ-klhmdyrcyq9KKbd0',
        'x-requested-with': 'XMLHttpRequest',
        'x-sb-brand': 'DAFAKENYA',
        'x-sb-origin': 'WEB',
        'x-sb-portalid': '71'
    }

    response = request_function(url, headers, payload)
    return response['markets']

def exctract_odds(match, league, bookie_name):
    games = {}

    wager_types = []

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

    games['match_id'] = match['id']
    # # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)
    #
    #
    # # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(match['opponents'][0]['description'], match['opponents'][0]['description'])
    # games['away_team'] = team_mapping.get(match['opponents'][-1]['description'], match['opponents'][-1]['description'])
    games['home_team'] = match['opponents'][0]['description']
    games['away_team'] = match['opponents'][-1]['description']

    timestamp = datetime.fromisoformat(match['eventDate']).replace(tzinfo=pytz.utc)
    unix_timestamp = int(timestamp.timestamp())
    games['time'] = unix_timestamp

    odds_market = api_call_odds(match['id'])
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    for x in odds_market:
        if x['description'] == "Win/Draw/Win" and x['period']['fullDescription'] == 'Regular Time':
            outcomes = x['outcomes']
            home_odd = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            draw_odd = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            away_odd = outcomes[2]['consolidatedPrice']['currentPrice']['decimal']
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if x['description'] == "Win/Draw/Win" and x['period']['fullDescription'] == 'First Half':
            outcomes = x['outcomes']
            home_odd = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            draw_odd = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            away_odd = outcomes[2]['consolidatedPrice']['currentPrice']['decimal']
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"fasthalf1X2": home_draw_away})

        if x['description'] == "Both teams to score" and x['period']['fullDescription'] == 'Regular Time':
            outcomes = x['outcomes']
            ggyes = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            ggno = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            gg = [ggyes, ggno]
            wager_types.append({"gg": gg})

        if x['description'] == "Both teams to score" and x['period']['fullDescription'] == 'First Half':
            outcomes = x['outcomes']
            ggyes = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            ggno = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            gg_firsthalf = [ggyes, ggno]
            wager_types.append({"gg_firsthalf": gg_firsthalf})

        if x['description'] == "Win Match - Draw No Bet" and x['period']['fullDescription'] == 'Regular Time':
            outcomes = x['outcomes']
            dnbyes = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            dnbno = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            draw_no_bet = [dnbyes, dnbno]
            wager_types.append({"draw_no_bet": draw_no_bet})

        if x['description'] == "Double Chance" and x['period']['fullDescription'] == 'Regular Time':
            outcomes = x['outcomes']
            dnbhome = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            dnbdraw = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            dnbaway = outcomes[2]['consolidatedPrice']['currentPrice']['decimal']
            double_chance = [dnbhome, dnbdraw, dnbaway]
            wager_types.append({"double_chance": double_chance})

        # if x['description'] == "Over / Under" and x['outcomes'][0]['description'] == 'Over 2.5,3':
        if x['description'] == "Over / Under" and x['outcomes'][0]['description'] == 'Over 2.5':
            outcomes = x['outcomes']
            over25 = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            under25 = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            over_two_five = [over25, under25]
            wager_types.append({"over_two_five": over_two_five})

        # if x['description'] == "Over / Under" and x['outcomes'][0]['description'] == 'Over 3,3.5':
        if x['description'] == "Over / Under" and x['outcomes'][0]['description'] == 'Over 3.5':
            outcomes = x['outcomes']
            over25 = outcomes[0]['consolidatedPrice']['currentPrice']['decimal']
            under25 = outcomes[1]['consolidatedPrice']['currentPrice']['decimal']
            over_three_five = [over25, under25]
            wager_types.append({"over_three_five": over_three_five})


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
        home_team = match_detail['opponents'][0]['description']
        away_team = match_detail['opponents'][-1]['description']

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
    bookie_name = 'dafabet'
    leagues = [
        {"England Premier League": 23132},
        {"England Championship": 23031},
        {"England League One": 23058},
        {"England League Two": 23522},
        {"Scotland Premiership": 23309},
        {"Scotland Championship": 23420},
        {"Scotland League One": 25530},
        {"Scotland League Two": 25531},
        {"Irish Premier": 22916},
        {"Northern Ireland": 25203},
        {"France League One": 23169},
        {"France League Two": 23428},
        {"Laliga": 23034},
        {"Copa del Ray": 29855},
        {"Laliga 2": 28571},
        {"German Bundesliga": 23405},
        {"German Bundesliga 2": 23925},
        {"German Bundesliga 3": 23907},
        {"German DFB Pokal": 43606},
        {"Italy Serie A": 23454},
        {"Italy Serie B": 23716},
        {"Italy Coppa Italia": 99090},
        {"Netherlands Eredivisie": 23952},
        {"Netherlands Erste Division": 24168},
        {"Czech Liga 1": 36921981},
        {"Greece Super League 1": 25175},
        {"Swedish Allsvenska": 23271},
        {"Superatten": 24573},
        {"Danish Superligan": 26047},
        {"England FA": 105245},
    ]

    bookmaker_data = []
    for league in leagues:
        try:
            print(league)
            league_name, league_id = process_league(league)
            match_details = api_calls_events(f"{league_id}")
            if match_details is None:
                continue

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
                    league_wager_dic =  exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)

            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("dafabet", bookmaker_data)
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

