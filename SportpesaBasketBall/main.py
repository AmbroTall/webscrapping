import requests
import json


def get_scores_by_phase(score_by_phases, current_phase):
    home_score = score_by_phases.get('homeScore', {}).get(f'phase{current_phase}', 0)
    away_score = score_by_phases.get('awayScore', {}).get(f'phase{current_phase}', 0)
    total_score = home_score + away_score

    return home_score, away_score, total_score


url = "https://sportpesa.betstream.betgenius.com/widget-data/multisportgametracker?productName=sportpesa&region=&country=KE&fixtureId=10499617&activeContent=court&sport=Basketball&sportId=4&getAllTabsData=false&matchActionsSourceId=&culture\\[0\\]=en-US&live=false&phase="

payload={}
headers = {
  'authority': 'sportpesa.betstream.betgenius.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'application/json',
  'if-none-match': 'W/"64e-71wGlGbuN5wzRYnjBy6SBsomjek"',
  'referer': 'https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/html?eventId=10430757',
  'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("GET", url, headers=headers, data=payload)
re = response.json()
r = response.json()['data']['scoreboardInfo']
if 'NBA' in re['data']['matchInfo']['seasonName']:
    total_quarter_secs = 720
else:
    total_quarter_secs = 600
total_away_score = r['awayScore']
total_home_score = r['homeScore']
current_home_score, current_away_score, total_scores = get_scores_by_phase(r['scoreByPhases'], r['currentPhase'])
home_time_outs = r['homeTimeoutsLeft']
away_time_outs = r['awayTimeoutsLeft']
remaining_quarter_secs = r['timeRemainingInPhase']
clock = r['clockAction']['clock']
event = r['clockAction']['event']  #start
game_total_scores = int(r['awayScore']) + int(r['homeScore'])
print(current_home_score, current_away_score, total_scores,remaining_quarter_secs,clock, event, game_total_scores )
print(total_quarter_secs)


def time_str_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = (minutes * 60) + seconds
        return total_seconds
    except ValueError:
        print("Invalid time format. Please provide time in 'mm:ss' format.")

# Example usage:
time_input = "02:58"
result = time_str_to_seconds(time_input)

if result is not None:
    print(f'Total seconds: {result}')



# total_scores, total_quarter_secs, remaining_quarter_secs, game_total_scores