import requests
import json
import datetime
import pytz
import pprint
import pandas as pd
from typing import List
from prettytable import PrettyTable

# def merge_odds_lists(list1: List[dict], list2: List[dict]) -> str:
#     merged_list = []
#     for game1 in list1:
#         for game2 in list2:
#             if game1['time'] == game2['time']:
#                 team1_split1 = sorted(game1['home_team'].split(' '), key=len, reverse=True)
#                 team1_split2 = sorted(game1['away_team'].split(' '), key=len, reverse=True)
#                 team2_split1 = sorted(game2['home_team'].split(' '), key=len, reverse=True)
#                 team2_split2 = sorted(game2['away_team'].split(' '), key=len, reverse=True)
#                 if set(team1_split1[:1]).intersection(team2_split1[:1]) and set(team1_split2[:1]).intersection(team2_split2[:1]):
#                     merged_list.append({
#                         'time': game1['time'],
#                         'home_team1': game1['home_team'],
#                         'away_team1': game1['away_team'],
#                         'home_odds1': game1['home_odds'],
#                         'away_odds1': game1['away_odds'],
#                         'home_team2': game2['home_team'],
#                         'away_team2': game2['away_team'],
#                         'home_odds2': game2['home_odds'],
#                         'away_odds2': game2['away_odds'],
#                         'arbitrage': caller_function(game1['home_odds'],game1['away_odds'],game2['home_odds'], game2['away_odds'])
#                     })
#                 elif set(team1_split1[:1]).intersection(team2_split2[:1]) and set(team1_split2[:1]).intersection(team2_split1[:1]):
#                     merged_list.append({
#                         'time': game1['time'],
#                         'home_team1': game1['home_team'],
#                         'away_team1': game1['away_team'],
#                         'home_odds1': game1['home_odds'],
#                         'away_odds1': game1['away_odds'],
#                         'home_team2': game2['home_team'],
#                         'away_team2': game2['away_team'],
#                         'home_odds2': game2['home_odds'],
#                         'away_odds2': game2['away_odds'],
#                         'arbitrage': caller_function(game1['home_odds'], game1['away_odds'], game2['home_odds'], game2['away_odds'])
#                     })
#     table = PrettyTable()
#     table.field_names = ["Date", "SportPesa Home Team", "SportPesa Away Team", "SportPesa Home Odds", "SportPesa Away Odds", "Betika Home Team", "Betika Away Team", "Betika Home Odds", "Betika Away Odds", "Arbitrage"]
#     for row in merged_list:
#         table.add_row([row['time'], row['home_team1'], row['away_team1'], row['home_odds1'], row['away_odds1'], row['home_team2'], row['away_team2'], row['home_odds2'], row['away_odds2'], row['arbitrage'] ])
#     return str(table)
#

def merge_odds_lists(list1: List[dict], list2: List[dict], list3: List[dict]) -> str:
    merged_list = []
    for game1 in list1:
        for game2 in list2:
            for game3 in list3:
                if game1['time'] == game2['time'] == game3['time']:
                    team1_split1 = sorted(game1['home_team'].split(' '), key=len, reverse=True)
                    team1_split2 = sorted(game1['away_team'].split(' '), key=len, reverse=True)
                    team2_split1 = sorted(game2['home_team'].split(' '), key=len, reverse=True)
                    team2_split2 = sorted(game2['away_team'].split(' '), key=len, reverse=True)
                    team3_split1 = sorted(game3['home_team'].split(' '), key=len, reverse=True)
                    team3_split2 = sorted(game3['away_team'].split(' '), key=len, reverse=True)
                    if set(team1_split1[:1]).intersection(team2_split1[:1]) and set(team1_split2[:1]).intersection(team2_split2[:1]) and set(team1_split1[:1]).intersection(team3_split1[:1]) and set(team1_split2[:1]).intersection(team3_split2[:1]):
                        merged_list.append({
                            'time': game1['time'],
                            'home_team1': game1['home_team'],
                            'away_team1': game1['away_team'],
                            'home_odds1': game1['home_odds'],
                            'away_odds1': game1['away_odds'],
                            'home_team2': game2['home_team'],
                            'away_team2': game2['away_team'],
                            'home_odds2': game2['home_odds'],
                            'away_odds2': game2['away_odds'],
                            'home_team3': game3['home_team'],
                            'away_team3': game3['away_team'],
                            'home_odds3': game3['home_odds'],
                            'away_odds3': game3['away_odds'],
                            'arbitrage': caller_function(game1['home_odds'], game1['away_odds'], game2['home_odds'], game2['away_odds'], game3['home_odds'], game3['away_odds'])
                        })
    table = PrettyTable()
    table.field_names = ["Date", "SportPesa Home Team", "SportPesa Away Team", "SportPesa Home Odds", "SportPesa Away Odds", "Betika Home Team", "Betika Away Team", "Betika Home Odds", "Betika Away Odds", "BetLion Home Team", "BetLion Away Team", "Oddi Home Odds", "Oddi Away Odds", "Arbitrage"]
    for row in merged_list:
        table.add_row([row['time'], row['home_team1'], row['away_team1'], row['home_odds1'], row['away_odds1'], row['home_team2'], row['away_team2'], row['home_odds2'], row['away_odds2'], row['home_team3'], row['away_team3'], row['home_odds3'], row['away_odds3'], row['arbitrage']])
    return str(table)


