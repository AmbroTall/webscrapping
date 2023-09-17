import requests


# Wekelea bet teketeke
def place_bet_api():
    url = "https://www.ke.sportpesa.com/api/live/place"

    payload = "{\"stake\":\"50.00\",\"amount\":\"50.00\",\"selections\":[{\"eventId\":10349415,\"marketId\":126666043,\"sequence\":0,\"selectionId\":377308869,\"odds\":\"1.76\",\"coeff\":\"1.76\",\"id\":377308869}],\"bets\":[{\"eventId\":10349415,\"marketId\":126666043,\"sequence\":0,\"selectionId\":377308869,\"odds\":\"1.76\",\"coeff\":\"1.76\",\"id\":377308869}],\"acceptOdds\":true,\"betSpinner\":-2}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Atrue%7D%7D; locale=en; _hjSession_1199008=eyJpZCI6Ijg4NmQ2MjNkLTZiNjctNDMxNC05YThhLTU0YWVjNDdjYWQxMCIsImNyZWF0ZWQiOjE2OTQ5NTUxNDMwNjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; LPSID-85738142=rqxNXIrIQHC94ZS9rCNZCQ; spkessid=a4kusuvnte35dlhjija1pufk8c; _ga=GA1.2.619053130.1693297829; _hjIncludedInSessionSample_1199008=0; _ga_5KBWG85NE7=GS1.1.1694955130.41.1.1694956436.7.0.0',
        'Origin': 'https://www.ke.sportpesa.com',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events/10349415/markets?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Querry active bets
def fetch_active_bets():
    url = "https://www.ke.sportpesa.com/api/live/bets"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; locale=en; _hjSession_1199008=eyJpZCI6Ijg4NmQ2MjNkLTZiNjctNDMxNC05YThhLTU0YWVjNDdjYWQxMCIsImNyZWF0ZWQiOjE2OTQ5NTUxNDMwNjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; LPSID-85738142=rqxNXIrIQHC94ZS9rCNZCQ; spkessid=a4kusuvnte35dlhjija1pufk8c; _ga=GA1.2.619053130.1693297829; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Afalse%7D%7D; _ga_5KBWG85NE7=GS1.1.1694955130.41.1.1694957816.60.0.0; _gat_UA-47970910-1=1',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events/10349415/markets?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


stake = "50.00"
amount = "50.00"
eventId = 10349415
marketId = 126666043
sequence = 0
selectionId = 377308869
odds = "1.76"
coeff = odds
id = selectionId

bet = {"eventId": int(eventId), "marketId": int(marketId), "sequence": int(sequence), "selectionId": int(selectionId),"odds": odds,"coeff": odds, "id": int(id)}
payload = {"stake": stake, "amount": amount, "selections": [bet], "bets": [bet], "acceptOdds": True, "betSpinner": -2}


def live_games_display():
    url = "https://www.ke.sportpesa.com/api/live/sports/4/events?count=15&offset=0"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Atrue%7D%7D; locale=en; spkessid=u9335e7ldusjlra39bufefmndl; _ga=GA1.1.619053130.1693297829; LPSID-85738142=oBtwahmWT_GruGrVRahInw; _ga_5KBWG85NE7=GS1.1.1694886035.34.0.1694886035.60.0.0',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    events = r['events']
    all_games = []
    for index, x in enumerate(events, start=0):
        print(f"\n index {index} Game : {x} \n")


def quater_scores_api( event_id, quater):
    url = f"https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/json?eventId={event_id}&cb=1688197270322"

    payload = {}
    headers = {
        'authority': 'sportpesa.betstream.betgenius.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'referer': f'https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/html?eventId={event_id}',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()

    print(r)
    data = r['Scoreboard']
    league = data['CompetitionName']
    teams_playing = data['DisplayName']
    total_home = data['FirstDisplayed']['GameScore']
    total_away = data['SecondDisplayed']['GameScore']
    home_team_quarter_scores = data['FirstDisplayed']['QuarterScores'][quater - 1]['Value']
    away_team_quarter_scores = data['SecondDisplayed']['QuarterScores'][quater - 1]['Value']
    total_quarter_secs = data['Clock']['NumberOfQuarterSeconds']
    remaining_quarter_secs_static = data['Clock']['SecondsRemainingInQuarter']
    remaining_secs = r['Commentary']['Actions'][0]['Action']['QuarterTimeRemaining']
    remaining_quarter_secs = int(remaining_secs) / 1000
    #Quarter Scores
    total_scores = int(home_team_quarter_scores) + int(away_team_quarter_scores)
    game_total_scores = int(total_home) + int(total_away)
    return total_scores, total_quarter_secs, remaining_quarter_secs, game_total_scores

print(quater_scores_api(eventId, 4))