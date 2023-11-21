import json
import pandas as pd
from match import Match
from thefuzz import process
from db import *
import network_utils as nu
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept': '*/*',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json',
    'Referer': 'https://www.sportybet.com/ng/sport/football/',
    'clientid': 'web',
    'operid': '2',
    'platform': 'web',
    'Origin': 'https://www.sportybet.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers'
}
def sportybetALP():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60", #60 - 1st Half 1x2
        "tournamentId": [
        [
            "sr:tournament:155"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "ALP")
def sportybetBSA():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
        {
            "sportId": "sr:sport:1",
            "marketId": "1,18,10,29,11,26,36,14,60",
            "tournamentId": [
                [
                    "sr:tournament:325"
                ]
            ]
        }
    ])

    return sportybetGetData(url, payload, "BSA")
def sportybetBSB():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:390"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "BSB")
def sportybetCPA():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:27070"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "CPA")
def sportybetCPB():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:1238"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "CPB")
def sportybetPP():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:27098"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "PP")
def sportybetELP():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:240"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "ELP")
def sportybetPL1():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:406"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "PL1")
def sportybetUSD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:1908"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "USD")   
def sportybetBPD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:33980"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "BPD")
def sportybetMLM():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:27466"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "MLM")
def sportybetUSM():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:242"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "USM")

def sportybetEPL():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:17"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "EPL")
def sportybetEFL():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:18"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "EFL")
def sportybetEL1():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:24"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "EL1")
def sportybetEL2():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:25"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "EL2")
def sportybetSP():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:36"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "SP")
def sportybetSC():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:206"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "SC")
def sportybetIFD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:193"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "IFD")
def sportybetIPD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:192"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "IPD")
def sportybetSPD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:8"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "SPD")
def sportybetSSD():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:54"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "SSD")
def sportybetFL1():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:34"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "FL1")
def sportybetFL2():
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = json.dumps([
    {
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14,60",
        "tournamentId": [
        [
            "sr:tournament:182"
        ]
        ]
    }
    ])
    return sportybetGetData(url, payload, "FL2")

def sportybetGetData(url, payload, tag):
    final_dict = {"Name":"SportyBet", "Matches": []}
    event_list = []
    urls = []
    response = nu.make_request(url, headers, payload, post=True)
    if(response and 'data' in response and response['data'] and 'events' in response['data'][0]):
        event_list = [event['eventId'].split('match:')[-1] for event in response['data'][0]['events']]
        for event in event_list:
           urls.append(f"https://www.sportybet.com/api/ng/factsCenter/event?eventId=sr%3Amatch%3A{event}")
        responses = nu.fetch_data(urls, headers)
        final_dict = sportybetExtractData(responses, tag)
    return final_dict

def sportybetExtractData(responses, tag):
  matches = []
  for response in responses:
      match_data = []
      if(not response):
         continue
      try:
        match_data = response.json()
      except json.JSONDecodeError as json_error:
        print("Sportybet JSON decoding error:", json_error)
      if(not match_data or 'data' not in match_data):
         continue
      match_data = match_data['data']
      dc_data = []
      dnb = []
      fh = []
      oe = []
      lg = []
      fg = []
      sh_m = []
      fhfg = []
      ggng = []
      fhoe = []
      fhdnb = []
      shdnb = []
      shggng = []
      fhggng = []
      over = {}
      under = {}
      draw_odd = 0
      name1 = match_data['homeTeamName']
      name2 = match_data['awayTeamName']
      name = f"{name1} - {name2}"
      markets = match_data['markets']
      if(markets):
        for market in markets:
            if(market['desc'] == "1X2"):
                home_odd = float(market['outcomes'][0]['odds'])
                away_odd = float(market['outcomes'][2]['odds'])
                draw_odd = float(market['outcomes'][1]['odds'])
            if(market['desc'] == "Double Chance"):
                dc_data.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][2]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "Over/Under" and market['specifier'] == "total=2.5"):
                over[2.5] = float(market['outcomes'][0]['odds'])
                under[2.5] = float(market['outcomes'][1]['odds'])
            if(market['desc'] == "Draw No Bet"):
                dnb.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Half - Draw No Bet"):
                fhdnb.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "2nd Half - Draw No Bet"):
                shdnb.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Half - 1X2"):
                fh.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][2]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "GG/NG"):
                ggng.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Half - GG/NG"):
                fhggng.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "2nd Half - GG/NG"):
                shggng.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Goal"):
                fg.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][2]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Half - 1st Goal"):
                fhfg.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "Last Goal"):
                lg.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "Odd/Even"):
                oe.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "1st Half - Odd/Even"):
                fhoe.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][1]['odds'])))
            if(market['desc'] == "2nd Half - 1X2"):
                sh_m.extend((float(market['outcomes'][0]['odds']), float(market['outcomes'][2]['odds']), float(market['outcomes'][1]['odds'])))

      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=dc_data, dnb=dnb,
                    fh1x2=fh, ggng=ggng, fg=fg, fh_fg=fhfg, fh_ggng=fhggng, fh_dnb=fhdnb, fh_odd_even=fhoe, ltts=lg, odd_even=oe,
                    sh1x2=sh_m, sh_dnb=shdnb, sh_ggng=shggng)
      matches.append(match)

  bet9ja_dict = {"Name":"SportyBet", "Matches": matches}
  return bet9ja_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeSportBetALPTeamNames,
        "BSA": normalizeSportBetBSATeamNames,
        "BSB": normalizeSportBetBSBTeamNames,
        "CPA": normalizeSportBetCPATeamNames,
        "CPB": normalizeSportBetCPBTeamNames,
        "PP": normalizeSportBetPPTeamNames,
        "ELP": normalizeSportBetELPTeamNames,
        "PL1": normalizeSportBetPL1TeamNames,
        "USD": normalizeSportBetUSDTeamNames,
        "BPD": normalizeSportBetBPDTeamNames,
        "MLM": normalizeSportBetMLMTeamNames,
        "USM": normalizeSportBetUSMTeamNames,
        'EPL': normalizeSportBetEPLTeamNames,
        'EFL': normalizeSportBetEFLTeamNames,
        'EL1': normalizeSportBetEL1TeamNames,
        'EL2': normalizeSportBetEL2TeamNames,
        'SP': normalizeSportBetSPTeamNames,
        'SC': normalizeSportBetSCTeamNames,
        'IFD': normalizeSportBetIFDTeamNames,
        'IPD': normalizeSportBetIPDTeamNames,
        'SPD': normalizeSportBetSPDTeamNames,
        'SSD': normalizeSportBetSSDTeamNames,
        'FL1': normalizeSportBetFL1TeamNames,
        'FL2': normalizeSportBetFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeSportBetALPTeamNames(team_name):
  correct_name = team_name
  if("CA Central Cordoba SE" == team_name):
      correct_name = "Central Cordoba SDE"
  else:
    correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizeSportBetBSATeamNames(team_name):
  if(team_name == "Atletico Mineiro MG"):
     return "Atletico Mineiro"
  elif(team_name == "CA Paranaense PR"):
     return "Atletico PR"
  else:
    correct_name = process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
  return correct_name
def normalizeSportBetBSBTeamNames(team_name):
  if(team_name == "AC Goianiense GO"):
     return "Atletico-GO"
  correct_name = process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
  return correct_name
def normalizeSportBetCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeSportBetCPBTeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeSportBetPPTeamNames(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeSportBetELPTeamNames(team_name):
  if(team_name == "CD Universidad Catolica del Ecuador"):
    return "Catolica del Ecuador"
  else:
    correct_name = process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
  return correct_name 
def normalizeSportBetPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeSportBetUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeSportBetBPDTeamNames(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeSportBetMLMTeamNames(team_name):
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeSportBetUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeSportBetEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeSportBetEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeSportBetEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeSportBetEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeSportBetSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeSportBetSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeSportBetIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeSportBetIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeSportBetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeSportBetSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeSportBetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeSportBetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]
   
if __name__ == '__main__':
    sportybet_dict = sportybetEPL()
    pd.set_option('display.max_colwidth', None)
    sportybetdF = pd.DataFrame.from_dict(sportybet_dict)
    print(sportybetdF)