def sport_pesa():
    url = "https://www.ke.sportpesa.com/api/upcoming/games?type=prematch&sportId=2&section=upcoming&markets_layout=multiple&o=startTime&pag_count=15&pag_min=1"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.2023157303.1679733010; initialTrafficSource=utmcsr=google|utmcmd=cpc|utmccn=(not set); __utmzzses=1; _fbp=fb.1.1679733010952.1525854058; cookies_consented=1; LPVID=M1ZWFlZTYwMDBlMDc1ZGJi; _hjSessionUser_1199008=eyJpZCI6IjczMGQ3NjEyLWViMDAtNTFmYS1hYTQxLTE3MmY4YTM4MzA5NCIsImNyZWF0ZWQiOjE2Nzk3MzMwMTA2OTQsImV4aXN0aW5nIjp0cnVlfQ==; settings=%7B%22first-time-multijackpot%22%3A%221%22%7D; _gcl_aw=GCL.1679733434.Cj0KCQjwt_qgBhDFARIsABcDjOewjh2dgKlMzlxwq5E82TWfgizgqe04jNbLO5a84GitjjPEil0mNIkaAmKvEALw_wcB; _gac_UA-47970910-1=1.1679733436.Cj0KCQjwt_qgBhDFARIsABcDjOewjh2dgKlMzlxwq5E82TWfgizgqe04jNbLO5a84GitjjPEil0mNIkaAmKvEALw_wcB; LPSID-85738142=PTPz8nRmSrupKPS0sFm3yw; spkessid=tkva66jf2s9bqhbpfm5dih7835; locale=en; _gid=GA1.2.1553517251.1680720602; _ga=GA1.2.1966569184.1679733010; _hjSession_1199008=eyJpZCI6IjMyMTIxNmRhLTBlYTktNDNlZC04NDU5LWVhZmExMmQ0ZjMzYiIsImNyZWF0ZWQiOjE2ODA3MjA2MDU2MjcsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _clck=ghfvcu|1|fai|0; _ga_5KBWG85NE7=GS1.1.1680720603.15.1.1680720935.42.0.0; _clsk=l2bjgg|1680720935676|3|1|w.clarity.ms/collect',
        'Referer': 'https://www.ke.sportpesa.com/en/sports-betting/basketball-2/upcoming-games/?filterOrder=startTime',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()

    sport_pesa = []
    for x in r:
        game = {}
        date_time = x['dateTimestamp']
        home_team = x['markets'][0]['selections'][0]['name']
        home_team_odds = x['markets'][0]['selections'][0]['odds']
        away_team_odds = x['markets'][0]['selections'][1]['odds']
        away_team = x['markets'][0]['selections'][1]['name']
        dt_object = datetime.datetime.fromtimestamp(date_time / 1000.0)
        # Set the timezone to EAT
        eat_timezone = pytz.timezone('Africa/Nairobi')
        dt_eat = eat_timezone.localize(dt_object)
        # Convert to readable time zone
        readable_time_zone = dt_eat.strftime("%Y-%m-%d %H:%M:%S")
        # print(readable_time_zone)
        # print(f"{home_team} - {home_team_odds}")
        # print(f"{away_team} - {away_team_odds}")
        # print()
        game["time"] = readable_time_zone
        game["home_team"] = home_team
        game["away_team"] = away_team
        game["home_odds"] = home_team_odds
        game["away_odds"] = away_team_odds

        sport_pesa.append(game)
    return sport_pesa

