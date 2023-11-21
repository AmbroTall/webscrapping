import pandas as pd
from thefuzz import process
from db import *
from match import Match
import time
import network_utils as nu

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'Referer': 'https://www.nairabet.com/',
    'content-type': 'application/json',
    'Origin': 'https://www.nairabet.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}
def nairabetALP():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=ARGENTINA_PRIMERA_DIVISION&marketId=1x2"
  return nairabetGetData(url, "ALP")
def nairabetBSA():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=BRAZIL_SERIE_A"
  return nairabetGetData(url, "BSA")
def nairabetBSB():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=BRAZIL_SERIE_B"
  return nairabetGetData(url, "BSB")
def nairabetCPA():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=COLOMBIA_PRIMERA_A"
  return nairabetGetData(url, "CPA")
def nairabetCPB():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=COLOMBIA_PRIMERA_B"
  return nairabetGetData(url, "CPB")
def nairabetPP():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=PARAGUAY_PRIMERA_DIVISION"
  return nairabetGetData(url, "PP")
def nairabetELP():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=ECUADOR_LIGA_PRO_SERIE_A"
  return nairabetGetData(url, "ELP")
def nairabetPL1():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=PERU_PRIMERA_DIVISION"
  return nairabetGetData(url, "PL1")
def nairabetUSD():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=URUGUAY_SEGUNDA_DIVISION"
  return nairabetGetData(url, "USD")
def nairabetBPD():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=BOLIVIA_PROFESSIONAL_FOOTBALL_LEAGUE"
  return nairabetGetData(url, "BPD")
def nairabetMLM():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=MEXICO_PRIMERA_DIVISION"
  return nairabetGetData(url, "MLM")
def nairabetUSM():
  url = "https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=US_MAJOR_LEAGUE_SOCCER"
  return nairabetGetData(url, "USM")

def nairabetEPL():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=EN_PR'
  return nairabetGetData(url, "EPL")
def nairabetEFL():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=EN_D1'
  return nairabetGetData(url, "EFL")
def nairabetSP():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=LD_SP'
  return nairabetGetData(url, "SP")
def nairabetIFD():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=IRELAND_LEAGUE_DIVISION_1'
  return nairabetGetData(url, "IFD")
def nairabetIPD():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=IRELAND_PREMIER_LEAGUE'
  return nairabetGetData(url, "IPD")
def nairabetSPD():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=ES_PL'
  return nairabetGetData(url, "SPD")
def nairabetSSD():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=SPAIN_SEGUNDA_DIVISION'
  return nairabetGetData(url, "SSD")
def nairabetFL1():
  url = 'https://sports-api.nairabet.com/v2/events?country=NG&locale=en&group=g3&platform=desktop&sportId=SOCCER&competitionId=FR_L1'
  return nairabetGetData(url, "FL1")

def nairabetGetData(url, tag):
  urls = []
  response = nu.make_request(url, headers)
  nairabet_dict = {"Name": "Nairabet", "Matches": []}
  if(response and 'data' in response and 'categories' in response['data'] and len(response['data']['categories'])>0):
    event_list = [int(event['id']) for event in response['data']['categories'][0]['competitions'][0]['events']]
    for event in event_list:
      urls.append(f"https://sports-api.nairabet.com/v2/events/{event}?country=NG&locale=en&group=g3&platform=desktop")
    responses = nu.fetch_data(urls, headers)
    nairabet_dict = nairabetExtractData(tag, responses)
  return nairabet_dict

