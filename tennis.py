import requests
import json
import datetime
import pytz
import pprint
import pandas as pd
from typing import List
from prettytable import PrettyTable

def merge_odds_lists(list1: List[dict], list2: List[dict]) -> str:
    merged_list = []
    for game1 in list1:
        for game2 in list2:
            if game1['time'] == game2['time']:
                team1_split1 = sorted(game1['home_team'].split(' '), key=len, reverse=True)
                team1_split2 = sorted(game1['away_team'].split(' '), key=len, reverse=True)
                team2_split1 = sorted(game2['home_team'].split(' '), key=len, reverse=True)
                team2_split2 = sorted(game2['away_team'].split(' '), key=len, reverse=True)
                if set(team1_split1[:1]).intersection(team2_split1[:1]) and set(team1_split2[:1]).intersection(team2_split2[:1]):
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
                        'arbitrage': caller_function(game1['home_odds'],game1['away_odds'],game2['home_odds'], game2['away_odds'])
                    })
                elif set(team1_split1[:1]).intersection(team2_split2[:1]) and set(team1_split2[:1]).intersection(team2_split1[:1]):
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
                        'arbitrage': caller_function(game1['home_odds'], game1['away_odds'], game2['home_odds'], game2['away_odds'])
                    })
    table = PrettyTable()
    table.field_names = ["Date", "SportPesa Home Team", "SportPesa Away Team", "SportPesa Home Odds", "SportPesa Away Odds", "Betika Home Team", "Betika Away Team", "Betika Home Odds", "Betika Away Odds", "Arbitrage"]
    for row in merged_list:
        table.add_row([row['time'], row['home_team1'], row['away_team1'], row['home_odds1'], row['away_odds1'], row['home_team2'], row['away_team2'], row['home_odds2'], row['away_odds2'], row['arbitrage'] ])
    return str(table)




def odi_basketball():
    url = "https://apis.odibets.com/v5/matches?src=1&sport_id=5&tab=live&country_id=&day=&sub_type_id=&specifiers=&sort_by=&competition_id=&trials=0"

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

    r = response.json()["data"]["competitions"]

    odibets = []
    for i in r:
        try:
            matches = i["matches"]
        except:
            pass
        for match in matches:
            if len(match["markets"]) >= 1 and match["sport_name"] == "Tennis":
                game = {}
                date_time = match["start_time"]
                home_team = match["home_team"]
                away_team = match["away_team"]
                away_team_odds = match["markets"][0]["outcomes"][1]["odd_value"]
                home_team_odds = match["markets"][0]["outcomes"][0]["odd_value"]
                # print(date_time)
                # print(f"{home_team} - {home_team_odds}")
                # print(f"{away_team} - {away_team_odds}")
                # print()

                game["time"] = date_time
                game["home_team"] = home_team
                game["away_team"] = away_team
                game["home_odds"] = home_team_odds
                game["away_odds"] = away_team_odds
                odibets.append(game)
            else:
                pass
    return sorted(odibets, key=lambda x: x['time'])

def betika_basketball():
    url = "https://live.betika.com/v1/uo/matches?page=1&limit=1000&sub_type_id=1,186,340&sport=null&sort=1"

    payload = {}
    headers = {
        'authority': 'live.betika.com',
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
        'Cookie': '__cf_bm=iWQ31nJHLPkNLcGQzd88WF.YXHk193gQRWHwDdEUXSo-1680780772-0-AefyK6TJvoHM92IDl0PCN5QI1iWR5KpHOt95+hn47tGCT94ryaEj9DZ1w1oipbTyqOn8cn+xTWCLHu9hHkKTFrY='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    r = response.json()['data']
    betika = []
    for x in r:
        if x["sport_name"] == "Tennis" and x['home_odd'] != "0.00" and x['away_odd'] != "0.00":
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
def arbitrage_calc(odds1, odds2, total_stake):
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
    return {f'stake1 for Bookmaker 1 with odds {odds1}': round(stake1, 2),
            f'stake2 for Bookmaker 2 with odds {odds2}': round(stake2, 2),
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
        potential_profit = arbitrage_calc(odds_1_player_2, odds_2_player_1, 2000)
        print("Potential profit: $", potential_profit)
        return potential_profit
    elif arbitrage_margin_player_1 > 0:
        print("Arbitrage opportunity found!2")
        print(f"Bookmaker 1 with odds {odds_1_player_1} || and Bookmaker 2 with odd {odds_2_player_2}")
        potential_profit = arbitrage_calc(odds_1_player_1, odds_2_player_2, 2000)
        print("Potential profit: $", potential_profit)
        return potential_profit
    else:
        print("No arbitrage opportunity")
        return "😢"



betika = betika_basketball()
odi = odi_basketball()
# print("BETIKA --------------------", betika)
print()
print("ODI    --------------------", odi)
merged_list = merge_odds_lists(betika, odi)
print("hello",merged_list)
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