def odi_basketball():
    url = "https://apis.odibets.com/v5/matches?src=2&sport_id=basketball&tab=upcoming&country_id=&day=0&sub_type_id=&specifiers=&sort_by=&competition_id=&trials=0"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://odibets.com',
        'Referer': 'https://odibets.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    r = response.json()["data"]["competitions"]

    odibets = []
    for i in r:
        try:
            matches = i["matches"]
            for match in matches:
                if len(match["markets"]) >= 1:
                    game = {}
                    date_time = match["start_time"]
                    home_team = match["home_team"]
                    away_team = match["away_team"]
                    away_team_odds = match["markets"][0]["outcomes"][2]["odd_value"]
                    home_team_odds = match["markets"][0]["outcomes"][0]["odd_value"]
                    print(date_time)
                    print(f"{home_team} - {home_team_odds}")
                    print(f"{away_team} - {away_team_odds}")
                    print()

                    game["time"] = date_time
                    game["home_team"] = home_team
                    game["away_team"] = away_team
                    game["home_odds"] = home_team_odds
                    game["away_odds"] = away_team_odds

                    odibets.append(game)
        except:
            pass
    return sorted(odibets, key=lambda x: x['time'])

def betika_basketball():
    url = "https://api.betika.com/v1/uo/matches?page=1&limit=10&tab=&sub_type_id=1,186,340&sport_id=30&tag_id=&sort_id=2&period_id=-1&esports=false"
    payload = {}
    headers = {
        'authority': 'api.betika.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.betika.com',
        'referer': 'https://www.betika.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=KVwDiKPxb_1s8aLURjI9wfci7W5nCSEjbE7Md.7GIUM-1680720883-0-Acswj8jvkzwJtjiCqADa+ZitjSPYlaUCc/oHTHLLHUu5WYwswle/sHM7qLxWZcIutOAvnf7jOU6QFq9gg5HZMFs='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()['data']
    betika = []
    for x in r:
        game = {}
        date_time = x['start_time']
        home_team = x['home_team']
        home_team_odds = x['home_odd']
        away_team_odds = x['away_odd']
        away_team = x['away_team']

        # print(date_time)
        # print(f"{home_team} - {home_team_odds}")
        # print(f"{away_team} - {away_team_odds}")
        # print()

        game["time"] = date_time
        game["home_team"] = home_team
        game["away_team"] = away_team
        game["home_odds"] = home_team_odds
        game["away_odds"] = away_team_odds

        betika.append(game)
    return betika

# def arbitrage_calc(odds1, odds2, total_stake):
#     # Calculate the implied probabilities of each outcome
#     prob1 = 1 / odds1
#     prob2 = 1 / odds2
# 
#     # Calculate the total implied probability
#     total_prob = prob1 + prob2
# 
#     # Calculate the fair odds for each outcome
#     fair_odds1 = prob1 / total_prob
#     fair_odds2 = prob2 / total_prob
# 
#     # Calculate the stake for each outcome
#     stake1 = (total_stake * fair_odds1) / (fair_odds1 + fair_odds2)
#     stake2 = (total_stake * fair_odds2) / (fair_odds1 + fair_odds2)
# 
#     # Calculate the possible winnings for each outcome
#     winnings1 = stake1 * odds1
#     winnings2 = stake2 * odds2
# 
#     # Calculate the guaranteed profit
#     guaranteed_profit = (total_stake / total_prob) - total_stake
# 
#     # Return the results as a dictionary
#     return {f'stake1 for SportPesa with odds {odds1}': round(stake1, 2),
#             f'stake2 for Odi with odds {odds2}': round(stake2, 2),
#             'winnings1': round(winnings1, 2),
#             'winnings2': round(winnings2, 2),
#             'guaranteed_profit': round(guaranteed_profit, 2)}

def arbitrage_calc(odds1, bookie1,odds2,bookie2, total_stake):
    # Calculate the implied probabilities of each outcome
    prob1 = 1 / odds1
    prob2 = 1 / odds2

    # Calculate the total implied probability
    total_prob = prob1 + prob2

    # Calculate the fair odds for each outcome
    fair_odds1 = prob1 / total_prob
    fair_odds2 = prob2 / total_prob

    # Calculate the stake for each outcome
    stake1 = (total_stake * fair_odds1) / (fair_odds1 + fair_odds2)
    stake2 = (total_stake * fair_odds2) / (fair_odds1 + fair_odds2)

    # Calculate the possible winnings for each outcome
    winnings1 = stake1 * odds1
    winnings2 = stake2 * odds2

    # Calculate the guaranteed profit
    guaranteed_profit = (total_stake / total_prob) - total_stake

    # Return the results as a dictionary
    return {f'stake1 for {bookie1} with odds {odds1}': round(stake1, 2),
            f'stake2 for {bookie2} with odds {odds2}': round(stake2, 2),
            'winnings1': round(winnings1, 2),
            'winnings2': round(winnings2, 2),
            'guaranteed_profit': round(guaranteed_profit, 2)}

def caller_function(odds_1_player_1,odds_1_player_2,odds_2_player_1,odds_2_player_2 ):
    odds_1_player_1 = float(odds_1_player_1)
    odds_1_player_2 = float(odds_1_player_2)
    odds_2_player_1 = float(odds_2_player_1)
    odds_2_player_2 = float(odds_2_player_2)
    # Arbitrage calculations
    prob_player_1_bookmaker_1 = 1 / odds_1_player_1
    prob_player_1_bookmaker_2 = 1 / odds_2_player_2
    total_prob_player_1 = prob_player_1_bookmaker_1 + prob_player_1_bookmaker_2

    print("Prob 1", total_prob_player_1)
    prob_player_2_bookmaker_1 = 1 / odds_1_player_2
    prob_player_2_bookmaker_2 = 1 / odds_2_player_1
    total_prob_player_2 = prob_player_2_bookmaker_1 + prob_player_2_bookmaker_2

    print("Prob 2", total_prob_player_2)

    arbitrage_margin_player_1 = 1 - total_prob_player_1
    arbitrage_margin_player_2 = 1 - total_prob_player_2

    if arbitrage_margin_player_2 > 0:
        print("Arbitrage opportunity found!1")
        print(f"Bookmaker 1 with odds {odds_1_player_2} || and Bookmaker 2 with odd {odds_2_player_1}")
        potential_profit = arbitrage_calc(odds_1_player_2, odds_2_player_1, 50000)
        print("Potential profit: $", potential_profit)
        return potential_profit
    elif arbitrage_margin_player_1 > 0:
        print("Arbitrage opportunity found!2")
        print(f"Bookmaker 1 with odds {odds_1_player_1} || and Bookmaker 2 with odd {odds_2_player_2}")
        potential_profit = arbitrage_calc(odds_1_player_1, odds_2_player_2, 50000)
        print("Potential profit: $", potential_profit)
        return potential_profit
    else:
        print("No arbitrage opportunity")
        return "😢"

def caller_function(odds_1_player_1, odds_1_player_2, odds_2_player_1, odds_2_player_2, odds_3_player_1, odds_3_player_2):
    bookmakers = ["sport_pesa", "betika", "odi"]
    odds = {bookmakers[0]: (float(odds_1_player_1), float(odds_1_player_2)),
            bookmakers[1]: (float(odds_2_player_1), float(odds_2_player_2)),
            bookmakers[2]: (float(odds_3_player_1), float(odds_3_player_2))}

    # Arbitrage calculations
    best_combination = None
    max_profit = 0
    for i in range(len(odds)):
        for j in range(i + 1, len(odds)):
            prob_player_1 = 1 / odds[list(odds.keys())[i]][0] + 1 / odds[list(odds.keys())[j]][1]
            prob_player_2 = 1 / odds[list(odds.keys())[i]][1] + 1 / odds[list(odds.keys())[j]][0]
            margin_player_1 = 1 - prob_player_1
            margin_player_2 = 1 - prob_player_2
            if margin_player_1 > 0 and margin_player_1 > max_profit:
                max_profit = margin_player_1
                best_combination = (list(odds.keys())[i], list(odds.keys())[j], odds[list(odds.keys())[i]][0], odds[list(odds.keys())[j]][1])
            if margin_player_2 > 0 and margin_player_2 > max_profit:
                max_profit = margin_player_2
                best_combination = (list(odds.keys())[i], list(odds.keys())[j], odds[list(odds.keys())[i]][1], odds[list(odds.keys())[j]][0])

    if best_combination is not None:
        print("Arbitrage opportunity found!")
        print(f"{best_combination[0]} with odds {best_combination[2]} || and {best_combination[1]} with odd {best_combination[3]}")
        potential_profit = arbitrage_calc(best_combination[2],best_combination[0], best_combination[3],best_combination[1], 50000)
        print("Potential profit: $", potential_profit)
        return potential_profit, best_combination[0], best_combination[1]
    else:
        print("No arbitrage opportunity")
        return "😢"

sport_pesa = sport_pesa()
betika = betika_basketball()
odi = odi_basketball()
print("SPORT PESA : ++++++++++++++",sport_pesa)
print()
print("BETIKA --------------------", betika)
print()
print("ODI    --------------------", odi)
merged_list = merge_odds_lists(sport_pesa, betika, odi)
print(merged_list)
# pprint.pprint(merged_list)
# SportPesa Odds
# odds_1_player_1 = 2.50
# odds_1_player_2 = 1.80
# odds_2_player_1 = 1.70
# odds_2_player_2 = 3.20
# odds_3_player_1 = 3.50
# odds_3_player_2 = 1.90
#
#
# caller_function(odds_1_player_1, odds_1_player_2, odds_2_player_1, odds_2_player_2, odds_3_player_1, odds_3_player_2)
