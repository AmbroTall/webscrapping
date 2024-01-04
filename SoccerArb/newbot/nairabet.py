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
    fasthalf1X2 = []

    draw_no_bet_first_half = []
    draw_no_bet_second_half = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
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
    corners_overunder11_3way = []  #over under exactly
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

    games['match_id'] = match['id']
    # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)
    #
    #
    # # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(match['eventNames'][0], match['eventNames'][0])
    # games['away_team'] = team_mapping.get(match['eventNames'][-1], match['eventNames'][-1])
    games['home_team'] = match['eventNames'][0]
    games['away_team'] = match['eventNames'][-1]
    games['time'] = match['startTime']

    odds_market = api_call_odds(match['id'])
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    for marketgroup in odds_market:
        if (marketgroup['name'] == 'Main'):
            markets = marketgroup['markets']
            for market in markets:
                if market['name'] == "1x2":
                    home_odd = float(market['outcomes'][0]['value'])
                    draw_odd = float(market['outcomes'][1]['value'])
                    away_odd = float(market['outcomes'][2]['value'])
                    home_draw_away = [home_odd, draw_odd, away_odd]
                    wager_types.append({"1X2": home_draw_away})

                if market['name'] == "Draw No Bet" and len(market['outcomes']) == 2:
                    draw_no_bet.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))
                    wager_types.append({"draw_no_bet": draw_no_bet})

                if market['name'] == "Double Chance" and len(market['outcomes']) == 3:
                    double_chance.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']),float(market['outcomes'][1]['value'])))
                    wager_types.append({"double_chance": double_chance})

                if market['entityName'] == "Total Goals - Total Goals 1.5":
                    over_one_five_o = float(market['outcomes'][1]['value'])
                    over_one_five_u = float(market['outcomes'][0]['value'])
                    over_one_five = [over_one_five_o, over_one_five_u]
                    wager_types.append({"over_one_five": over_one_five})

                if market['entityName'] == "Total Goals - Total Goals 2.5":
                    over_two_five_o = float(market['outcomes'][1]['value'])
                    over_two_five_u = float(market['outcomes'][0]['value'])
                    over_two_five = [over_two_five_o, over_two_five_u]
                    wager_types.append({"over_two_five": over_two_five})

                if market['entityName'] == "Total Goals - Total Goals 4.5":
                    over_two_five_o = float(market['outcomes'][1]['value'])
                    over_two_five_u = float(market['outcomes'][0]['value'])
                    over_four_five = [over_two_five_o, over_two_five_u]
                    wager_types.append({"over_four_five": over_four_five})

                if market['entityName'] == "Total Goals - Total Goals 5.5":
                    over_two_five_o = float(market['outcomes'][1]['value'])
                    over_two_five_u = float(market['outcomes'][0]['value'])
                    over_five_five = [over_two_five_o, over_two_five_u]
                    wager_types.append({"over_five_five": over_five_five})

                if market['entityName'] == "Total Goals - Total Goals 3.5":
                    over_three_five_o = float(market['outcomes'][1]['value'])
                    over_three_five_u = float(market['outcomes'][0]['value'])
                    over_three_five = [over_three_five_o, over_three_five_u]
                    wager_types.append({"over_three_five": over_three_five})

                if market['name'] == "Both Teams to Score":
                    for x in market['outcomes']:
                        if x['id'].lower() == "yes":
                            ggyes = x['value']
                        if x['id'].lower() == "no":
                            ggno = x['value']
                    over_three_five = [float(ggyes), float(ggno)]
                    wager_types.append({"gg": over_three_five})

        if marketgroup['name'] == '1st Half':
            markets2 = marketgroup['markets']
            for market in markets2:
                if market['entityName'] == "First Half Double Chance" and len(market['outcomes']) == 3:
                    fasthalf_dc.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']),float(market['outcomes'][1]['value'])))
                    wager_types.append({"fasthalf_dc": fasthalf_dc})
                if market['entityName'] == "First Half Result" and len(market['outcomes']) == 3:
                    fasthalf1X2.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"fasthalf1X2": fasthalf1X2})
                if market['entityName'] == "Half Time Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    over_ofive_five_first_half.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})
                if market['entityName'] == "Half Time Goals - Over/Under 1.5" and len(market['outcomes']) == 2:
                    over_one_five_first_half.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_one_five_first_half": over_one_five_first_half})
                if market['entityName'] == "Half Time Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    over_two_five_first_half.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_two_five_first_half": over_two_five_first_half})
                if market['entityName'] == "Both Teams To Score In 1st Half" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "yes":
                            ggyes = x['value']
                        if x['id'].lower() == "no":
                            ggno = x['value']
                    gg_firsthalf = [ggyes, ggno]
                    wager_types.append({"gg_firsthalf": gg_firsthalf})
                if market['entityName'] == f"{match['eventNames'][0]} First Half Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    first_half_home_team_overunder05.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_home_team_overunder05": first_half_home_team_overunder05})
                if market['entityName'] == f"{match['eventNames'][0]} First Half Goals - Over/Under 1.5" and len(market['outcomes']) == 2:
                    first_half_home_team_overunder15.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_home_team_overunder15": first_half_home_team_overunder15})
                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    first_half_away_team_overunder05.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_away_team_overunder05": first_half_away_team_overunder05})
                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 1.5" and len(market['outcomes']) == 2:
                    first_half_away_team_overunder15.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_away_team_overunder15": first_half_away_team_overunder15})
                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    first_half_away_team_overunder25.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_away_team_overunder25": first_half_away_team_overunder25})
                if market['entityName'] == f"{match['eventNames'][0]} First Half Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    first_half_home_team_overunder25.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"first_half_home_team_overunder25": first_half_home_team_overunder25})
                if market['entityName'] == "First Half Goals – odd/even" and len(market['outcomes']) == 2:
                    odd_even_firsthalf.extend((float(market['outcomes'][1]['value']),float(market['outcomes'][0]['value'])))
                    wager_types.append({"odd_even_firsthalf": odd_even_firsthalf})
        if marketgroup['name'] == '2nd Half':
            markets2 = marketgroup['markets']
            for market in markets2:
                if market['entityName'] == "Second Half Double Chance" and len(market['outcomes']) == 3:
                    secondhalf_dc.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']),
                                          float(market['outcomes'][1]['value'])))
                    wager_types.append({"secondhalf_dc": secondhalf_dc})
                if market['entityName'] == "Second Half Result" and len(market['outcomes']) == 3:
                    second1X2.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value']),
                                      float(market['outcomes'][2]['value'])))
                    wager_types.append({"second1X2": second1X2})
                if market['entityName'] == "Second Half Total Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    over_ofive_five_second_half.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_ofive_five_second_half": over_ofive_five_second_half})

                if market['entityName'] == "Second Half Total Goals - Over/Under 1.5" and len(market['outcomes']) == 2:
                    over_one_five_second_half.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_one_five_second_half": over_one_five_second_half})

                if market['entityName'] == "Second Half Total Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    over_two_five_second_half.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"over_two_five_second_half": over_two_five_second_half})

                if market['entityName'] == "Both Teams To Score In 2nd Half" and len(market['outcomes']) == 2:
                    gg_secondhalf.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"gg_secondhalf": gg_secondhalf})

                if market['entityName'] == f"{match['eventNames'][0]} Second Half Goals - Over/Under 0.5" and len(
                        market['outcomes']) == 2:
                    second_half_home_team_overunder05.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_home_team_overunder05": second_half_home_team_overunder05})

                if market['entityName'] == f"{match['eventNames'][0]} Second Half Goals - Over/Under 1.5" and len(
                        market['outcomes']) == 2:
                    second_half_home_team_overunder15.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_home_team_overunder15": second_half_home_team_overunder15})

                if market['entityName'] == f"{match['eventNames'][0]} Second Half Goals - Over/Under 2.5" and len(
                        market['outcomes']) == 2:
                    second_half_home_team_overunder25.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_home_team_overunder25": second_half_home_team_overunder25})

                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 0.5" and len(
                        market['outcomes']) == 2:
                    second_half_away_team_overunder05.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_away_team_overunder05": second_half_away_team_overunder05})

                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 2.5" and len(
                        market['outcomes']) == 2:
                    second_half_away_team_overunder25.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_away_team_overunder25": second_half_away_team_overunder25})

                if market['entityName'] == f"{match['eventNames'][-1]} First Half Goals - Over/Under 1.5" and len(
                        market['outcomes']) == 2:
                    second_half_away_team_overunder15.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"second_half_away_team_overunder15": second_half_away_team_overunder15})

                if market['entityName'] == "Second Half Goals – odd/even" and len(market['outcomes']) == 2:
                    odd_even_secondhalf.extend(
                        (float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"odd_even_secondhalf": odd_even_secondhalf})

        if marketgroup['name'] == 'Goals':
            markets2 = marketgroup['markets']
            for market in markets2:
                if market['entityName'] == "First Team to Score" and len(market['outcomes']) == 3:
                    first_team_to_score.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"first_team_to_score": first_team_to_score})

                if market['entityName'] == "Last Team to Score" and len(market['outcomes']) == 3:
                    last_team_to_score.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"last_team_to_score": last_team_to_score})

                if market['entityName'] == f"{match['eventNames'][0]} - Clean Sheet - tcs" and len(market['outcomes']) == 2:
                    home_clean_sheet.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"home_clean_sheet": home_clean_sheet})

                if market['entityName'] == f"{match['eventNames'][-1]} - Clean Sheet - tcs" and len(market['outcomes']) == 2:
                    away_clean_sheet.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"away_clean_sheet": away_clean_sheet})

                if market['entityName'] == f"{match['eventNames'][0]} Total Goals Over/Under 1.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder15 = [float(ggyes), float(ggno)]
                    wager_types.append({"home_team_overunder15": away_team_overunder15})

                if market['entityName'] == f"{match['eventNames'][0]} Total Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder15 = [float(ggyes), float(ggno)]
                    wager_types.append({"home_team_overunder05": away_team_overunder15})

                if market['entityName'] == f"{match['eventNames'][0]} Total Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder15 = [float(ggyes), float(ggno)]
                    wager_types.append({"home_team_overunder25": away_team_overunder15})
                if market['entityName'] == f"{match['eventNames'][-1]} Total Goals - Over/Under 2.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder15 = [float(ggyes), float(ggno)]
                    wager_types.append({"away_team_overunder25": away_team_overunder15})
                if market['entityName'] == f"{match['eventNames'][-1]} Total Goals - Over/Under 1.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder15 = [float(ggyes), float(ggno)]
                    wager_types.append({"away_team_overunder15": away_team_overunder15})
                if market['entityName'] == f"{match['eventNames'][-1]} Total Goals - Over/Under 0.5" and len(market['outcomes']) == 2:
                    for x in market['outcomes']:
                        if x['id'].lower() == "over":
                            ggyes = x['value']
                        if x['id'].lower() == "under":
                            ggno = x['value']
                    away_team_overunder05 = [float(ggyes), float(ggno)]
                    wager_types.append({"away_team_overunder05": away_team_overunder05})


        if marketgroup['name'] == 'Others':
            markets2 = marketgroup['markets']
            for market in markets2:
                if market['entityName'] == f"{match['eventNames'][0]} Total Goals - Odd/Even":
                    hometeam_odd_even.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"hometeam_odd_even": hometeam_odd_even})

                if market['entityName'] == f"{match['eventNames'][-1]} Total Goals - Odd/Even":
                    awayteam_odd_even.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"awayteam_odd_even": awayteam_odd_even})

        if marketgroup['name'] == 'Corners':
            markets2 = marketgroup['markets']
            for market in markets2:
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213452:
                    corners_overunder65.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder65": corners_overunder65})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213453:
                    corners_overunder75.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder75": corners_overunder75})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213454:
                    corners_overunder85.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder85": corners_overunder85})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213456:
                    corners_overunder105.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder105": corners_overunder105})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213455:
                    corners_overunder95.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder95": corners_overunder95})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213457:
                    corners_overunder115.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder115": corners_overunder115})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213458:
                    corners_overunder125.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder125": corners_overunder125})
                if market['entityName'] == "Total Corners" and market['entityId'] == 107213459:
                    corners_overunder135.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
                    wager_types.append({"corners_overunder135": corners_overunder135})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 7":
                    corners_overunder7_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder7_3way": corners_overunder7_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 8":
                    corners_overunder8_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder8_3way": corners_overunder8_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 9":
                    corners_overunder9_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder9_3way": corners_overunder9_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 10":
                    corners_overunder10_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder10_3way": corners_overunder10_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 11":
                    corners_overunder11_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder11_3way": corners_overunder11_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 12":
                    corners_overunder12_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder12_3way": corners_overunder12_3way})

                if market['entityName'] == "3-Way Corners - Over/Exact/Under 13":
                    corners_overunder13_3way.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value']),float(market['outcomes'][2]['value'])))
                    wager_types.append({"corners_overunder13_3way": corners_overunder13_3way})


    handicap1 = []  # -1.5 / 1.5
    gg = [ggyes, ggno]
    away2_home1X = [away_odd, double_chance[0]]
    home1_awayX2 = [home_odd, double_chance[2]]
    X_away12 = [draw_odd, double_chance[1]]

    # wager_types.append({"21X": away2_home1X})
    # wager_types.append({"12X": home1_awayX2})
    # wager_types.append({"X12": X_away12})
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
        {"Scotland League Two": "SCOTLAND_LEAGUE_TWO"},
        {"Northern Ireland": "NORTHERN_IRELAND_PREMIER_LEAGUE"},
        {"France League One": "FR_L1"},
        {"France League Two": "FRANCE_LIGUE_2"},
        {"Laliga": "ES_PL"},
        {"Copa del Ray": "SPAIN_CUP"},
        {"Laliga 2": "SPAIN_SEGUNDA_DIVISION"},
        {"German Bundesliga": "DE_BL"},
        {"German Bundesliga 2": "GERMANY_BUNDESLIGA_2"},
        {"Italy Serie A": "IT_SA"},
        {"Italy Serie B": "ITALY_SERIE_B"},
        {"Italy Coppa Italia": "ITALY_CUP"},
        {"Netherlands Eredivisie": "NETHERLANDS_EREDIVISIE"},
        {"Greece Super League 1": "GREECE_SUPER_LEAGUE"},
        {"England FA": "EN_FA"},
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

