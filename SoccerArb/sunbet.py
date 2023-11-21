import pandas as pd
from match import Match
from thefuzz import process
from db import *
from unidecode import unidecode
import json
import network_utils as nu

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://sunbet.co.za/',
'Origin': 'https://sunbet.co.za',
'Connection': 'keep-alive',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site',
'TE': 'trailers'
}

def sunbetALP():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/argentina/liga_profesional_argentina/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1683650486151&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "ALP")
def sunbetBSA():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/brazil/brasileirao_serie_a/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&useCombined=true&useCombinedLive=true"   
   return sunbetGetData(url, "BSA")
def sunbetBSB():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/brazil/brasileirao_serie_b/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "BSB")
def sunbetCPA():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/colombia/liga_betplay_dimayor/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "CPA")
def sunbetCPB():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/colombia/torneo_betplay_dimayor/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1684802548331&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "CPB")
def sunbetELP():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/ecuador/liga_pro/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1684972498087&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "ELP")
def sunbetPL1():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/peru/liga_1/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1685184430316&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "PL1")
def sunbetUSD():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/uruguay/segunda_division/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1685191856182&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "USD")
def sunbetBPD():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/bolivia/liga_profesional_bolivia/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1685194985435&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "BPD")
def sunbetMLM():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/mexico/liga_mx/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1685205222829&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "MLM")
def sunbetUSM():
   url = "https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/usa/mls/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1685213599955&useCombined=true&useCombinedLive=true"
   return sunbetGetData(url, "USM")

def sunbetEPL():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/england/premier_league/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691180953452&useCombined=true'
   return sunbetGetData(url, "EPL")
def sunbetEFL():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/england/the_championship/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691411412240&useCombined=true'
   return sunbetGetData(url, "EFL")
def sunbetEL1():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/england/league_one/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691411003875&useCombined=true'
   return sunbetGetData(url, "EL1")
def sunbetEL2():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/england/league_two/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691452144756&useCombined=true'
   return sunbetGetData(url, "EL2")
def sunbetSP():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/scotland/scottish_premiership/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691622391896&useCombined=true'
   return sunbetGetData(url, "SP")
def sunbetSC():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/scotland/championship/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691772816777&useCombined=true'
   return sunbetGetData(url, "SC")
def sunbetIFD():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/ireland/1st_division/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691768340738&useCombined=true'
   return sunbetGetData(url, "IFD")
def sunbetIPD():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/ireland/premier_division/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691768383560&useCombined=true'
   return sunbetGetData(url, "IPD")
def sunbetSPD():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/spain/la_liga/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691850436263&useCombined=true'
   return sunbetGetData(url, "SPD")
def sunbetSSD():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/spain/la_liga_2/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691872481425&useCombined=true'
   return sunbetGetData(url, "SSD")
def sunbetFL1():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/france/ligue_1/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1691928225882&useCombined=true'
   return sunbetGetData(url, "FL1")
def sunbetFL2():
   url = 'https://eu-offering-api.kambicdn.com/offering/v2018/siwc/listView/football/france/ligue_2/all/matches.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1692010671256&useCombined=true'
   return sunbetGetData(url, "FL2")

def sunbetGetData(url, tag):
   urls = []
   response = nu.make_request(url, headers)
   sunbet_dict = {"Name":"Sunbet", "Matches": []}
   if(response and 'events' in response):
      event_list = [event['event']['id'] for event in response['events']]
      for event in event_list:
         urls.append(f"https://eu-offering-api.kambicdn.com/offering/v2018/siwc/betoffer/event/{event}.json?lang=en_ZA&market=ZA&client_id=2&channel_id=1&ncid=1684066083268&includeParticipants=true")
      responses = nu.fetch_data(urls, headers)
      sunbet_dict = sunbetExtractData(tag, responses)
   return sunbet_dict

