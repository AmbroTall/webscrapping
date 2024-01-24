import datetime
import time

import pytz
import requests


def odds_call_api(event_id):
    url = f"https://www.ke.sportpesa.com/api/games/markets?games={event_id}&markets=all"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.1416567265.1702573256; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _fbp=fb.1.1702573258024.1249372149; LPVID=g2YzBhNTI4OGE5NjcyOGNl; _hjSessionUser_1199008=eyJpZCI6IjFmMGE1ZDk2LWZiNzAtNTdmNS1hNWQ0LWI5MGUzNDYyMzlmMSIsImNyZWF0ZWQiOjE3MDI1NzMyNTg1NDQsImV4aXN0aW5nIjp0cnVlfQ==; cookies_consented=1; spkessid=gthb42api5tu20kjjgt8lrlj3u; locale=en; _gid=GA1.2.1472040237.1702888456; settings=%7B%22first-time-multijackpot%22%3A%221%22%7D; _ga=GA1.1.993909426.1702573257; _hjIncludedInSessionSample_1199008=0; _hjSession_1199008=eyJpZCI6ImUyODZlODBlLWJmMWEtNDY4MC04ZjdlLTFmZTlkMzA1ZGE1YyIsImMiOjE3MDI4OTMyMzQzODEsInMiOjAsInIiOjAsInNiIjowfQ==; _hjAbsoluteSessionInProgress=0; LPSID-85738142=jupHvwHLTGyDzAjELcbdMQ; _ga_5KBWG85NE7=GS1.1.1702893233.4.1.1702894804.60.0.0; device_view=full; spkessid=bibvtq98dmo7n6ac92envmm0t3; visited=1',
        'Referer': 'https://www.ke.sportpesa.com/games/4994197/markets?sportId=1&section=today-games',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    return  r[f'{event_id}']
def sport_pesa():
    url = "https://www.ke.sportpesa.com/api/todays/1/games?type=prematch&section=today&markets_layout=multiple&o=startTime&pag_count=100&pag_min=1"

    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.ke.sportpesa.com/en/sports-betting/football-1/today-games/',
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Timezone': 'Africa/Nairobi',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'device_view=full; spkessid=bibvtq98dmo7n6ac92envmm0t3; visited=1'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()

    sport_pesa = []
    for x in r:
        game = {}
        id = x['id']
        date_time = x['dateTimestamp']
        home_team = x['markets'][0]['selections'][0]['name']
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
        # game["bookie"] = "sportpesa"
        matches = exctract_odds(id, game)
        sport_pesa.append(matches)
    print(len(sport_pesa))
    return sorted(sport_pesa, key=lambda x: x['time'])


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
    away_odd = 0
    home_odd = 0
    double_chanceX2 = 0
    double_chance1X = 0
    draw_odd = 0
    double_chance12 = 0

    for market in odds_market:
        if market['name'] == "3 Way":
            home_odd = market['selections'][0]['odds']
            away_odd = market['selections'][2]['odds']
            draw_odd = market['selections'][1]['odds']

            home_draw_away = [home_odd, draw_odd, away_odd]
            wager_types.append({"1X2": home_draw_away})

        if market['name'] == "Double Chance":
            dc1X = market['selections'][0]['odds']
            dc12 = market['selections'][2]['odds']
            dcX2 = market['selections'][1]['odds']
            home_draw_away = [dc1X, dc12, dcX2]
            wager_types.append({"dc": home_draw_away})

        if market['name'] == "Both Teams To Score":
            ggyes = market['selections'][0]['odds']
            ggno = market['selections'][1]['odds']
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
    games = sport_pesa()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60
    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)