def nairabetExtractData(tag, responses):
  matches = []
  for response in responses:
      if(not response):
        continue
      match_data = response.json()
      over = {}
      under = {}
      dnb = []
      ggng = []
      dc = []
      fh = []
      fh_dnb = []
      fh_ggng = []
      fh_odd_even = [] #???
      odd_even = [] #including overtime?
      first_goal = []
      sh1x2 = []
      ltts = []
      sh_ggng = []
      draw_odd = 0
      name1 = match_data['eventNames'][0]
      name2 = match_data['eventNames'][1]
      name = f"{name1} - {name2}"
      for marketgroup in match_data['marketGroups']:
        if(marketgroup['name'] == 'Main'):
          markets = marketgroup['markets']
          for market in markets:
            if(market['name'] == "1x2"):
              home_odd = float(market['outcomes'][0]['value'])
              draw_odd = float(market['outcomes'][1]['value'])
              away_odd = float(market['outcomes'][2]['value'])
            if(market['name'] == "Draw No Bet" and len(market['outcomes']) == 2):
              dnb.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))
            if(market['name'] == "Double Chance" and len(market['outcomes']) == 3):
              dc.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']), float(market['outcomes'][1]['value'])))
            if(market['entityName'] == "Total Goals - Over/Under 2.5" or market['entityName'] == 'Total Goals - Total Goals 2.5'):
              over[2.5] = float(market['outcomes'][1]['value'])
              under[2.5] = float(market['outcomes'][0]['value'])
            elif(market['entityName'] == 'Total Goals (O/U)'):
              for odd in market['outcomes']:
                if(odd['name'] == "Over 2.5"): over[2.5] = float(odd['value'])
                if(odd['name'] == "Under 2.5"): under[2.5] = float(odd['value'])
            if(market['entityName'] == "Both Teams To Score" and len(market['outcomes']) == 2):
              if(market['outcomes'][0]['name'] == "Yes"):
                ggng.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))
              else:
                ggng.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
        if(marketgroup['name'] == '1st Half'):
          markets2 = marketgroup['markets']
          for market in markets2:
            if(market['entityName'] == "First Half Result" and len(market['outcomes']) == 3):
                fh.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']), float(market['outcomes'][1]['value'])))
            if(market['entityName'] == "Both Teams To Score In 1st Half"  and len(market['outcomes']) == 2):
                if(market['outcomes'][0]['name'] == "Yes"):
                    fh_ggng.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))
                else:
                    fh_ggng.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
        if(marketgroup['name'] == 'Goals'):
          markets3 = marketgroup['markets']
          for market in markets3:
            if(market['entityName'] == "First Team to Score" and len(market['outcomes']) == 3):
                first_goal.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][2]['value']), float(market['outcomes'][0]['value'])))
            if(market['entityName'] == "Last Team to Score" and len(market['outcomes']) == 3):
                ltts.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][2]['value']), float(market['outcomes'][0]['value'])))
        if(marketgroup['name'] == '2nd Half'):
            markets4 = marketgroup['markets']
            for market in markets4:
              if(market['entityName'] == "Second Half Result" and len(market['outcomes']) == 3):
                sh1x2.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][2]['value']), float(market['outcomes'][1]['value'])))
              if(market['entityName'] == "Both Teams To Score In 2nd Half"):
                if(market['outcomes'][0]['name'] == "Yes"):
                    sh_ggng.extend((float(market['outcomes'][0]['value']), float(market['outcomes'][1]['value'])))
                else:
                    sh_ggng.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))
        if(marketgroup['name'] == 'Others'):
            markets5 = marketgroup['markets']
            for market in markets5:
              if(market['entityName'] == "Match (inc OT) Odd/Even"):
                odd_even.extend((float(market['outcomes'][1]['value']), float(market['outcomes'][0]['value'])))

      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dnb=dnb, dc=dc, fh1x2=fh,
                    ggng=ggng, fh_dnb=fh_dnb, fh_ggng=fh_ggng, odd_even=odd_even, fh_odd_even=fh_odd_even, fg=first_goal, sh1x2=sh1x2, ltts=ltts, 
                    sh_ggng=sh_ggng)
      matches.append(match)

  nairabet_dict = {"Name": "Nairabet", "Matches": matches}
  return nairabet_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeNairabetALPTeamName,
        "BSA": normalizeNairabetBSATeamName,
        "BSB": normalizeNairabetBSBTeamName,
        "CPA": normalizeNairabetCPATeamName,
        "CPB": normalizeNairabetCPBTeamName,
        "PP": normalizeNairabetPPTeamName,
        "ELP": normalizeNairabetELPTeamName,
        "PL1": normalizeNairabetPL1TeamName,
        "USD": normalizeNairabetUSDTeamName,
        "BPD": normalizeNairabetBPDTeamName,
        "MLM": normalizeNairabetMLMTeamName,
        "USM": normalizeNairabetUSMTeamName,
        'EPL': normalizeNairabetEPLTeamName,
        'EFL': normalizeNairabetEFLTeamName,
        'SP': normalizeNairabetSPTeamName,
        'IFD': normalizeNairabetIFDTeamName,
        'IPD': normalizeNairabetIPDTeamName,
        'SPD': normalizeNairabetSPDTeamName,
        'SSD': normalizeNairabetSSDTeamName,
        'FL1': normalizeNairabetFL1TeamName
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeNairabetALPTeamName(team_name):
  correct_name = team_name
  if("Central Cordoba Rosario" in team_name):
    correct_name = "Central Cordoba SDE"
  elif("Gimnasia LP" in team_name):
    correct_name = "Esgrima La Plata"
  else:
    correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizeNairabetBSATeamName(team_name):
  if(team_name == "Atletico Mineiro"):
     return "Atletico Mineiro"
  else:
    correct_name = process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
  return correct_name
def normalizeNairabetBSBTeamName(team_name):
  correct_name = process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
  return correct_name
def normalizeNairabetCPATeamName(team_name):
  correct_name = process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
  return correct_name
def normalizeNairabetCPBTeamName(team_name):
  correct_name = process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
  return correct_name 
def normalizeNairabetPPTeamName(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeNairabetELPTeamName(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeNairabetPL1TeamName(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeNairabetUSDTeamName(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeNairabetBPDTeamName(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeNairabetMLMTeamName(team_name):
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeNairabetMLMTeamName(team_name):
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeNairabetUSMTeamName(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeNairabetEPLTeamName(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeNairabetEFLTeamName(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeNairabetSPTeamName(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeNairabetIFDTeamName(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeNairabetIPDTeamName(team_name):
  if(team_name == 'UCD'): return 'Uni College Dublin'
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeNairabetSPDTeamName(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeNairabetSSDTeamName(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeNairabetFL1TeamName(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]

if __name__ == '__main__':
    nairabet_dict = nairabetEPL()
    pd.set_option('display.max_colwidth', None)
    nairabetdF = pd.DataFrame.from_dict(nairabet_dict)
    print(nairabetdF)

