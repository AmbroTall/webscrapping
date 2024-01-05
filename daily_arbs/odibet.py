import datetime
import time
import pytz
import requests

def odds_call_api(event_id):
    url = f"https://odibets.com/pxy/sportsbook?id={event_id}&category_id=&sub_type_id=&sportsbook=sportsbook&ua=Mozilla%2F5.0+(X11%3B+Linux+x86_64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F119.0.0.0+Safari%2F537.36&resource=sportevent"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'odibetskenya=cqh1i8sj8fj7apugktqc6q8f71; _gcl_au=1.1.1016428623.1702896388; _gid=GA1.2.878086922.1702896389; _sp_srt_ses.133d=*; _clck=1wdtwhn%7C2%7Cfhn%7C0%7C1447; _ga_94HYZZ5XCK=GS1.1.1702896388.1.1.1702896450.60.0.0; _ga=GA1.1.430741064.1702896388; _sp_srt_id.133d=004e0014-deac-4642-8a35-fc93b20ec228.1702896392.1.1702896453..c017484c-501b-4354-a673-ca501a7f0b0a....0; _clsk=4d5pe5%7C1702896454678%7C2%7C0%7Ca.clarity.ms%2Fcollect; _ga_2YY5CZW56W=GS1.1.1702896390.1.1.1702896732.60.0.0',
        'Referer': 'https://odibets.com/sportevent/41893239',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Odi-Key': 'Y3FN2kDOyAzNxoSOxEjKl12byh2QqgXdulGTqEzNmhTc2MWc0t2Z1BXY3omZ4o2c4kWMoDQy',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()['data']['markets']
    return r
def odi_bets():
    url = "https://odibets.com/pxy/sportsbook?sport_id=soccer&day=&country_id=&sort_by=&sub_type_id=&competition_id=&hour=&filter=&cs=&hs=&sportsbook=sportsbook&ua=Mozilla%2F5.0+(X11%3B+Linux+x86_64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F119.0.0.0+Safari%2F537.36&resource=sport"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'odibetskenya=cqh1i8sj8fj7apugktqc6q8f71; _gcl_au=1.1.1016428623.1702896388; _gid=GA1.2.878086922.1702896389; _sp_srt_ses.133d=*; _sp_srt_id.133d=004e0014-deac-4642-8a35-fc93b20ec228.1702896392.1.1702896392..c017484c-501b-4354-a673-ca501a7f0b0a....0; _clck=1wdtwhn%7C2%7Cfhn%7C0%7C1447; _clsk=4d5pe5%7C1702896394803%7C1%7C0%7Ca.clarity.ms%2Fcollect; _gat_gtag_UA_154149242_2=1; _gat_UA-154149242-1=1; _ga_94HYZZ5XCK=GS1.1.1702896388.1.1.1702896450.60.0.0; _ga=GA1.1.430741064.1702896388; _ga_2YY5CZW56W=GS1.1.1702896390.1.1.1702896451.60.0.0',
        'Referer': 'https://odibets.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Odi-Key': 'Y3FN2kDOyAzNxoSOxEjKl12byh2QqgXdulGTqEzNmhTc2MWc0t2Z1BXY3omZ4o2c4kWMoDQy',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()["data"]["matches"]
    odibets = []

    for match in r:
        if len(match["markets"]) >= 1 and match["sport_name"] == "Soccer":
            game = {}
            id = match["parent_match_id"]
            date_time = match["start_time"]
            home_team = match["home_team"]
            away_team = match["away_team"]
            away_team_odds = match["markets"][0]["outcomes"][2]["odd_value"]
            draw_odds = match["markets"][0]["outcomes"][1]["odd_value"]
            home_team_odds = match["markets"][0]["outcomes"][0]["odd_value"]
            game["time"] = date_time
            game["home_team"] = home_team
            game["away_team"] = away_team
            # game["bookie"] = "odi"
            matches = exctract_odds(id, game)
            odibets.append(matches)
        else:
            pass
    print(len(odibets))
    return sorted(odibets, key=lambda x: x['time'])

def exctract_odds(id, game):
    wager_types = []
    draw_no_bet = []
    double_chance = []
    handicap1 = [] # -1.5 / 1.5
    over_one_five = []
    over_two_five = []
    over_three_five = []
    fasthalf1X2 = []
    gg = []

    odds_market = odds_call_api(id)

    for market in odds_market:
        if market['sub_type_id'] == "1":
            for x in market['outcomes']:
                if x['outcome_key'] == "1":
                    home = x['odd_value']
                elif x['outcome_key'] == "X":
                    draw = x['odd_value']
                else:
                    away = x['odd_value']
            home_draw_away = [home, draw, away]
            wager_types.append({"1X2": home_draw_away})

        if market['sub_type_id'] == "10":
            for x in market['outcomes']:
                if x['outcome_key'] == "1 or 2":
                    dc12 = x['odd_value']
                elif x['outcome_key'] == "X or 2":
                    dcX2 = x['odd_value']
                else:
                    dc1X = x['odd_value']
            home_draw_away = [dc1X, dc12, dcX2]
            wager_types.append({"dc": home_draw_away})

        if market['sub_type_id'] == "29":
            ggyes = market['outcomes'][0]['odd_value']
            ggno = market['outcomes'][1]['odd_value']
            home_draw_away = [ggyes, ggno]
            wager_types.append({"gg": home_draw_away})
    try:
        for x in wager_types:
            for key, value in x.items():
                if key == "1X2":
                    away_odd = value[-1]
                    home_odd = value[0]
                    draw_odd = value[1]
                if key == "dc":
                    double_chance1X = value[0]
                    double_chance12 = value[1]
                    double_chanceX2 = value[2]
        away2_home1X = [away_odd, double_chance1X]
        home1_awayX2 = [home_odd, double_chanceX2]
        X_away12 = [draw_odd, double_chance12]
        wager_types.append({"21X": away2_home1X})
        wager_types.append({"12X": home1_awayX2})
        wager_types.append({"X12": X_away12})
    except:
        pass
    game['wager_types'] = wager_types
    return game


if __name__ == '__main__':
    start_time = time.time()
    games = odi_bets()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60
    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)

