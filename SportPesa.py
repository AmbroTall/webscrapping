import requests
import json
import datetime
import pytz

url = "https://www.ke.sportpesa.com/api/upcoming/games?type=prematch&sportId=2&section=upcoming&markets_layout=multiple&o=startTime&pag_count=15&pag_min=1"

payload={}
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
print(response.text)
r = response.json()


for x in r:
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
  readable_time_zone = dt_eat.strftime("%Y-%m-%d %H:%M:%S %Z")
  print(readable_time_zone)
  print(f"{home_team} - {home_team_odds}")
  print(f"{away_team} - {away_team_odds}")
  print()
