import requests
import json

def get_countries():
    url = "https://www.ke.sportpesa.com/api/navigation"

    payload={}
    headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Cookie': 'visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Afalse%7D%2C%22first-time-bet-history-filter%22%3A%221%22%7D; device_view=full; cookies_consented=1; spkessid=a9fgibmrcdncv0ssmm1jkcileq; locale=en; _ga=GA1.2.619053130.1693297829; _gid=GA1.2.46064692.1700163205; _hjIncludedInSessionSample_1199008=0; _hjSession_1199008=eyJpZCI6ImVhZjM3NGEwLTgyZjgtNDhiOC04N2Y0LTlkNTVhZTNmZDEyMCIsImNyZWF0ZWQiOjE3MDAxNjMyMzY3NzMsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=1; LPSID-85738142=KxGPb1nzTMqfaM3ALcWvpw; _ga_5KBWG85NE7=GS1.1.1700163203.162.1.1700163491.60.0.0',
      'Referer': 'https://www.ke.sportpesa.com/en/sports-betting/football-1/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
      'X-App-Timezone': 'Africa/Nairobi',
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    sports = response.json()
    i = 0
    for sport in sports:
        if sport['name'] == "Football":
            countries = sport['countries']
            for country in countries:
                country_id = country['id']
                country_name = country['name']
                leagues = country['leagues']
                for league in leagues:
                    league_id = league['id']
                    league_name = league['name']
                    i += 1
                    print(i)
                    print(f'{country_id}- ---- {country_name} ------ {league_id} ---- {league_name}')

get_countries()