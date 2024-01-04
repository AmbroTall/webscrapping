import time
import pandas as pd
from SoccerArb.newbot.utils import map_teams, testing_function, request_function, convert_date_string_to_unix

def api_calls_events(code):
    url = f"https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID={code}&DISP=0&GROUPMARKETID=1&matches=false&v_cache_version=1.243.3.136"

    payload = {}
    headers = {
        'authority': 'sports.bet9ja.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'ftv=1; livlang=en; _gcl_au=1.1.1893408047.1698585396; cif_=1; _fbp=fb.1.1698585398451.455321226; _ga=GA1.1.1984204577.1698585399; _tgpc=b1eba940-5ef2-5ccf-877c-7b9aa248d76a; __adm_tid=tid-438ccd8f4.3844f2144; _hjSessionUser_95609=eyJpZCI6Ijk0NzAzMGQyLTI2OGEtNWY0YS04NjM2LWUyMzBhZDc1ZDdkMSIsImNyZWF0ZWQiOjE2OTg1ODUzOTg3NzAsImV4aXN0aW5nIjp0cnVlfQ==; landingRedirection=true; _tglksd={"s":"bc39d115-6819-5732-8290-21c4dabcbf69","st":1699440490110,"sod":"www.google.com","sodt":1698845764718,"sods":"r","sodst":1699440490110}; cto_bundle=dEpotl9mcE5oM0xseWtNRHlwOU9SSXFtVjN5cW9vejhTZSUyQkZOVUQlMkZNYWolMkJEMDEwcFJEelZWZXIyNW5nalVONTUxJTJGSDFib3FpbXIxd0U5SE9aYW9EQ3V0SDJZSjJTeTc2c2FCR3JleklESXYzZGhIYU1OSW10WVFYSlNPemJXZ09sdW14bG5jcDJSakFocG5pNVJvU0licjNzUSUzRCUzRA; _sp_srt_id.55ca=e00f74b1-f798-47a8-94ea-33a5efd061cb.1698585400.8.1699440494.1698846309.5a4139c0-de60-4913-bbad-7bc480ade72a.aa06a281-1265-4935-9ea1-60b52d8f194f...0; MgidSensorNVis=56; MgidSensorHref=https://sports.bet9ja.com/searchResults/; _ga_YYQNLHMCQS=GS1.1.1699449382.10.0.1699449382.0.0.0; ak_bmsc=1F8AEEBCD815DD7E1C23C52D7D74F83C~000000000000000000000000000000~YAAQBqERAuW5u3mLAQAAXZZpuBVLwQ8rrYEbbFXtHsErn0/r0gmDDtO9LMrzz/AkWWy9KyMF4+Fl1sboO8A6HSm/5GOg+aghm6ZxzxLgKPjlZ2skN46zxtRH5xOj5yHMgBxfnSRZKNH4ibaFORhKlzJ45K7UYd30Kz6s8tMWi9QI4aR+dy2xMs8HZB8kAj0sQP90P+/zfFoMCnHpp09Zjv5XPsR37aRoegoVyVqG1emqpBfdp+qkJiKy9oRrBpA9VqScHs665qBM+o2j8X32X2eIUrxBykRGuYiONH1TmOT2a74S4Hh0Q+LUdfVkcljgsVhX8Zv6yvs4diq9dpjSpqgAGmSw0Ma3T2PtydDIUEyhuA3THWGcMv0JjsOdspnIEuM7viAXAyeSzSo=; bm_sv=2AADC797E7BDA801B58E543B6AB01872~YAAQVkM0F5i3crWLAQAAyuR5uBU9oY7xPbfgGC5BKV7PK2JO2BvR9F6kePtDZ193FmooqK3+nTw8DR2dNafv6QWtDxYmODAcrgltP+kjYeEPUAVSagHHUMjjmR6qOoZAPn1VayVEViyF4Yukme5qFsrPsohCnyqZ9imczvIPQ9C7TKmusDgyBHRoJbH16bARVAaoykzFqX2Xm9Or7DqHUSGYWjetrbyQBcgKTHrIbV16O4kH6naeRj66yse7O8Rv~1',
        'referer': 'https://sports.bet9ja.com/competition/soccer/england/championship/1-11058-170881',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = request_function(url, headers, payload)
    return response['D']['E']


def api_call_odds(match_id):
    url = f"https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEvent?EVENTID={match_id}&v_cache_version=1.243.3.136"

    payload = {}
    headers = {
        'authority': 'sports.bet9ja.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'ftv=1; livlang=en; _gcl_au=1.1.1893408047.1698585396; cif_=1; _fbp=fb.1.1698585398451.455321226; _ga=GA1.1.1984204577.1698585399; _tgpc=b1eba940-5ef2-5ccf-877c-7b9aa248d76a; __adm_tid=tid-438ccd8f4.3844f2144; _hjSessionUser_95609=eyJpZCI6Ijk0NzAzMGQyLTI2OGEtNWY0YS04NjM2LWUyMzBhZDc1ZDdkMSIsImNyZWF0ZWQiOjE2OTg1ODUzOTg3NzAsImV4aXN0aW5nIjp0cnVlfQ==; landingRedirection=true; _tglksd={"s":"bc39d115-6819-5732-8290-21c4dabcbf69","st":1699440490110,"sod":"www.google.com","sodt":1698845764718,"sods":"r","sodst":1699440490110}; cto_bundle=dEpotl9mcE5oM0xseWtNRHlwOU9SSXFtVjN5cW9vejhTZSUyQkZOVUQlMkZNYWolMkJEMDEwcFJEelZWZXIyNW5nalVONTUxJTJGSDFib3FpbXIxd0U5SE9aYW9EQ3V0SDJZSjJTeTc2c2FCR3JleklESXYzZGhIYU1OSW10WVFYSlNPemJXZ09sdW14bG5jcDJSakFocG5pNVJvU0licjNzUSUzRCUzRA; _sp_srt_id.55ca=e00f74b1-f798-47a8-94ea-33a5efd061cb.1698585400.8.1699440494.1698846309.5a4139c0-de60-4913-bbad-7bc480ade72a.aa06a281-1265-4935-9ea1-60b52d8f194f...0; MgidSensorNVis=56; MgidSensorHref=https://sports.bet9ja.com/searchResults/; _ga_YYQNLHMCQS=GS1.1.1699449382.10.0.1699449382.0.0.0; bm_mi=E36C4C16362D28D2A477B8A9EB968055~YAAQBqERAnG8u3mLAQAA5MeduBXSROQ4hdvT0ffeobBWYukGZzWWwJNlBQ0KMoxow3BvI2iLY+G8EjkDiL0RgypLknO4zGVnlx2BqGLpi2aUTTwGS7QaKzftRQ7NiNM2qx6L3QOUnR4xLcABMhOXU706I9aI1OGnUf3R1aCQM3cXwWxJJ4pO3NvKW0c8wAVHQJUigpZtPx7p+fzgqEU70ZHyRcl2BkxRPyvKW1LDBiGGM4RDJ8FRqMLvybF4Bwl0dpq+Ps6kozS+lta/GklMrDB92qLGu8pFcq34zDmFu29KMkYneDBVc7Fn0miL7G2AeMrADIcqPObj/pHjcQ==~1; ak_bmsc=1F8AEEBCD815DD7E1C23C52D7D74F83C~000000000000000000000000000000~YAAQBqERAnW8u3mLAQAAr9WduBWXQwv72rlCFujOg7n1rlWg2CF7SHz7ukuXjTZoYlC+5XsFjgRu+CS+UPUjbp+bwoC65P2ypcrm6RYu4112Ev47DSOq6YaMMO38/VTr2cYPimJPlg115ctDmklBCnKIhF2fhffZBpxLhkxiT2yIZcw7IMD7TpJNUbmHN6pwSBkMaDOK0OFmR6oJYCSUGdGFZPv7BdVv24EWTAHIcWPU2+6tYBaaWRfMq+M1am8emwDynczAMnczmKqtjHvYQ6wC4MDxzEWEDpLEG1uAVqZ9MIH9WtS8TyrnfabLx3vXJvNlyMTeyZIGGAsO1ISdWEFSQYUPw511XHWvB/TCCvGDbNbDtJWsNXeGFq3uSKen1kXlvnsroYsPZwvN8J2dWC9nmLfX2PUHRBWTMBkr4C3YoPltGLPNzBuVBb2oZEdQ9rNUxYOKha1LEZZW1EBFYrzhS8ExH7/qVp/j90hf5QWsfxoGKOIphFvDRrb7esg6MPvDFHDcJSPezFyTuy37l7Seq3bNE1NHyzFmZ5DI90FwRog=; bm_sv=2AADC797E7BDA801B58E543B6AB01872~YAAQBqERAni8u3mLAQAAQd2duBVbC5eCjCKRK5Lax8jfhghObO3vaKlESZtL3BHS1lC8vcLGGjlbaeX+ZbmAmk/rD2DOfMlIATLWjkFVpfo7BWIr8XfULGBKTqcXNOQ3Zyt4lVdPGI4bTfTTlS38j5bE092CM5xi+ZhpUrBtwJUftBsL8aivUhKBTIr78opeVHjLpb6t/JRVwX+ZzNTkJzFAXpSu2F46JKmcOHYGl5DBwvdq4dD897M1bI6girdnVQ==~1',
        'referer': 'https://sports.bet9ja.com/event/361869804',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response['D']['O']


def exctract_odds(match, league, bookie_name):
    games = {}
    wager_types = []
    draw_no_bet = []
    draw_no_bet_first_half = []
    double_chance = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five = []
    over_one_five_first_half = []
    over_two_five = []
    over_two_five_first_half = []
    over_three_five = []
    over_four_five = []
    over_five_five = []
    fasthalf1X2 = []
    fasthalf_dc = []
    gg = []
    gg_firsthalf = []
    odd_even = []
    odd_even_firsthalf = []
    first_team_to_score = []  # hometeam, draw, away_team
    home_team_overunder15 = []
    home_team_overunder25 = []
    home_team_overunder05 = []
    away_team_overunder15 = []
    away_team_overunder25 = []
    away_team_overunder05 = []

    teams = match['DS'].split(' - ')

    games['match_id'] = match['ID']
    # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)
    #
    # # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(teams[0].strip(), teams[0].strip())
    # games['away_team'] = team_mapping.get(teams[1].strip(), teams[1].strip())

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = teams[0].strip()
    games['away_team'] = teams[1].strip()

    games['time'] = convert_date_string_to_unix(match['STARTDATE'])

    odds = api_call_odds(match['ID'])

    if ('S_1X2_1' in odds and 'S_1X2_2' in odds and 'S_1X2_X' in odds):
        h_odd = float(odds['S_1X2_1'])
        a_odd = float(odds['S_1X2_2'])
        d_odd = float(odds['S_1X2_X'])
        home_draw_away = [h_odd, d_odd, a_odd]
        wager_types.append({"1X2": home_draw_away})
    if ('S_DC_1X' in odds and 'S_DC_X2' in odds and 'S_DC_12' in odds):
        double_chance.extend((float(odds['S_DC_1X']), float(odds['S_DC_12']), float(odds['S_DC_X2'])))
        wager_types.append({"double_chance": double_chance})
    if ('S_OU@2.5_O' in odds and 'S_OU@2.5_U' in odds):
        over_two_five.extend((float(odds['S_OU@2.5_O']), float(odds['S_OU@2.5_U'])))
        wager_types.append({"over_two_five": over_two_five})
    if ('S_OU1T@2.5_O' in odds and 'S_OU1T@2.5_U' in odds):
        over_two_five_first_half.extend((float(odds['S_OU1T@2.5_O']), float(odds['S_OU1T@2.5_U'])))
        wager_types.append({"over_two_five_first_half": over_two_five_first_half})
    if ('S_OU1T@1.5_O' in odds and 'S_OU1T@1.5_U' in odds):
        over_one_five_first_half.extend((float(odds['S_OU1T@1.5_O']), float(odds['S_OU1T@1.5_U'])))
        wager_types.append({"over_one_five_first_half": over_one_five_first_half})
    if ('S_OU1T@0.5_O' in odds and 'S_OU1T@0.5_U' in odds):
        over_ofive_five_first_half.extend((float(odds['S_OU1T@0.5_O']), float(odds['S_OU1T@0.5_U'])))
        wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})
    if ('S_OU@0.5_O' in odds and 'S_OU@0.5_U' in odds):
        over_ofive_five.extend((float(odds['S_OU@0.5_O']), float(odds['S_OU@0.5_U'])))
        wager_types.append({"over_ofive_five": over_ofive_five})
    if ('S_OU@1.5_O' in odds and 'S_OU@1.5_U' in odds):
        over_one_five.extend((float(odds['S_OU@1.5_O']), float(odds['S_OU@1.5_U'])))
        wager_types.append({"over_one_five": over_one_five})
    if ('S_OU@3.5_O' in odds and 'S_OU@3.5_U' in odds):
        over_three_five.extend((float(odds['S_OU@3.5_O']), float(odds['S_OU@3.5_U'])))
        wager_types.append({"over_three_five": over_three_five})

    if ('S_HAOU@0.5_OA' in odds and 'S_HAOU@0.5_UA' in odds):
        away_team_overunder05.extend((float(odds['S_HAOU@0.5_OA']), float(odds['S_HAOU@0.5_UA'])))
        wager_types.append({"away_team_overunder05": away_team_overunder05})
    if ('S_HAOU@1.5_OA' in odds and 'S_HAOU@1.5_UA' in odds):
        away_team_overunder15.extend((float(odds['S_HAOU@1.5_OA']), float(odds['S_HAOU@1.5_UA'])))
        wager_types.append({"away_team_overunder15": away_team_overunder15})
    if ('S_HAOU@2.5_OA' in odds and 'S_HAOU@2.5_UA' in odds):
        away_team_overunder25.extend((float(odds['S_HAOU@2.5_OA']), float(odds['S_HAOU@2.5_UA'])))
        wager_types.append({"away_team_overunder25": away_team_overunder25})

    if ('S_HAOU@0.5_OH' in odds and 'S_HAOU@0.5_UH' in odds):
        home_team_overunder05.extend((float(odds['S_HAOU@0.5_OH']), float(odds['S_HAOU@0.5_UH'])))
        wager_types.append({"home_team_overunder05": home_team_overunder05})
    if ('S_HAOU@1.5_OH' in odds and 'S_HAOU@1.5_UH' in odds):
        home_team_overunder15.extend((float(odds['S_HAOU@1.5_OH']), float(odds['S_HAOU@1.5_UH'])))
        wager_types.append({"home_team_overunder15": home_team_overunder15})
    if ('S_HAOU@2.5_OH' in odds and 'S_HAOU@2.5_UH' in odds):
        home_team_overunder25.extend((float(odds['S_HAOU@2.5_OH']), float(odds['S_HAOU@2.5_UH'])))
        wager_types.append({"home_team_overunder25": home_team_overunder25})



    if ('S_OU@4.5_O' in odds and 'S_OU@4.5_U' in odds):
        over_four_five.extend((float(odds['S_OU@4.5_O']), float(odds['S_OU@4.5_U'])))
        wager_types.append({"over_four_five": over_four_five})

    if ('S_OU@5.5_O' in odds and 'S_OU@5.5_U' in odds):
        over_five_five.extend((float(odds['S_OU@5.5_O']), float(odds['S_OU@5.5_U'])))
        wager_types.append({"over_five_five": over_five_five})

    if ('S_DNB_1' in odds and 'S_DNB_2' in odds):
        draw_no_bet.extend((float(odds['S_DNB_1']), float(odds['S_DNB_2'])))
        wager_types.append({"draw_no_bet": draw_no_bet})
    if ('S_DNB1T_1' in odds and 'S_DNB1T_2' in odds):
        draw_no_bet_first_half.extend((float(odds['S_DNB1T_1']), float(odds['S_DNB1T_2'])))
        wager_types.append({"draw_no_bet_first_half": draw_no_bet_first_half})
    if ('S_1X21T_1' in odds and 'S_1X21T_2' in odds and 'S_1X21T_X' in odds):
        fasthalf1X2.extend((float(odds['S_1X21T_1']), float(odds['S_1X21T_X']), float(odds['S_1X21T_2'])))
        wager_types.append({"fasthalf1X2": fasthalf1X2})
    if ('S_DC1T_1X' in odds and 'S_DC1T_12' in odds and 'S_DC1T_X2' in odds):
        fasthalf_dc.extend((float(odds['S_DC1T_1X']), float(odds['S_DC1T_12']), float(odds['S_DC1T_X2'])))
        wager_types.append({"fasthalf_dc": fasthalf_dc})
    if ('S_GGNG_Y' in odds and 'S_GGNG_N' in odds):
        gg.extend((float(odds['S_GGNG_Y']), float(odds['S_GGNG_N'])))
        wager_types.append({"gg": gg})
    if ('S_OE_EV' in odds and 'S_OE_OD' in odds):
        odd_even.extend((float(odds['S_OE_OD']), float(odds['S_OE_EV'])))
        wager_types.append({"odd_even": odd_even})
    if ('S_GGNG1T_Y' in odds and 'S_GGNG1T_N' in odds):
        gg_firsthalf.extend((float(odds['S_GGNG1T_Y']), float(odds['S_GGNG1T_N'])))
        wager_types.append({"gg_firsthalf": gg_firsthalf})
    if ('S_OE1T_OD' in odds and 'S_OE1T_EV' in odds):
        odd_even_firsthalf.extend((float(odds['S_OE1T_OD']), float(odds['S_OE1T_EV'])))
        wager_types.append({"odd_even_firsthalf": odd_even_firsthalf})
    if ('S_1STGOAL_1' in odds and 'S_1STGOAL_X' in odds and 'S_1STGOAL_2' in odds):
        first_team_to_score.extend((float(odds['S_1STGOAL_1']), float(odds['S_1STGOAL_X']), float(odds['S_1STGOAL_2'])))
        wager_types.append({"first_team_to_score": first_team_to_score})

    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    # try:
    #     for x in wager_types:
    #         for key, value in x.items():
    #             if key == "1X2":
    #                 away_odd = value[-1]
    #                 home_odd = value[0]
    #                 draw_odd = value[1]
    #             if key == "double_chance":
    #                 double_chance1X = value[0]
    #                 double_chance12 = value[1]
    #                 double_chanceX2 = value[2]
    #     away2_home1X = [away_odd, double_chance1X]
    #     home1_awayX2 = [home_odd, double_chanceX2]
    #     X_away12 = [draw_odd, double_chance12]
    #     wager_types.append({"21X": away2_home1X})
    #     wager_types.append({"12X": home1_awayX2})
    #     wager_types.append({"X12": X_away12})
    # except:
    #     pass

    games['wager_types'] = wager_types
    return games


