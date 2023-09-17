import time
from datetime import datetime
import pytz
import requests
import datetime


def request_function(url, headers, payload):
    while True:
        response = requests.request("GET", url, headers=headers, data=payload)
        r = response.json()
        time.sleep(2)
        if r:
            return r
def get_start_time():
    # Get the current date in your desired timezone (e.g., Nairobi)
    # Replace 'Africa/Nairobi' with your desired timezone
    nairobi_timezone = datetime.timezone(datetime.timedelta(hours=3))  # Nairobi timezone is UTC+3
    current_date = datetime.datetime.now(nairobi_timezone).date()

    # Calculate the end of the day by setting the time to 23:59:59
    end_of_day = datetime.datetime.combine(current_date, datetime.time(23, 59, 59, 999999), tzinfo=nairobi_timezone)

    # Convert the end of the day to a Unix timestamp (seconds since the epoch)
    end_of_day_unix_timestamp = int(end_of_day.timestamp())
    current_time_unix = int(time.time())  # Current time in Linux timestamp (seconds)

    url = f"https://www.ke.sportpesa.com/api/upcoming/games?type=prematch&sportId=2&section=upcoming&markets_layout=multiple&o=startTime&pag_count=15&pag_min=1&from={current_time_unix}&to={end_of_day_unix_timestamp}"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; settings=%7B%22first-time-multijackpot%22%3A%221%22%7D; locale=en; _gid=GA1.2.1111460384.1694628076; spkessid=mkke0h5mqs203bqb7of7l6qfn7; LPSID-85738142=UEPV_otdQN2VyGuYmcr73A; _gat_UA-47970910-1=1; _ga_5KBWG85NE7=GS1.1.1694711035.18.1.1694711576.8.0.0; _ga=GA1.1.619053130.1693297829; visited=1',
        'Referer': 'https://www.ke.sportpesa.com/en/sports-betting/basketball-2/upcoming-games/?filterDay=0&filterOrder=startTime&paginationOffset=0',
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

    r = request_function(url, headers, payload)
    try:
        all_games = []
        for game in r:
            games = {}
            games['time'] = game['dateTimestamp']
            games['competition_name'] = game['competition']['name']
            games['country'] = game['country']['name']
            games['home_team'] = game['competitors'][0]['name']
            games['away_team'] = game['competitors'][1]['name']
            all_games.append(games)
        print(all_games)
        return all_games

    except:
        print("No games available.")


# print(get_start_time(current_time_unix, end_of_day_unix_timestamp))
