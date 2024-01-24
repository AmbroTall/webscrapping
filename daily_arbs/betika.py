import datetime
import time
import pytz
import requests

def odds_call_api(event_id):
    url = f"https://api.betika.com/v1/uo/match?parent_match_id={event_id}"

    payload = {}
    headers = {
        'authority': 'api.betika.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'if-modified-since': 'Thu, 21 Dec 2023 08:55:28 GMT',
        'origin': 'https://www.betika.com',
        'referer': 'https://www.betika.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=xMP9HrCEEc8nQupXL.0PlIx9I9VXD4jEdHxA_6RYgxY-1703173482-1-AVIAVL9bzi/gHeL/cPQRmyN7g4kwSdkuBptlTHbR5DzlzlHV3zkhp8+8F1ZhzUWqC3DTMMV/htAQJFTYzpLwf1U='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()['data']
    return r
def betika():
    url = "https://api.betika.com/v1/uo/matches?page=1&limit=100&tab=&sub_type_id=1,186,340&sport_id=14&tag_id=&sort_id=1&period_id=-2&esports=false"

    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.betika.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': '__cf_bm=xMP9HrCEEc8nQupXL.0PlIx9I9VXD4jEdHxA_6RYgxY-1703173482-1-AVIAVL9bzi/gHeL/cPQRmyN7g4kwSdkuBptlTHbR5DzlzlHV3zkhp8+8F1ZhzUWqC3DTMMV/htAQJFTYzpLwf1U='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()['data']
    betika = []
    for match in response:
        game = {}
        id = match['parent_match_id']
        home_team = match["home_team"]
        away_team = match["away_team"]
        date_time = match["start_time"]

        game["time"] = date_time
        game["home_team"] = home_team
        game["away_team"] = away_team
        matches = exctract_odds(id, game)
        betika.append(matches)

    print(len(betika))
    return sorted(betika, key=lambda x: x['time'])
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
        if market['name'] == "1X2":
            home_odd = market['odds'][0]['odd_value']
            away_odd = market['odds'][2]['odd_value']
            draw_odd = market['odds'][1]['odd_value']

            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if market['name'] == "DOUBLE CHANCE":
            dc1X = market['odds'][0]['odd_value']
            dc12 = market['odds'][2]['odd_value']
            dcX2 = market['odds'][1]['odd_value']
            home_draw_away = [dc1X, dc12, dcX2]
            wager_types.append({"dc": home_draw_away})

        if market['name'] == "BOTH TEAMS TO SCORE (GG/NG)":
            ggyes = market['odds'][0]['odd_value']
            ggno = market['odds'][1]['odd_value']
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
    games = betika()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60
    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)