def sunbetExtractData(tag, responses):
  matches = []
  for response in responses:
      if(not response):
         continue
      match_data = response.json()
      if(match_data['events'][0]['state'] == 'STARTED'):
          continue
      over = {}
      under = {}
      dnb = []
      ggng = []
      fh = []
      dc_data = []
      draw_odd = 0
      fh_dnb = []
      fh_ggng = []
      sh_dnb = []
      sh_ggng = []
      sh_m = []
      odd_even = []
      name = match_data['events'][0]['name']
      name1 = name.split(" - ")[0]
      name2 = name.split(" - ")[1]
      markets = match_data['betOffers']
      for market in markets:
         if(market['criterion']['label'] == "Full Time"):
            home_odd = float(market['outcomes'][0]['odds'])/1000
            away_odd = float(market['outcomes'][2]['odds'])/1000
            draw_odd = float(market['outcomes'][1]['odds'])/1000
         if(market['criterion']['label'] == "Double Chance"):
            x1 = float(market['outcomes'][0]['odds'])/1000
            x2 = float(market['outcomes'][2]['odds'])/1000
            x12 = float(market['outcomes'][1]['odds'])/1000
            dc_data.extend((x1, x2, x12))
         if(market['criterion']['label'] == "Draw No Bet"):
            dnb.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))
         if(market['criterion']['label'] == "Total Goals" and market['outcomes'][0]['line'] == 2500):
            over[2.5] = float(market['outcomes'][0]['odds'])/1000
            under[2.5] = float(market['outcomes'][1]['odds'])/1000
         if(market['criterion']['label'] == "Half Time"):
            fh.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000, 
                       float(market['outcomes'][1]['odds'])/1000))
         if(market['criterion']['label'] == "Both Teams To Score"):
            ggng.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][1]['odds'])/1000))
         if(market['criterion']['label'] == "Draw No Bet - 1st Half"):
            fh_dnb.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))
         if(market['criterion']['label'] == "Both Teams To Score - 1st Half"):
            fh_ggng.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))
         if(market['criterion']['label'] == "Draw No Bet - 2nd Half"):
            sh_dnb.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))
         if(market['criterion']['label'] == "Both Teams To Score - 2nd Half"):
            sh_ggng.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))
         if(market['criterion']['label'] == "2nd Half"):
            sh_m.extend((float(market['outcomes'][0]['odds'])/1000, float(market['outcomes'][2]['odds'])/1000, 
                         float(market['outcomes'][1]['odds'])/1000))
         if(market['criterion']['label'] == "Total Goals Odd/Even"):
            odd_even.extend((market['outcomes'][0]['odds']/1000, market['outcomes'][1]['odds']/1000))

      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=dc_data, dnb=dnb, fh1x2=fh,
                    ggng=ggng, fh_dnb=fh_dnb, fh_ggng=fh_ggng, sh_dnb=sh_dnb, sh_ggng=sh_ggng, sh1x2=sh_m)
      matches.append(match)
  sunbet_dict = {"Name":"Sunbet", "Matches": matches}
  return sunbet_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizesunbetALPTeamNames,
        "BSA": normalizesunbetBSATeamNames,
        "BSB": normalizesunbetBSBTeamNames,
        "CPA": normalizesunbetCPATeamNames,
        "CPB": normalizesunbetCPBTeamNames,
        "ELP": normalizesunbetELPTeamNames,
        "PL1": normalizesunbetPL1TeamNames,
        "USD": normalizesunbetUSDTeamNames,
        "BPD": normalizesunbetBPDTeamNames,
        "MLM": normalizesunbetMLMTeamNames,
        "USM": normalizesunbetUSMTeamNames,
        'EPL': normalizesunbetEPLTeamNames,
        'EFL': normalizesunbetEFLTeamNames,
        'EL1': normalizesunbetEL1TeamNames,
        'EL2': normalizesunbetEL2TeamNames,
        'SP': normalizesunbetSPTeamNames,
        'SC': normalizesunbetSCTeamNames,
        'IFD': normalizesunbetIFDTeamNames,
        'IPD': normalizesunbetIPDTeamNames,
        'SPD': normalizesunbetSPDTeamNames,
        'SSD': normalizesunbetSSDTeamNames,
        'FL1': normalizesunbetFL1TeamNames,
        'FL2': normalizesunbetFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizesunbetALPTeamNames(team_name):
  correct_name = team_name
  if(team_name == "Central Córdoba de Santiago del Estero"):
     correct_name = "Central Cordoba SDE"
  elif(team_name == "Unión de Santa Fe"):
     correct_name = "Union"
  else: 
     correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizesunbetBSATeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizesunbetBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizesunbetCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizesunbetCPBTeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizesunbetELPTeamNames(team_name):
  if(team_name == "Universidad Católica (ECU)"):
     return "Catolica del Ecuador"
  else:
   correct_name = process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
  return correct_name    
def normalizesunbetPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizesunbetUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizesunbetBPDTeamNames(team_name):
  return process.extract(unidecode(team_name), Bolivia_Primera, limit=1)[0][0]
def normalizesunbetMLMTeamNames(team_name):
  return process.extract(unidecode(team_name), Mexico_Liga_MX, limit=1)[0][0]
def normalizesunbetUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizesunbetEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizesunbetEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizesunbetEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizesunbetEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizesunbetSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizesunbetSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizesunbetIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizesunbetIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizesunbetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizesunbetSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizesunbetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizesunbetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    sunbet_dict = sunbetEPL()
    pd.set_option('display.max_colwidth', None)
    dF = pd.DataFrame.from_dict(sunbet_dict)
    print(dF)