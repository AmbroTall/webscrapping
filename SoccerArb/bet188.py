from playwright.sync_api import sync_playwright
import pandas as pd
from match import Match
from thefuzz import process
from db import *
import time
import network_utils as nu
import random

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=',
  'Authorization': '',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'DNT': '1',
  'DeviceType': 'Web',
  'Origin': 'https://sports.188bet-sports.com',
  'Pragma': 'no-cache',
  'Referer': 'https://sports.188bet-sports.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
}

def getBearerToken():
  final_token = 'Bearer '
  token = ''
  with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        leagues = [26726, 27325, 26470, 26326, 27068, 26281, 28649, 27250, 26526]
        id = random.choice(leagues)
        url = f'https://sports.188bet-sports.com/en-gb/sports/match-by-sport/football/main_markets?c=124&u=https://www.188bet.com&competition={id}'
        page.goto(url)
        page.wait_for_function('''() => {
            return sessionStorage.getItem('JWT') !== null;
        }''')
        # Retrieve the token from local storage
        token = page.evaluate('''() => {
            return sessionStorage.getItem('JWT');
        }''')
  update_token(final_token + token)

def update_token(new_token):
    headers['Authorization'] = new_token

def bet188BSA():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/29083/premium"
  return bet188GetData(url, headers, "BSA")
def bet188BSB():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/27938/premium"
  return bet188GetData(url, headers, "BSB")
def bet188CPA():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/27314/premium"
  return bet188GetData(url, headers, "CPA")
def bet188CPB():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/34222/premium"
  return bet188GetData(url, headers, "CPB")
def bet188USM():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26862/premium"
  return bet188GetData(url, headers, "USM")

def bet188EPL():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26726/premium"
  return bet188GetData(url, headers, "EPL")
def bet188EL1():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/27325/premium"
  return bet188GetData(url, headers, "EL1")
def bet188EL2():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26470/premium"
  return bet188GetData(url, headers, "EL2")
def bet188EFL():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26326/premium"
  return bet188GetData(url, headers, "EFL")
def bet188SPD():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/27068/premium"
  return bet188GetData(url, headers, "SPD")
def bet188SSD():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26281/premium"
  return bet188GetData(url, headers, "SSD")
def bet188FL1():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/28649/premium"
  return bet188GetData(url, headers, "FL1")
def bet188FL2():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/27250/premium"
  return bet188GetData(url, headers, "FL2")
def bet188IFD():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/26526/premium"
  return bet188GetData(url, headers, "IFD")
def bet188SP():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/29042/premium"
  return bet188GetData(url, headers, "SP")
def bet188SC():
  getBearerToken()
  url = "https://landing-sports-api.188bet-sports.com/api/v2/en-gb/ROW/sport/1/mop/competition/28864/premium"
  return bet188GetData(url, headers, "SC")

def bet188GetData(url, headers, tag):
  response = nu.make_request(url, headers)
  bet188_dict = {"Name":"188bet", "Matches": []}
  urls = []
  if(response != None and 'd' in response and 's' in response['d'] and 'c' in response['d']['s'] and response['d']['s']['c'] and
    'e' in response['d']['s']['c'][0]):
    event_list = [event['id'] for event in response['d']['s']['c'][0]['e']]
    for event in event_list:
      urls.append(f"https://landing-sports-api.188bet-sports.com/api/v1/en-gb/ROA/event/{event}")
    responses = nu.fetch_data(urls, headers, proxy_type='https')
    bet188_dict = bet188ExtractData(tag, responses)
  return bet188_dict

