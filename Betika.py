import requests

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

    print(date_time)
    print(f"{home_team} - {home_team_odds}")
    print(f"{away_team} - {away_team_odds}")
    print()

    game["time"] = date_time
    game["home_team"] = home_team
    game["away_team"] = away_team
    game["home_odds"] = home_team_odds
    game["away_odds"] = away_team_odds

    betika.append(game)

print(betika)
