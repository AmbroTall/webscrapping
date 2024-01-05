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
    handicap1 = []  # -1.5 / 1.5
    fasthalf1X2 = []

    draw_no_bet_first_half = []
    draw_no_bet_second_half = []
    over_ofive_five_first_half = []
    over_ofive_five = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_two_five = []
    over_one_five = []
    over_three_five = []
    over_four_five = []
    over_five_five = []
    gg = []
    over_ofive_five_second_half = []
    over_one_five_second_half = []
    over_two_five_second_half = []

    fasthalf_dc = []
    secondhalf_dc = []
    gg_firsthalf = []
    gg_secondhalf = []
    odd_even = []
    odd_even_firsthalf = []
    odd_even_secondhalf = []
    hometeam_odd_even = []
    awayteam_odd_even = []
    first_team_to_score = []  # hometeam, draw, away_team
    first_team_to_score_1st_half = []  # hometeam, draw, away_team
    first_team_to_score_2nd_half = []  # hometeam, draw, away_team
    last_team_to_score = []  # hometeam, draw, away_team
    home_team_overunder15 = []
    home_team_overunder25 = []
    home_team_overunder05 = []
    away_team_overunder15 = []
    away_team_overunder25 = []
    away_team_overunder05 = []

    corners_overunder65 = []
    corners_overunder75 = []
    corners_overunder85 = []
    corners_overunder95 = []
    corners_overunder105 = []
    corners_overunder115 = []
    corners_overunder125 = []
    corners_overunder135 = []

    corners_overunder7_3way = []
    corners_overunder8_3way = []
    corners_overunder9_3way = []
    corners_overunder10_3way = []
    corners_overunder11_3way = []  # over under exactly
    corners_overunder12_3way = []
    corners_overunder13_3way = []

    home_clean_sheet = []
    away_clean_sheet = []
    home_clean_sheet_first_half = []
    away_clean_sheet_first_half = []
    home_clean_sheet_second_half = []
    away_clean_sheet_second_half = []
    first_half_home_team_overunder15 = []
    first_half_home_team_overunder25 = []
    first_half_home_team_overunder05 = []
    first_half_away_team_overunder15 = []
    first_half_away_team_overunder25 = []
    first_half_away_team_overunder05 = []

    second_half_home_team_overunder15 = []
    second_half_home_team_overunder25 = []
    second_half_home_team_overunder05 = []
    second_half_away_team_overunder15 = []
    second_half_away_team_overunder25 = []
    second_half_away_team_overunder05 = []
    second1X2 = []

    games['match_id'] = match['event']['id']
    # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)

    # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(match['event']['homeName'], match['event']['homeName'])
    # games['away_team'] = team_mapping.get(match['event']['awayName'], match['event']['awayName'])
    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = match['event']['homeName']
    games['away_team'] = match['event']['awayName']

    games['time'] = converting_time_string(match['event']['start'])

    odds_market = api_call_odds(match['event']['id'])

    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    for market in odds_market:
        if market['criterion']['label'] == "Full Time":
            home_odd = float(market['outcomes'][0]['odds']) / 1000
            away_odd = float(market['outcomes'][2]['odds']) / 1000
            draw_odd = float(market['outcomes'][1]['odds']) / 1000
            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if market['criterion']['label'] == "Double Chance":
            double_chance.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000))
            wager_types.append({"double_chance": double_chance})

        if market['criterion']['label'] == "Double Chance - 1st Half":
            fasthalf_dc.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000))
            wager_types.append({"fasthalf_dc": fasthalf_dc})
        if market['criterion']['label'] == "Double Chance - 2nd Half":
            secondhalf_dc.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000))
            wager_types.append({"secondhalf_dc": secondhalf_dc})

        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 500:
            over_ofive_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_ofive_five": over_ofive_five})

        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 2500:
            over_two_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_two_five": over_two_five})


        if market['criterion']['label'] == "Total Goals - 1st Half" and market['outcomes'][0]['line'] == 500:
            over_ofive_five_first_half.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})

        if market['criterion']['label'] == "Total Goals - 1st Half" and market['outcomes'][0]['line'] == 1500:
            over_one_five_first_half.extend((float(market['outcomes'][0]['odds']) / 1000, float(market['outcomes'][1]['odds']) / 1000))
            wager_types.append({"over_one_five_first_half": over_one_five_first_half})

        if market['criterion']['label'] == "Total Goals - 1st Half" and market['outcomes'][0]['line'] == 2500:
            over_two_five_first_half.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_two_five_first_half": over_two_five_first_half})

        if market['criterion']['label'] == "Total Goals - 2nd Half" and market['outcomes'][0]['line'] == 500:
            over_ofive_five_second_half.extend((float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][0]['odds'])/1000))
            wager_types.append({"over_ofive_five_second_half": over_ofive_five_second_half})

        if market['criterion']['label'] == "Total Goals - 2nd Half" and market['outcomes'][0]['line'] == 1500:
            over_one_five_second_half.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"over_one_five_second_half": over_one_five_second_half})

        if market['criterion']['label'] == "Total Goals - 2nd Half" and market['outcomes'][0]['line'] == 2500:
            over_two_five_second_half.extend((float(market['outcomes'][1]['odds'])/1000, float(market['outcomes'][0]['odds'])/1000))
            wager_types.append({"over_two_five_second_half": over_two_five_second_half})

        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 4500:
            over_four_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_four_five": over_four_five})
        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 5500:
            over_five_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_five_five": over_five_five})

        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 1500:
            over_one_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_one_five": over_one_five})

        if market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 3500:
            over_three_five.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"over_three_five": over_three_five})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']}" and market['outcomes'][0]['line'] == 500:
            away_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"away_team_overunder05": away_team_overunder05})
        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']}" and market['outcomes'][0]['line'] == 1500:
            away_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"away_team_overunder15": away_team_overunder15})
        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']}" and market['outcomes'][0]['line'] == 2500:
            away_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"away_team_overunder25": away_team_overunder25})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']}" and market['outcomes'][0]['line'] == 500:
            home_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"home_team_overunder05": home_team_overunder05})
        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']}" and market['outcomes'][0]['line'] == 1500:
            home_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"home_team_overunder15": home_team_overunder15})
        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']}" and market['outcomes'][0]['line'] == 2500:
            home_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"home_team_overunder25": home_team_overunder25})


        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 1st Half" and market['outcomes'][0]['line'] == 500:
            first_half_home_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_home_team_overunder05": first_half_home_team_overunder05})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 1st Half" and market['outcomes'][0]['line'] == 1500:
            first_half_away_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_home_team_overunder15": first_half_home_team_overunder15})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 1st Half" and market['outcomes'][0]['line'] == 2500:
            first_half_away_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_home_team_overunder25": first_half_home_team_overunder25})


        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 1st Half" and market['outcomes'][0]['line'] == 500:
            first_half_away_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_away_team_overunder05": first_half_away_team_overunder05})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 1st Half" and market['outcomes'][0]['line'] == 1500:
            first_half_away_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_away_team_overunder15": first_half_away_team_overunder15})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 1st Half" and market['outcomes'][0]['line'] == 2500:
            first_half_away_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"first_half_away_team_overunder25": first_half_away_team_overunder25})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 2nd Half" and market['outcomes'][0]['line'] == 500:
            second_half_home_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_home_team_overunder05": second_half_home_team_overunder05})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 2nd Half" and market['outcomes'][0]['line'] == 1500:
            second_half_home_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_home_team_overunder15": second_half_home_team_overunder15})

        if market['criterion']['label'] == f"Total Goals by {match['event']['homeName']} - 2nd Half" and market['outcomes'][0]['line'] == 2500:
            second_half_home_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_home_team_overunder25": second_half_home_team_overunder25})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 2nd Half" and market['outcomes'][0]['line'] == 500:
            second_half_away_team_overunder05.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_away_team_overunder05": second_half_away_team_overunder05})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 2nd Half" and market['outcomes'][0]['line'] == 1500:
            first_half_away_team_overunder15.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_away_team_overunder15": second_half_away_team_overunder15})

        if market['criterion']['label'] == f"Total Goals by {match['event']['awayName']} - 2nd Half" and market['outcomes'][0]['line'] == 2500:
            first_half_away_team_overunder25.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
            wager_types.append({"second_half_away_team_overunder25": second_half_away_team_overunder25})



        if market['criterion']['label'] == "Draw No Bet":
            draw_no_bet.extend((market['outcomes'][0]['odds'] / 1000, market['outcomes'][1]['odds'] / 1000))
            wager_types.append({"draw_no_bet": draw_no_bet})

        if market['criterion']['label'] == "Draw No Bet - 1st Half":
            draw_no_bet_first_half.extend((market['outcomes'][0]['odds'] / 1000, market['outcomes'][1]['odds'] / 1000))
            wager_types.append({"draw_no_bet_first_half": draw_no_bet_first_half})

        if market['criterion']['label'] == "Draw No Bet - 2nd Half":
            draw_no_bet_second_half.extend((market['outcomes'][0]['odds'] / 1000, market['outcomes'][1]['odds'] / 1000))
            wager_types.append({"draw_no_bet_second_half": draw_no_bet_second_half})

        if market['criterion']['label'] == "Half Time":
            fasthalf1X2.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000,  float(market['outcomes'][2]['odds'])/1000))
            wager_types.append({"fasthalf1X2": fasthalf1X2})
        if market['criterion']['label'] == "2nd Half":
            second1X2.extend((float(market['outcomes'][0]['odds'])/1000,float(market['outcomes'][1]['odds'])/1000,  float(market['outcomes'][2]['odds'])/1000))
            wager_types.append({"second1X2": second1X2})

        if market['criterion']['label'] == "Both Teams To Score":
            gg.extend((float(market['outcomes'][0]['odds']) / 1000, float(market['outcomes'][1]['odds']) / 1000))
            wager_types.append({"gg": gg})

        if market['criterion']['label'] == "Both Teams To Score - 1st Half":
            gg_firsthalf.extend((float(market['outcomes'][0]['odds']) / 1000, float(market['outcomes'][1]['odds']) / 1000))
            wager_types.append({"gg_firsthalf": gg_firsthalf})

        if market['criterion']['label'] == "Both Teams To Score - 2nd Half":
            gg_secondhalf.extend((float(market['outcomes'][0]['odds']) / 1000, float(market['outcomes'][1]['odds']) / 1000))
            wager_types.append({"gg_secondhalf": gg_secondhalf})

        if market['criterion']['label'] == "Total Corners"  and market['outcomes'][0]['line'] == 7500:
            corners_overunder75.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder75": corners_overunder75})
        if market['criterion']['label'] == "Total Corners"  and market['outcomes'][0]['line'] == 6500:
            corners_overunder75.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder65": corners_overunder75})

        if market['criterion']['label'] == "Total Corners" and market['outcomes'][0]['line'] == 8500:
            corners_overunder85.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder85": corners_overunder85})
        if market['criterion']['label'] == "Total Corners" and market['outcomes'][0]['line'] == 10500:
            corners_overunder105.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder105": corners_overunder105})
        if market['criterion']['label'] == "Total Corners" and market['outcomes'][0]['line'] == 11500:
            corners_overunder115.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder115": corners_overunder115})
        if market['criterion']['label'] == "Total Corners" and market['outcomes'][0]['line'] == 12500:
            corners_overunder125.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder125": corners_overunder125})
        if market['criterion']['label'] == "Total Corners" and market['outcomes'][0]['line'] == 13500:
            corners_overunder135.extend((float(market['outcomes'][1]['odds']) / 1000, float(market['outcomes'][0]['odds']) / 1000))
            wager_types.append({"corners_overunder135": corners_overunder135})

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