def bet188ExtractData(tag, responses):
  matches = []
  for response in responses:
    if(not response):
      continue
    resp = response.json()
    if(not resp or 'd' not in resp or 'e' not in resp['d']):
      continue
    match_data = resp['d']['e']
    ht = match_data['h']
    at = match_data['a']
    fh_ggng = []
    fh_odd_even = []
    odd_even = []
    first_goal = []
    fh1x2 = []
    ltts = []
    ggng = []
    d_odd = 0
    h_odd = 0
    a_odd = 0
    d_odd = 0
    markets = match_data['ml']
    for market in markets:
      if('n' in market and market['n'] == '1 X 2'):
        h_odd = float(market['o'][0]['v'])
        a_odd = float(market['o'][1]['v'])
        d_odd = float(market['o'][2]['v'])
      if('n' in market and market['n'] == '1 X 2 - 1st Half'):
        fh1x2.extend((float(market['o'][0]['v']), float(market['o'][1]['v']), float(market['o'][2]['v'])))
      if('n' in market and market['n'] == 'Both Teams to Score'):
        ggng.extend((float(market['o'][0]['v']), float(market['o'][1]['v'])))
      if('n' in market and market['n'] == 'Both Teams to Score - 1st Half'):
        fh_ggng.extend((float(market['o'][0]['v']), float(market['o'][1]['v'])))
      if('n' in market and market['n'] == 'Goals: Odd / Even'):
        odd_even.extend((round(float(market['o'][0]['v']) + 1, 2), round(float(market['o'][1]['v']) + 1, 2))) # +1 bcs odds are represented as fractional odd/1
      if('n' in market and market['n'] == 'Goals: Odd / Even - 1st Half'):
        odd = float(market['o'][0]['v'])
        even = float(market['o'][1]['v'])
        if(odd < 0): odd = 1/abs(odd) + 1
        if(even < 0): even = 1/abs(even) + 1
        if(odd <= 1): odd = odd + 1
        if(even <= 1): even = even + 1
        fh_odd_even.extend((round(odd, 2), round(even, 2)))
      if(market['t'] == 'FT_TTS'):
        first_goal.extend((float(market['o'][0]['v']), float(market['o'][1]['v']), float(market['o'][2]['v'])))
        ltts.extend((float(market['o'][3]['v']), float(market['o'][4]['v']), float(market['o'][2]['v'])))

    name = f"{normalizeName(tag, ht)} - {normalizeName(tag, at)}"
    match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd, fh1x2=fh1x2, ggng=ggng, fh_ggng=fh_ggng,
                  odd_even=odd_even, fh_odd_even=fh_odd_even, fg=first_goal, ltts=ltts)
    matches.append(match)

  bet188_dict = {"Name":"188bet", "Matches": matches}
  return bet188_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "EPL": normalize188betEPLTeamNames,
        'EL1': normalize188betEL1TeamNames,
        'EL2': normalize188betEL2TeamNames,
        'EFL': normalize188betEFLTeamNames,
        'SPD': normalize188betSPDTeamNames,
        'SSD': normalize188betSSDTeamNames,
        'FL1': normalize188betFL1TeamNames,
        'FL2': normalize188betFL2TeamNames,
        'IFD': normalize188betIFDTeamNames,
        'SC': normalize188betSCTeamNames,
        'SP': normalize188betSPTeamNames,
        'BSA': normalize188betBSATeamNames,
        'BSB': normalize188betBSBTeamNames,
        'CPA': normalize188betCPATeamNames,
        'CPB': normalize188betCPBTeamNames,
        'USM': normalize188betUSMTeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalize188betEPLTeamNames(team_name):
  return process.extractOne(team_name, English_Premier_League)[0]
def normalize188betEL1TeamNames(team_name):
  return process.extractOne(team_name, English_League_One)[0]
def normalize188betEL2TeamNames(team_name):
  return process.extractOne(team_name, English_League_Two)[0]
def normalize188betEFLTeamNames(team_name):
  return process.extractOne(team_name, English_Football_League)[0]
def normalize188betSPDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Primera_Division)[0]
def normalize188betSSDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Segunda_Division)[0]
def normalize188betFL1TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue1)[0]
def normalize188betFL2TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue2)[0]
def normalize188betIFDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_First_Division)[0]
def normalize188betSCTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Championship)[0]
def normalize188betSPTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Premiership)[0]
def normalize188betBSATeamNames(team_name):
  if(team_name == 'Atletico Mineiro'): return 'Atletico MG'
  return process.extractOne(team_name, Brazil_Serie_A)[0]
def normalize188betBSBTeamNames(team_name):
  return process.extractOne(team_name, Brazil_Serie_B)[0]
def normalize188betCPATeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_A)[0]
def normalize188betCPBTeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_B)[0]
def normalize188betUSMTeamNames(team_name):
  return process.extractOne(team_name, UnitedS_Major_League)[0]

if __name__ == '__main__':
  print("Ambrsoe")
  bet188_dict = bet188EFL()
  pd.set_option('display.max_colwidth', None)
  bet188dF = pd.DataFrame.from_dict(bet188_dict)
  print(bet188dF)