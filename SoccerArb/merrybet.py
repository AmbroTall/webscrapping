import pandas as pd
from match import Match
from thefuzz import process
from db import *
import network_utils as nu
import time

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/json; charset=utf-8',
  'Request-Language': 'en',
  'X-Requested-With': 'XMLHttpRequest',
  'Connection': 'keep-alive',
  'Referer': 'https://www.merrybet.com/sports/events/Soccer/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'TE': 'trailers'
}
def merrybetALP():
  url = "https://www.merrybet.com/rest/market/categories/multi/3368/events"
  return merrybetGetData(url, headers, "ALP")
def merrybetBSA():
  url = "https://www.merrybet.com/rest/market/categories/multi/134/events"
  return merrybetGetData(url, headers, "BSA")
def merrybetBSB():
  url = "https://www.merrybet.com/rest/market/categories/multi/305/events"
  return merrybetGetData(url, headers, "BSB")
def merrybetCPA():
  url = "https://www.merrybet.com/rest/market/categories/multi/47335/events"
  return merrybetGetData(url, headers, "CPA")
def merrybetCPB():
  url = "https://www.merrybet.com/rest/market/categories/multi/30832/events"
  return merrybetGetData(url, headers, "CPB")
def merrybetPP():
  url = "https://www.merrybet.com/rest/market/categories/multi/5482/events"
  return merrybetGetData(url, headers, "PP")
def merrybetELP():
  url = "https://www.merrybet.com/rest/market/categories/multi/16493/events"
  return merrybetGetData(url, headers, "ELP")
def merrybetPL1():
  url = "https://www.merrybet.com/rest/market/categories/multi/109/events"
  return merrybetGetData(url, headers, "PL1")
def merrybetUSD():
  url = "https://www.merrybet.com/rest/market/categories/multi/18742/events"
  return merrybetGetData(url, headers, "USD")
def merrybetBPD():
  url = "https://www.merrybet.com/rest/market/categories/multi/53665/events"
  return merrybetGetData(url, headers, "BPD")
def merrybetMLM():
  url = "https://www.merrybet.com/rest/market/categories/multi/47106/events"
  return merrybetGetData(url, headers, "MLM")
def merrybetUSM():
  url = "https://www.merrybet.com/rest/market/categories/multi/228/events"
  return merrybetGetData(url, headers, "USM")

def merrybetEPL():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1060/events'
  return merrybetGetData(url, headers, "EPL")
def merrybetEFL():
  url = 'https://www.merrybet.com/rest/market/categories/multi/352/events'
  return merrybetGetData(url, headers, "EFL")
def merrybetEL1():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1088/events'
  return merrybetGetData(url, headers, "EL1")
def merrybetEL2():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1090/events'
  return merrybetGetData(url, headers, "EL2")
def merrybetSP():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1091/events'
  return merrybetGetData(url, headers, "SP")
def merrybetSC():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1092/events'
  return merrybetGetData(url, headers, "SC")
def merrybetIFD():
  url = 'https://www.merrybet.com/rest/market/categories/multi/223/events'
  return merrybetGetData(url, headers, "IFD")
def merrybetIPD():
  url = 'https://www.merrybet.com/rest/market/categories/multi/222/events'
  return merrybetGetData(url, headers, "IPD")
def merrybetSPD():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1587/events'
  return merrybetGetData(url, headers, "SPD")
def merrybetSSD():
  url = 'https://www.merrybet.com/rest/market/categories/multi/3347/events'
  return merrybetGetData(url, headers, "SSD")
def merrybetFL1():
  url = 'https://www.merrybet.com/rest/market/categories/multi/1648/events'
  return merrybetGetData(url, headers, "FL1")
def merrybetFL2():
  url = 'https://www.merrybet.com/rest/market/categories/multi/32754/events'
  return merrybetGetData(url, headers, "FL2")

def merrybetGetData(url, headers, tag):
  urls = []
  response = nu.make_request(url, headers)
  merrybet_dict = {"Name":"Merrybet", "Matches": []}
  if(response and 'data' in response):
    event_list = [event['eventId'] for event in response['data']]
    for event in event_list:
      urls.append(f"https://www.merrybet.com/rest/market/events/{event}")
    responses = nu.fetch_data(urls, headers)
    merrybet_dict = merrybetExtractData(responses, tag)
  return merrybet_dict