# def main():
#     bookie_name = 'sunbet'
#     # leagues = [{"England Premier League": "england/premier_league"} ]
#     leagues = [
#         {"England Premier League": "england/premier_league"},
#         {"England Championship": "england/the_championship"},
#         {"England League One": "england/league_one"},
#         {"England League Two": "england/league_two"},
#         {"Scotland Premiership": "scotland/scottish_premiership"},
#         {"Scotland Championship":"scotland/championship"},
#         {"Scotland League One":"scotland/league_one"},
#         {"Scotland League Two":"scotland/league_two"},
#         {"France League One": "france/ligue_1"},
#         {"France League Two": "france/ligue_2"},
#         {"Laliga": "spain/la_liga"},
#         {"Copa del Ray": "spain/copa_del_rey"},
#         {"Laliga 2": "spain/la_liga_2"},
#         {"German Bundesliga": "germany/bundesliga"},
#         {"German Bundesliga 2": "germany/2__bundesliga"},
#         {"German DFB Pokal": "germany/dfb_pokal"},
#         {"Italy Serie A": "italy/serie_a"},
#         {"Italy Serie B": "italy/serie_b"},
#         {"Italy Coppa Italia": "italy/coppa_italia"},
#         {"Netherlands Eredivisie": "netherlands/eredivisie"},
#         {"Netherlands Erste Division": "netherlands/eerste_divisie"},
#         {"KNVB Cup": "netherlands/knvb_beker"},
#         {"Czech Liga 1": "czech_republic/first_league"},
#         {"Greece Super League 1": "greece/super_league"},
#         {"Swedish Allsvenska": "sweden/allsvenskan"},
#         {"Superatten": "sweden/superettan"},
#         {"Danish Superligan": "denmark/superligaen"},
#         {"Denmark Landspokel": "denmark/dbu_pokalen"},
#         {"England FA": "england/fa_cup"},
#     ]
#
#     bookmaker_data = []
#     for league in leagues:
#         try:
#             print(league)
#             league_name, league_id = process_league(league)
#             match_details = api_calls_events(f"{league_id}")
#
#             league_mapping = {
#                 "England Premier League": "England-Premier League",
#                 "England Championship": "England-EFL Cup",
#                 "England League One": "England-League One",
#                 "England League Two": "England-League Two",
#                 "Scotland Premiership": "Scotland-Premiership",
#                 "Scotland Championship": "Scotland-Championship",
#                 "Scotland League One": "Scotland-League One",
#                 "Scotland League Two": "Scotland-League Two",
#             }
#             # Check if the league_name is in the mapping dictionary, if yes, update it
#             # if league_name in league_mapping:
#             #     league_name = league_mapping[league_name]
#             #
#             # # Testing Function To See if teams are correctly named
#             # testing = testing_function(bookie_name, league_name)
#             # missing_names = check_team_names_in_match_details(testing, match_details)
#             # print("**** This are the missing matches", missing_names)
#
#             liga = {}
#             league_data = []
#
#             for match in match_details:
#                 try:
#                     league_wager_dic =  exctract_odds(match, league_name, bookie_name)
#                     league_data.append(league_wager_dic)
#                 except:
#                     continue
#             liga[league_name] = league_data
#             bookmaker_data.append(liga)
#             print("sunbet", bookmaker_data)
#         except Exception as e:
#             print("Ambrose", e)
#             continue
#     return bookmaker_data


