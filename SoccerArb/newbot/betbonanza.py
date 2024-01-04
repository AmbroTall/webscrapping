from SoccerArb.newbot.utils import map_teams, testing_function, request_function,converting_time_string
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time

MAX_RETRIES = 3
TIMEOUT_LIMIT = 120  # 2 minutes

def api_calls_events(code):
    url = f"https://pre-98o-sp.websbkt.com/cache/98/en/ke/{code}/prematch-by-tournaments.json?hidenseek=7fbf4210110daa1e4216b66eeb1fcefb6a143918"

    payload = {}
    headers = {
        'authority': 'pre-98o-sp.websbkt.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://betbonanza.com',
        'referer': 'https://betbonanza.com/',
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
    url = f"https://pre-98o-sp.websbkt.com/cache/98/en/ke/{match_id}/single-pre-event.json?hidenseek=7fbf4654210110daa1e4216b66eeb1fcefb6a1439184"

    payload = {}
    headers = {
        'authority': 'pre-98o-sp.websbkt.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/"13dfb5-G9hx+XmrMnSVzYpttv0rPA"',
        'origin': 'https://betbonanza.com',
        'referer': 'https://betbonanza.com/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = request_function(url, headers, payload)
    return response

def exctract_odds(match, league, bookie_name):
    games = {}
    wager_types = []
    draw_no_bet = []
    home_draw_away = []

    draw_no_bet_first_half = []
    double_chance = []
    fasthalf_dc = []
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
    gg = []
    gg_firsthalf = []
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
    # Get the team mapping for the specified bookie and league
    # team_mapping = map_teams(bookie_name, league)
    #
    # # Use the default team names if mapping is available, otherwise use the original names
    # games['home_team'] = team_mapping.get(match['teams']['home'], match['teams']['home'])
    # games['away_team'] = team_mapping.get(match['teams']['away'], match['teams']['away'])
    #
    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] =  match['teams']['home']
    games['away_team'] =  match['teams']['away']

    date_start = match['date_start']
    games['time'] = converting_time_string(date_start)

    odds_market = api_call_odds(match['id'])
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    for key, value in odds_market['odds'].items():
        default_name = value.get('defaultName', '')
        additional_value = value.get('additional_value', '')
        odd_code = value.get('odd_code', '')
        # Check if defaultName is 'Over'
        if default_name == f"Draw No Bet - {match['teams']['home']}":
            odd_value = value.get('odd_value')
            draw_no_bet_home = round(odd_value, 2)
            draw_no_bet.insert(0, draw_no_bet_home)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == f"Draw No Bet - {match['teams']['away']}":
            odd_value = value.get('odd_value')
            draw_no_bet_away= round(odd_value, 2)
            draw_no_bet.insert(2, draw_no_bet_away)


        if default_name == f"1st half Draw No Bet - {match['teams']['home']}":
            odd_value = value.get('odd_value')
            draw_no_bet_home_fh = round(odd_value, 2)
            draw_no_bet_first_half.insert(0, draw_no_bet_home_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == f"1st half Draw No Bet - {match['teams']['away']}":
            odd_value = value.get('odd_value')
            draw_no_bet_away_fh= round(odd_value, 2)
            draw_no_bet_first_half.insert(2, draw_no_bet_away_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "1X":
            odd_value = value.get('odd_value')
            double_chance1X = round(odd_value, 2)
            double_chance.insert(0, double_chance1X)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "12":
            odd_value = value.get('odd_value')
            double_chance12 = round(odd_value, 2)
            double_chance.insert(1, double_chance12)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "X2":
            odd_value = value.get('odd_value')
            double_chanceX2 = round(odd_value, 2)
            double_chance.insert(2, double_chanceX2)


        if default_name == "1st half result - 1X":
            odd_value = value.get('odd_value')
            double_chance1X_fh = round(odd_value, 2)
            fasthalf_dc.insert(0, double_chance1X_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "1st half result - 12":
            odd_value = value.get('odd_value')
            double_chance12_fh = round(odd_value, 2)
            fasthalf_dc.insert(1, double_chance12_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "1st half result - X2":
            odd_value = value.get('odd_value')
            double_chanceX2_fh = round(odd_value, 2)
            fasthalf_dc.insert(2, double_chanceX2_fh)



        if default_name == f"{match['teams']['home']} to score 1st goal in 1st half":
            odd_value = value.get('odd_value')
            first_goal_home_fh = round(odd_value, 2)
            first_team_to_score_first_half.insert(0, first_goal_home_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "No goals in first half time":
            odd_value = value.get('odd_value')
            first_goal_no_fh = round(odd_value, 2)
            first_team_to_score_first_half.insert(1, first_goal_no_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == f"{match['teams']['away']} to score 1st goal in 1st half":
            odd_value = value.get('odd_value')
            first_goal_away_fh = round(odd_value, 2)
            first_team_to_score_first_half.insert(2, first_goal_away_fh)



        if default_name == f"{match['teams']['home']} to score first goal":
            odd_value = value.get('odd_value')
            first_goal_home = round(odd_value, 2)
            first_team_to_score.insert(0, first_goal_home)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "No goals" and odd_code == 'ODD_FTB_FIRSTGOAL_NONE':
            odd_value = value.get('odd_value')
            first_goal_no = round(odd_value, 2)
            first_team_to_score.insert(1, first_goal_no)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == f"{match['teams']['away']} to score first goal":
            odd_value = value.get('odd_value')
            first_goal_away = round(odd_value, 2)
            first_team_to_score.insert(2, first_goal_away)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "1.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_one_five_o = round(odd_value, 2)
            over_one_five.insert(0, over_one_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "1.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_one_five_u = round(odd_value, 2)
            over_one_five.insert(1, over_one_five_u)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_ofive_five_o = round(odd_value, 2)
            over_ofive_five.insert(0, over_ofive_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_ofive_five_u = round(odd_value, 2)
            over_ofive_five.insert(1, over_ofive_five_u)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == "1st half total OVER":
            odd_value = value.get('odd_value')
            over_ofive_five_o_fh = round(odd_value, 2)
            over_ofive_five_first_half.insert(0, over_ofive_five_o_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == "1st half total UNDER":
            odd_value = value.get('odd_value')
            over_ofive_five_u_fh = round(odd_value, 2)
            over_ofive_five_first_half.insert(1, over_ofive_five_u_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "1.5" and default_name == "1st half total OVER":
            odd_value = value.get('odd_value')
            over_one_five_o_fh = round(odd_value, 2)
            over_one_five_first_half.insert(0, over_one_five_o_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "1.5" and default_name == "1st half total UNDER":
            odd_value = value.get('odd_value')
            over_one_five_u_fh = round(odd_value, 2)
            over_one_five_first_half.insert(1, over_one_five_u_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "2.5" and default_name == "1st half total OVER":
            odd_value = value.get('odd_value')
            over_two_five_o_fh = round(odd_value, 2)
            over_two_five_first_half.insert(0, over_two_five_o_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "2.5" and default_name == "1st half total UNDER":
            odd_value = value.get('odd_value')
            over_two_five_u_fh = round(odd_value, 2)
            over_two_five_first_half.insert(1, over_two_five_u_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "2.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_two_five_o = round(odd_value, 2)
            over_two_five.insert(0, over_two_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "2.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_two_five_u = round(odd_value, 2)
            over_two_five.insert(1, over_two_five_u)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "3.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_three_five_o = round(odd_value, 2)
            over_three_five.insert(0, over_three_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "3.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_three_five_u = round(odd_value, 2)
            over_three_five.insert(1, over_three_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "4.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_four_five_o = round(odd_value, 2)
            over_four_five.insert(0, over_four_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "4.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_four_five_u = round(odd_value, 2)
            over_four_five.insert(1, over_four_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "5.5" and default_name == "Total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            over_five_five.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "5.5" and default_name == "Total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            over_five_five.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "1.5" and default_name == f"{match['teams']['home']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            home_team_overunder15.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "1.5" and default_name == f"{match['teams']['home']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            home_team_overunder15.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "2.5" and default_name == f"{match['teams']['home']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            home_team_overunder25.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "2.5" and default_name == f"{match['teams']['home']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            home_team_overunder25.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "0.5" and default_name == f"{match['teams']['home']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            home_team_overunder05.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == f"{match['teams']['home']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            home_team_overunder05.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "1.5" and default_name == f"{match['teams']['away']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            away_team_overunder15.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "1.5" and default_name == f"{match['teams']['away']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            away_team_overunder15.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "2.5" and default_name == f"{match['teams']['away']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            away_team_overunder25.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "2.5" and default_name == f"{match['teams']['away']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            away_team_overunder25.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if additional_value.strip() == "0.5" and default_name == f"{match['teams']['away']} total OVER":
            odd_value = value.get('odd_value')
            over_five_five_o = round(odd_value, 2)
            away_team_overunder05.insert(0, over_five_five_o)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if additional_value.strip() == "0.5" and default_name == f"{match['teams']['away']} total UNDER":
            odd_value = value.get('odd_value')
            over_five_five_u = round(odd_value, 2)
            away_team_overunder05.insert(1, over_five_five_u)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")







        if  default_name == f"1st half result - {match['teams']['home']}":
            odd_value = value.get('odd_value')
            fasthalf1 = round(odd_value, 2)
            fasthalf1X2.insert(0, fasthalf1)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if default_name == f"1st half result - {match['teams']['away']}":
            odd_value = value.get('odd_value')
            fasthalf2 = round(odd_value, 2)
            fasthalf1X2.insert(2, fasthalf2)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == f"1st half result - X":
            odd_value = value.get('odd_value')
            fasthalfX = round(odd_value, 2)
            fasthalf1X2.insert(1, fasthalfX)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Both teams to score - YES":
            odd_value = value.get('odd_value')
            ggyes = round(odd_value, 2)
            gg.insert(0, ggyes)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Both teams to score - NO":
            odd_value = value.get('odd_value')
            ggno = round(odd_value, 2)
            gg.insert(1, ggno)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Both teams to score in 1st half - YES":
            odd_value = value.get('odd_value')
            ggyes_fh = round(odd_value, 2)
            gg_firsthalf.insert(0, ggyes_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Both teams to score in 1st half - NO":
            odd_value = value.get('odd_value')
            ggno_fh = round(odd_value, 2)
            gg_firsthalf.insert(1, ggno_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")


        # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "1st half total Odd":
            odd_value = value.get('odd_value')
            odd_fh = round(odd_value, 2)
            odd_even_firsthalf.insert(0, odd_fh)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "1st half total Even":
            odd_value = value.get('odd_value')
            even_fh = round(odd_value, 2)
            odd_even_firsthalf.insert(1, even_fh)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Total odd":
            odd_value = value.get('odd_value')
            odd_odd = round(odd_value, 2)
            odd_even.insert(0, odd_odd)

            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")
        if default_name == "Total even":
            odd_value = value.get('odd_value')
            even_odd = round(odd_value, 2)
            odd_even.insert(1, even_odd)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if default_name == f"{match['teams']['home']}" and value.get('market_tags') == "h1, h2":
            odd_value = value.get('odd_value')
            home_odd= round(odd_value, 2)
            home_draw_away.insert(0, home_odd)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if default_name == "X" and value.get('market_tags') == "h1, h2":
            odd_value = value.get('odd_value')
            draw_odd = round(odd_value, 2)
            home_draw_away.insert(1, draw_odd)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

        if default_name == f"{match['teams']['away']}" and value.get('market_tags') == "h1, h2":
            odd_value = value.get('odd_value')
            away_odd = round(odd_value, 2)
            home_draw_away.insert(2, away_odd)
            # print(f"Key: {key}, Odd Value for 'Draw No Bet': {odd_value}")

    wager_types.append({"1X2": home_draw_away})
    wager_types.append({"double_chance": double_chance})
    wager_types.append({"draw_no_bet": draw_no_bet})
    wager_types.append({"over_one_five": over_one_five})
    wager_types.append({"over_ofive_five_first_half": over_ofive_five_first_half})
    wager_types.append({"over_one_five_first_half": over_one_five_first_half})
    wager_types.append({"over_two_five_first_half": over_two_five_first_half})
    wager_types.append({"over_ofive_five": over_ofive_five})
    wager_types.append({"over_five_five": over_five_five})
    wager_types.append({"over_four_five": over_four_five})
    wager_types.append({"over_two_five": over_two_five})
    wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"fasthalf1X2": fasthalf1X2})
    wager_types.append({"fasthalf_dc": fasthalf_dc})
    wager_types.append({"gg_firsthalf": gg_firsthalf})
    wager_types.append({"odd_even": odd_even})
    wager_types.append({"odd_even_firsthalf": odd_even_firsthalf})
    wager_types.append({"draw_no_bet_first_half": draw_no_bet_first_half})
    wager_types.append({"first_team_to_score_first_half": first_team_to_score_first_half})
    wager_types.append({"first_team_to_score": first_team_to_score})
    wager_types.append({"gg": gg})
    wager_types.append({"home_team_overunder15": home_team_overunder15})
    wager_types.append({"home_team_overunder25": home_team_overunder25})
    wager_types.append({"home_team_overunder05": home_team_overunder05})
    wager_types.append({"away_team_overunder15": away_team_overunder15})
    wager_types.append({"away_team_overunder25": away_team_overunder25})
    wager_types.append({"away_team_overunder05": away_team_overunder05})
    # away2_home1X = [away_odd, double_chance1X]
    # home1_awayX2 = [home_odd, double_chanceX2]
    # X_away12 = [draw_odd, double_chance12]
    # wager_types.append({"21X": away2_home1X})
    # wager_types.append({"12X": home1_awayX2})
    # wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    return games

def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        home_team = match_detail['teams']['home']
        away_team = match_detail['teams']['away']

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


def process_and_fetch_data(league):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            start_time = time.time()
            league_name, league_id = process_league(league)
            match_details = api_calls_events(f"{league_id}")
            return league_name, match_details
        except Exception as e:
            print(f"Error processing {league}: {e}")

        # Check if the elapsed time exceeds the timeout limit
        elapsed_time = time.time() - start_time
        if elapsed_time > TIMEOUT_LIMIT:
            print(f"Timeout occurred for {league}. Restarting... (Retry {retries + 1}/{MAX_RETRIES})")
            retries += 1
        else:
            break

    raise TimeoutError(f"Function execution time exceeded {TIMEOUT_LIMIT} seconds after {MAX_RETRIES} retries")


def main():
    bookie_name = 'betbonanza'
    leagues = [
        {"England Premier League": 49},
        {"England Championship": 26909},
        {"England League One": 51},
        {"England League Two": 52},
        {"Scotland Premiership": 79},
        {"Scotland Championship": 5178},
        {"Scotland League One": 80},
        {"Scotland League Two": 5280},
        {"Northern Ireland": 565},
        {"Irish Premier": 26035},
        {"France League One": 57},
        {"France League Two": 58},
        {"Laliga": 83},
        {"Copa del Ray": 12911},
        {"Laliga 2": 84},
        # {"Japan League": 1787481},
        # {"Chinese League": 807},
        {"German Bundesliga": 60},
        {"German Bundesliga 2": 61},
        {"German DFB Pokal": 62},
        {"Italy Serie A": 64},
        {"Italy Serie B": 65},
        {"Italy Coppa Italia": 66},
        {"Netherlands Eredivisie": 70},
        {"Czech Liga 1": 23692},
        {"Greece Super League 1": 63},
        {"Superatten": 23144},
        {"England FA": 54},
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
                    league_wager_dic = exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)
                except:
                    continue
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("betbonanza", bookmaker_data)
        except Exception as e:
            print("Ambrose", e)
            continue
    return bookmaker_data

if __name__ == "__main__":
    start_time = time.time()
    games = main()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60

    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)
