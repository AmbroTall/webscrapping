import requests
from typing import List
from prettytable import PrettyTable
import datetime
import pytz
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
    profits = 0
    rows = 0
    total_funds_sportpesa = 0
    total_funds_odi = 0
    table.field_names = ["Date", "SportPesa Home Team", "SportPesa Away Team", "SportPesa Home Odds", "SportPesa Away Odds", "Odi Home Team", "Odi Away Team", "Odi Home Odds", "Odi Away Odds", "Arbitrage"]
    for row in merged_list:
        rows += 1

        total_funds_sportpesa += float(row['arbitrage'][list(row['arbitrage'].keys())[0]])
        total_funds_odi += float(row['arbitrage'][list(row['arbitrage'].keys())[1]])
        profits += int(row['arbitrage']['guaranteed_profit'])
        table.add_row([row['time'], row['home_team1'], row['away_team1'], row['home_odds1'], row['away_odds1'], row['home_team2'], row['away_team2'], row['home_odds2'], row['away_odds2'], row['arbitrage'] ])

    stake = rows * 2000
    print("******** Table Raws:", rows,"*********")
    print("******** Total Stake/Spending:",stake ,"*********")
    print("******** Potential Income:",profits,"*********")
    print("******** Potential Profits:",profits - stake,"*********")
    print("******** Total Funds Sportpesa:",total_funds_sportpesa,"*********")
    print("******** Total Funds Odi:",total_funds_odi,"*********")
    print("******** Loss:",stake,"********* \n")
    return str(table)

def odi_football():
    url = "https://apis.odibets.com/v5/matches?src=2&sport_id=soccer&tab=upcoming&country_id=&day=0&sub_type_id=&specifiers=&sort_by=&competition_id=&trials=0"

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
            if len(match["markets"]) >= 1 and match["sport_name"] == "Soccer":
                game = {}
                date_time = match["start_time"]
                home_team = match["home_team"]
                away_team = match["away_team"]
                away_team_odds = match["markets"][0]["outcomes"][2]["odd_value"]
                draw_odds = match["markets"][0]["outcomes"][1]["odd_value"]
                home_team_odds = match["markets"][0]["outcomes"][0]["odd_value"]

                game["time"] = date_time
                game["home_team"] = home_team
                game["away_team"] = away_team
                game["home_odds"] = home_team_odds
                game["draw_odds"] = draw_odds
                game["away_odds"] = away_team_odds
                odibets.append(game)
            else:
                pass
    return sorted(odibets, key=lambda x: x['time'])

def sport_pesa():
    url = "https://www.ke.sportpesa.com/api/highlights/1?type=prematch&section=highlights&markets_layout=multiple&o=startTime&pag_count=50&pag_min=1"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'visited=1; _gcl_au=1.1.2023157303.1679733010; initialTrafficSource=utmcsr=google|utmcmd=cpc|utmccn=(not set); __utmzzses=1; _fbp=fb.1.1679733010952.1525854058; LPVID=M1ZWFlZTYwMDBlMDc1ZGJi; _hjSessionUser_1199008=eyJpZCI6IjczMGQ3NjEyLWViMDAtNTFmYS1hYTQxLTE3MmY4YTM4MzA5NCIsImNyZWF0ZWQiOjE2Nzk3MzMwMTA2OTQsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_aw=GCL.1679733434.Cj0KCQjwt_qgBhDFARIsABcDjOewjh2dgKlMzlxwq5E82TWfgizgqe04jNbLO5a84GitjjPEil0mNIkaAmKvEALw_wcB; _gac_UA-47970910-1=1.1679733436.Cj0KCQjwt_qgBhDFARIsABcDjOewjh2dgKlMzlxwq5E82TWfgizgqe04jNbLO5a84GitjjPEil0mNIkaAmKvEALw_wcB; cookies_consented=1; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22first-time-bet-history-filter%22%3A%221%22%7D; device_view=full; _gid=GA1.2.1040695811.1682494667; _clck=ghfvcu|1|fb3|0; locale=en; spkessid=3pf2bvr6ms97dbu21tmlahul5v; _ga=GA1.2.1966569184.1679733010; LPSID-85738142=Kyq7gRmwSm-6bxoYeVQm9A; _clsk=165zf1o|1682517854173|1|1|s.clarity.ms/collect; _ga_5KBWG85NE7=GS1.1.1682517854.31.1.1682517878.36.0.0',
        'Referer': 'https://www.ke.sportpesa.com/en/sports-betting/football-1/',
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
        draw_odds = x['markets'][0]['selections'][1]['odds']
        away_team_odds = x['markets'][0]['selections'][2]['odds']
        away_team = x['markets'][0]['selections'][2]['name']
        dt_object = datetime.datetime.fromtimestamp(date_time / 1000.0)
        # Set the timezone to EAT
        eat_timezone = pytz.timezone('Africa/Nairobi')
        dt_eat = eat_timezone.localize(dt_object)
        # Convert to readable time zone
        readable_time_zone = dt_eat.strftime("%Y-%m-%d %H:%M:%S")

        game["time"] = readable_time_zone
        game["home_team"] = home_team
        game["away_team"] = away_team
        game["draw_odds"] = draw_odds
        game["home_odds"] = home_team_odds
        game["away_odds"] = away_team_odds

        sport_pesa.append(game)
    return sport_pesa

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
    return {f'stake1 for SportPesa with odds {odds1}': round(stake1, 2),
            f'stake2 for Odi with odds {odds2}': round(stake2, 2),
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

    # print("Prob 1", total_prob_player_1)
    prob_player_2_bookmaker_1 = 1 / odds_1_player_2
    prob_player_2_bookmaker_2 = 1 / odds_2_player_1
    total_prob_player_2 = prob_player_2_bookmaker_1 + prob_player_2_bookmaker_2

    # print("Prob 2", total_prob_player_2)

    arbitrage_margin_player_1 = 1 - total_prob_player_1
    arbitrage_margin_player_2 = 1 - total_prob_player_2

    if arbitrage_margin_player_2 > 0:
        # print("Arbitrage opportunity found!1")
        # print(f"Bookmaker 1 with odds {odds_1_player_2} || and Bookmaker 2 with odd {odds_2_player_1}")
        potential_profit = arbitrage_calc(odds_1_player_2, odds_2_player_1, 2000)
        # print("Potential profit: $", potential_profit)
        return potential_profit
    elif arbitrage_margin_player_1 > 0:
        # print("Arbitrage opportunity found!2")
        # print(f"Bookmaker 1 with odds {odds_1_player_1} || and Bookmaker 2 with odd {odds_2_player_2}")
        potential_profit = arbitrage_calc(odds_1_player_1, odds_2_player_2, 2000)
        # print("Potential profit: $", potential_profit)
        return potential_profit
    else:
        # print("No arbitrage opportunity")
        return "😢"

odi = odi_football()
sport = sport_pesa()
print()
merged_list = merge_odds_lists(sport, odi)
print("hello",merged_list)