def main(league):
    bookie_name = 'sunbet'
    leagues = [
        {"England Premier League": "england/premier_league"},
        {"England Championship": "england/the_championship"},
        {"England League One": "england/league_one"},
        {"England League Two": "england/league_two"},
        {"Scotland Premiership": "scotland/scottish_premiership"},
        {"Scotland Championship":"scotland/championship"},
        {"Scotland League One":"scotland/league_one"},
        {"Scotland League Two":"scotland/league_two"},
        {"France League One": "france/ligue_1"},
        {"France League Two": "france/ligue_2"},
        {"Laliga": "spain/la_liga"},
        {"Copa del Ray": "spain/copa_del_rey"},
        {"Laliga 2": "spain/la_liga_2"},
        {"German Bundesliga": "germany/bundesliga"},
        {"German Bundesliga 2": "germany/2__bundesliga"},
        {"German DFB Pokal": "germany/dfb_pokal"},
        {"Italy Serie A": "italy/serie_a"},
        {"Italy Serie B": "italy/serie_b"},
        {"Italy Coppa Italia": "italy/coppa_italia"},
        {"Netherlands Eredivisie": "netherlands/eredivisie"},
        {"Netherlands Erste Division": "netherlands/eerste_divisie"},
        {"KNVB Cup": "netherlands/knvb_beker"},
        {"Czech Liga 1": "czech_republic/first_league"},
        {"Greece Super League 1": "greece/super_league"},
        {"Swedish Allsvenska": "sweden/allsvenskan"},
        {"Superatten": "sweden/superettan"},
        {"Danish Superligan": "denmark/superligaen"},
        {"Denmark Landspokel": "denmark/dbu_pokalen"},
        {"England FA": "england/fa_cup"},
    ]

    bookmaker_data = []

    try:
        print(league)
        # Find the league dictionary based on the provided league name
        selected_league = next((item for item in leagues if league in item), None)

        if selected_league:
            league_name, league_id = process_league(selected_league)
            match_details = api_calls_events(f"{league_id}")

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
            print("sunbet", bookmaker_data)
            return bookmaker_data
        else:
            print(f"No matching league found for {league}")
    except Exception as e:
        print("Ambrose", e)


if __name__ == '__main__':
    start_time = time.time()
    games = main("England Premier League")
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60

    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)
