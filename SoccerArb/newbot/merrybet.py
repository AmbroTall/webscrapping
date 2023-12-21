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

    draw_no_bet_first_half = []
    draw_no_bet_second_half = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_ofive_five_second_half = []
    over_one_five_second_half = []
    over_two_five_second_half = []
    over_four_five = []
    over_five_five = []
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
        if (eventgame['gameName'] == "1st half - Double chance"):
            fasthalf_dc.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))
        if (eventgame['gameName'] == "2nd half - Double chance"):
            secondhalf_dc.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 2.5 goals"):
            over_two_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 0.5 goals"):
            over_ofive_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 1.5 goals"):
            over_one_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))

        if (eventgame['gameName'] == "2nd half - 1x2"):
            second1X2.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))

        if (eventgame['gameName'] == "1st goal"):
            first_team_to_score.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))

        if (eventgame['gameName'] == "Last goal"):
            last_team_to_score.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))



        if (eventgame['gameName'] == "1st half - 1st goal"):
            first_team_to_score_1st_half.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))

        if (eventgame['gameName'] == "2nd half - 1st goal"):
            first_team_to_score_2nd_half.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds']))

        if (eventgame['gameName'] == "1st half - Under/Over 0.5 goals"):
            over_ofive_five_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "1st half - Under/Over 1.5 goals"):
            over_one_five_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "1st half - Under/Over 2.5 goals"):
            over_two_five_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"1st half - {name[0].strip()} Under/Over 0.5"):
            first_half_home_team_overunder05.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == f"1st half - {name[0].strip()} Under/Over 1.5"):
            first_half_home_team_overunder15.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == f"1st half - {name[0].strip()} Under/Over 2.5"):
            first_half_home_team_overunder25.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"1st half - {name[1].strip()} Under/Over 0.5"):
            first_half_away_team_overunder05.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == f"1st half - {name[1].strip()} Under/Over 1.5"):
            first_half_away_team_overunder15.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == f"1st half - {name[1].strip()} Under/Over 2.5"):
            first_half_away_team_overunder25.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))


        if (eventgame['gameName'] == f"2nd half - {name[0].strip()} Under/Over 0.5 goals"):
            second_half_home_team_overunder05.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == f"2nd half - {name[0].strip()} Under/Over 1.5 goals"):
            second_half_home_team_overunder15.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == f"2nd half - {name[0].strip()} Under/Over 2.5 goals"):
            second_half_home_team_overunder25.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))

        if (eventgame['gameName'] == f"2nd half - {name[1].strip()} Under/Over 0.5 goals"):
            second_half_away_team_overunder05.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == f"2nd half - {name[1].strip()} Under/Over 1.5 goals"):
            second_half_away_team_overunder15.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == f"2nd half - {name[1].strip()} Under/Over 2.5 goals"):
            second_half_away_team_overunder25.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))

        if (eventgame['gameName'] == "2nd half - Under/Over 0.5 goals"):
            over_ofive_five_second_half.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "2nd half - Under/Over 1.5 goals"):
            over_one_five_second_half.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "2nd half - Under/Over 2.5 goals"):
            over_two_five_second_half.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))

        if (eventgame['gameName'] == "1st half - Draw no bet"):
            draw_no_bet_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == "2nd half - Draw no bet"):
            draw_no_bet_second_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == "1st half - Both teams to score"):
            gg_firsthalf.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == "2nd half - Both teams to score"):
            gg_secondhalf.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[0].strip()} Under/Over 1.5 goals"):
            home_team_overunder15.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[0].strip()} - Odd/Even"):
            hometeam_odd_even.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[1].strip()} - Odd/Even"):
            awayteam_odd_even.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[0].strip()} clean sheet"):
            home_clean_sheet.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[1].strip()} clean sheet"):
            away_clean_sheet.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"1st half - {name[0].strip()} clean sheet"):
            home_clean_sheet_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"1st half - {name[1].strip()} clean sheet"):
            away_clean_sheet_first_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"2nd half - {name[0].strip()} clean sheet"):
            home_clean_sheet_second_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"2nd half - {name[1].strip()} clean sheet"):
            away_clean_sheet_second_half.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))



        if (eventgame['gameName'] == f"{name[0].strip()} Under/Over 0.5 goals"):
            home_team_overunder05.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[0].strip()} Under/Over 2.5 goals"):
            home_team_overunder25.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[1].strip()} Under/Over 1.5 goals"):
            away_team_overunder15.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[1].strip()} Under/Over 0.5 goals"):
            away_team_overunder05.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))

        if (eventgame['gameName'] == f"{name[1].strip()} Under/Over 2.5 goals"):
            away_team_overunder25.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "Total goals - Odd/Even"):
            odd_even.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "1st half - Odd/Even"):
            odd_even_firsthalf.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "2nd half - Odd/Even"):
            odd_even_secondhalf.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 4.5 goals"):
            over_four_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if (eventgame['gameName'] == "Under/Over 5.5 goals"):
            over_five_five.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
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
    wager_types.append({"draw_no_bet_first_half": draw_no_bet_first_half})
    wager_types.append({"draw_no_bet_second_half": draw_no_bet_second_half})
    wager_types.append({"over_ofive_five": over_ofive_five})
    wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})
    wager_types.append({"over_one_five_first_half": over_one_five_first_half})
    wager_types.append({"over_two_five_first_half": over_two_five_first_half})
    wager_types.append({"over_ofive_five_second_half": over_ofive_five_second_half})
    wager_types.append({"over_one_five_second_half": over_one_five_second_half})
    wager_types.append({"over_two_five_second_half": over_two_five_second_half})
    wager_types.append({"over_four_five": over_four_five})
    wager_types.append({"over_five_five": over_five_five})
    wager_types.append({"fasthalf_dc": fasthalf_dc})
    wager_types.append({"secondhalf_dc": secondhalf_dc})
    wager_types.append({"gg_firsthalf": gg_firsthalf})
    wager_types.append({"gg_secondhalf": gg_secondhalf})
    wager_types.append({"odd_even": odd_even})
    wager_types.append({"odd_even_firsthalf": odd_even_firsthalf})
    wager_types.append({"odd_even_secondhalf": odd_even_secondhalf})
    wager_types.append({"hometeam_odd_even": hometeam_odd_even})
    wager_types.append({"awayteam_odd_even": awayteam_odd_even})
    wager_types.append({"first_team_to_score": first_team_to_score})
    wager_types.append({"first_team_to_score_1st_half": first_team_to_score_1st_half})
    wager_types.append({"first_team_to_score_2nd_half": first_team_to_score_2nd_half})
    wager_types.append({"last_team_to_score": last_team_to_score})
    wager_types.append({"home_team_overunder15": home_team_overunder15})
    wager_types.append({"home_team_overunder25": home_team_overunder25})
    wager_types.append({"home_team_overunder05": home_team_overunder05})
    wager_types.append({"away_team_overunder15": away_team_overunder15})
    wager_types.append({"away_team_overunder25": away_team_overunder25})
    wager_types.append({"away_team_overunder05": away_team_overunder05})
    wager_types.append({"home_clean_sheet": home_clean_sheet})
    wager_types.append({"away_clean_sheet": away_clean_sheet})
    wager_types.append({"home_clean_sheet_first_half": home_clean_sheet_first_half})
    wager_types.append({"away_clean_sheet_first_half": away_clean_sheet_first_half})
    wager_types.append({"home_clean_sheet_second_half": home_clean_sheet_second_half})
    wager_types.append({"away_clean_sheet_second_half": away_clean_sheet_second_half})
    wager_types.append({"first_half_home_team_overunder15": first_half_home_team_overunder15})
    wager_types.append({"first_half_home_team_overunder25": first_half_home_team_overunder25})
    wager_types.append({"first_half_home_team_overunder05": first_half_home_team_overunder05})
    wager_types.append({"first_half_away_team_overunder15": first_half_away_team_overunder15})
    wager_types.append({"first_half_away_team_overunder25": first_half_away_team_overunder25})
    wager_types.append({"first_half_away_team_overunder05": first_half_away_team_overunder05})
    wager_types.append({"second_half_home_team_overunder15": second_half_home_team_overunder15})
    wager_types.append({"second_half_home_team_overunder25": second_half_home_team_overunder25})
    wager_types.append({"second_half_home_team_overunder05": second_half_home_team_overunder05})
    wager_types.append({"second_half_away_team_overunder15": second_half_away_team_overunder15})
    wager_types.append({"second_half_away_team_overunder25": second_half_away_team_overunder25})
    wager_types.append({"second_half_away_team_overunder05": second_half_away_team_overunder05})
    wager_types.append({"second1X2": second1X2})
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