def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()

    for match_detail in match_details:
        teams = match_detail['DS'].split(' - ')
        home_team = teams[0].strip()
        away_team = teams[1].strip()

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
        return league_name, league_id


def main():
    bookie_name = 'bet9ja'
    # leagues = [{"England Premier League": 170880} ]
    leagues = [{"England Premier League": 170880}, {"England Championship": 170881}, {"England League One": 995354},
               {"England League Two": 995355}, {"Scotland Premiership": 941378}, {"Scotland Championship": 1075222},
               {"Scotland League One": 1076436}, {"Scotland League Two": 1076689}, {"Northern Ireland":1078221},{"France League One": 950503},{"France League Two":958691},{"Laliga":180928},{"Laliga 2":180929}, {"Japan League": 1787481}, {"German Bundesliga":180923}, {"German Bundesliga 2":180924},{"German DFB Pokal":180924}, {"Italy Serie A": 167856}, {"Italy Serie B": 907202}, {"Italy Coppa Italia": 1042342}, {"Netherlands Eredivisie" : 1016657},{"Greece Super League 1": 1018979},{"England FA":708732},{"Copa del Ray": 1125043}]

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
                # +++++++++++++ BenchMark +++++++++++++
                # "Northern Ireland": "Northern Ireland",
                # "France League One": "France League One",
                # "France League One": "France League One",
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
                    league_wager_dic = exctract_odds(match, league_name, bookie_name)

                    league_data.append(league_wager_dic)
                except Exception as e:
                    continue
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("bet9ja", bookmaker_data)
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