def merrybetExtractData(responses, tag):
  matches = []
  for response in responses:
      if(not response):
        continue
      resp = response.json()
      game = resp['data']
      draw_odd = 0
      over = {}
      under = {}
      fg = []
      lg = []
      oe = []
      dnb = []
      fhoe = []
      fhfg = []
      ggng = []
      fh_m = []
      sh_m = []
      fh_dnb = []
      sh_dnb = []
      dc_data = []
      fh_ggng = []
      sh_ggng = []
      name = game['eventName']
      name1 = name.split(" - ")[0]
      name2 = name.split(" - ")[1]
      eventgames = game['eventGames']
      home_odd = float(eventgames[0]['outcomes'][0]['outcomeOdds'])
      away_odd = float(eventgames[0]['outcomes'][2]['outcomeOdds'])
      draw_odd = float(eventgames[0]['outcomes'][1]['outcomeOdds'])
      for eventgame in eventgames:
        if(eventgame['gameName'] == "Double chance"):
          dc_data.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "Under/Over 2.5 goals"):
          over[2.5] = eventgame['outcomes'][1]['outcomeOdds']
          under[2.5] = eventgame['outcomes'][0]['outcomeOdds']
        if(eventgame['gameName'] == "1st half - 1x2"):
          fh_m.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "2nd half - 1x2"):
          sh_m.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "Both teams to score"):
          ggng.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "1st half - Both teams to score"):
          fh_ggng.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "2nd half - Both teams to score"):
          sh_ggng.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "Draw no bet"):
          dnb.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "1st half - Draw no bet"):
          fh_dnb.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "2nd half - Draw no bet"):
          sh_dnb.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "1st goal"):
          fg.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if(eventgame['gameName'] == "1st half - 1st goal"):
          fhfg.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if(eventgame['gameName'] == "Last goal"):
          lg.extend((eventgame['outcomes'][1]['outcomeOdds'], eventgame['outcomes'][2]['outcomeOdds'], eventgame['outcomes'][0]['outcomeOdds']))
        if(eventgame['gameName'] == "Total goals - Odd/Even"):
          oe.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
        if(eventgame['gameName'] == "1st half - Odd/Even"):
          fhoe.extend((eventgame['outcomes'][0]['outcomeOdds'], eventgame['outcomes'][1]['outcomeOdds']))
      if('Home Teams' in name1 or 'Away Teams' in name1):
        continue
      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=dc_data, dnb=dnb, fh1x2=fh_m,
                    ggng=ggng, sh1x2=sh_m, fh_dnb=fh_dnb, sh_dnb=sh_dnb, fh_ggng=fh_ggng, sh_ggng=sh_ggng, fg=fg, ltts=lg, fh_fg=fhfg,
                    odd_even=oe, fh_odd_even=fhoe)
      matches.append(match)

  merrybet_dict = {"Name":"Merrybet", "Matches": matches}
  return merrybet_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizemerrybetALPTeamNames,
        "BSA": normalizemerrybetBSATeamNames,
        "BSB": normalizemerrybetBSBTeamNames,
        "CPA": normalizemerrybetCPATeamNames,
        "CPB": normalizemerrybetCPBTeamNames,
        "PP": normalizemerrybetPPTeamNames,
        "ELP": normalizemerrybetELPTeamNames,
        "PL1": normalizemerrybetPL1TeamNames,
        "USD": normalizemerrybetUSDTeamNames,
        "BPD": normalizemerrybetBPDTeamNames,
        "MLM": normalizemerrybetMLMTeamNames,
        "USM": normalizemerrybetUSMTeamNames,
        'EPL': normalizemerrybetEPLTeamNames,
        'EFL': normalizemerrybetEFLTeamNames,
        'EL1': normalizemerrybetEL1TeamNames,
        'EL2': normalizemerrybetEL2TeamNames,
        'SP': normalizemerrybetSPTeamNames,
        'SC': normalizemerrybetSCTeamNames,
        'IFD': normalizemerrybetIFDTeamNames,
        'IPD': normalizemerrybetIPDTeamNames,
        'SPD': normalizemerrybetSPDTeamNames,
        'SSD': normalizemerrybetSPDTeamNames,
        'FL1': normalizemerrybetFL1TeamNames,
        'FL2': normalizemerrybetFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizemerrybetALPTeamNames(team_name):
  correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizemerrybetBSATeamNames(team_name):
  if(team_name == "CA Paranaense PR"):
    return "Atletico PR"
  else:
    correct_name = process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
  return correct_name
def normalizemerrybetBSBTeamNames(team_name):
  if(team_name == "AC Goianiense GO"):
    return "Atletico-GO"
  correct_name = process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
  return correct_name
def normalizemerrybetCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizemerrybetCPBTeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizemerrybetPPTeamNames(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizemerrybetELPTeamNames(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizemerrybetPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizemerrybetUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizemerrybetBPDTeamNames(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizemerrybetMLMTeamNames(team_name):
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizemerrybetUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizemerrybetEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizemerrybetEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizemerrybetEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizemerrybetEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizemerrybetSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizemerrybetSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizemerrybetIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizemerrybetIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizemerrybetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizemerrybetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizemerrybetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizemerrybetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    merrybet_dict = merrybetEPL()
    pd.set_option('display.max_colwidth', None)
    dF = pd.DataFrame.from_dict(merrybet_dict)
    print(dF)