import pandas as pd
from thefuzz import process
from match import Match
from db import *
import json
import network_utils as nu

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
  'Accept': 'application/json',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip',
  'X-Requested-With': 'XMLHttpRequest',
  'Is-srv': 'false',
  'Connection': 'keep-alive',
  'Referer': 'https://betwinner.com/en/line',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'TE': 'trailers'
}
def betwinnerALP():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=119599&count=20&lng=en&tz=2&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "ALP")
def betwinnerBSA():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=1268397&count=20&lng=en&tz=2&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "BSA")
def betwinnerBSB():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=57265&count=20&lng=en&tz=2&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "BSB")
def betwinnerCPA():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=214147&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "CPA")
def betwinnerCPB():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=214149&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "CPB")
def betwinnerPP():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=55479&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "PP")
def betwinnerELP():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=276999&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "ELP")
def betwinnerPL1():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=120503&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "PL1")
def betwinnerBPD():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=119629&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "BPD")
def betwinnerMLM():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=2306111&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "MLM") 
def betwinnerUSM():
  url = "https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=828065&count=20&lng=en&tz=2&mode=4&country=172&partner=152&getEmpty=true&virtualSports=true&gr=495"
  return betwinnerGetData(url, headers, "USM")

def betwinnerEPL():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=88637&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "EPL")
def betwinnerEFL():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=105759&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "EFL")
def betwinnerEL1():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=13709&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "EL1")
def betwinnerEL2():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=24637&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "EL2")
def betwinnerSP():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=13521&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "SP")
def betwinnerSC():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=281713&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "SC")
def betwinnerIFD():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=29975&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "IFD")
def betwinnerIPD():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=119445&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "IPD")
def betwinnerSPD():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=127733&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "SPD")
def betwinnerSSD():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=27687&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "SSD")
def betwinnerFL1():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=12821&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "FL1")
def betwinnerFL2():
  url = 'https://betwinner.com/service-api/LineFeed/Get1x2_VZip?sports=1&champs=12829&count=20&lng=en&mode=4&country=113&partner=152&getEmpty=true&virtualSports=true&gr=495'
  return betwinnerGetData(url, headers, "FL2")

def betwinnerGetData(url, headers, tag):
  r = nu.make_request(url, headers)
  betwinner_dict = {"Name":"BetW", "Matches": []}
  urls = []
  fh_urls = []
  if(r and 'Value' in r):
    event_list = [event['CI'] for event in r['Value'] if 'DI' not in event]
    for event in event_list:
      urls.append(f"https://betwinner.com/service-api/LineFeed/GetGameZip?id={event}&lng=en&isSubGames=true&GroupEvents=true&countevents=250&grMode=4&partner=152&topGroups=&marketType=1")
    responses = nu.fetch_data(urls, headers)
    for resp in responses:
      if(not resp):
        continue
      match_data = resp.json()
      if(not match_data['Value'] or 'SG' not in match_data['Value']):
        continue
      fh_urls.append(f"https://betwinner.com/service-api/LineFeed/GetGameZip?id={match_data['Value']['SG'][0]['CI']}&lng=en&isSubGames=true&GroupEvents=true&countevents=250&grMode=4&partner=152&topGroups=&marketType=1")
    fh_responses = nu.fetch_data(fh_urls, headers)
    betwinner_dict = betwinnerExtractData(r, tag, responses, fh_responses)
  return betwinner_dict 

def betwinnerExtractData(playerdata, tag, responses, fh_responses):
  matches = []
  print(len(responses), len(fh_responses))
  for i in range(len(responses)):
      print(responses[i])
      if(not responses[i]):
        continue
      match_data = responses[i].json()
      if(not match_data):
        continue
      if(i >= len(fh_responses) or not fh_responses[i]):
        continue
      fh_data = fh_responses[i].json()
      if(not fh_data):
        continue
      dc_data = []
      fh = []
      ggng = []
      over = {}
      under = {}
      draw_odd = 0
      name1 = match_data['Value']['O1']
      name2 = match_data['Value']['O2']
      fh_name1 = fh_data['Value']['O1']
      fh_name2 = fh_data['Value']['O2']
      if(name1 != fh_name1 or name2 != fh_name2):
        print(name1, fh_name1)
        print(name2, fh_name2)
        continue
      home_odd = round(float(match_data['Value']['GE'][0]['E'][0][0]['C']), 2)
      away_odd = round(float(match_data['Value']['GE'][0]['E'][2][0]['C']), 2)
      draw_odd = round(float(match_data['Value']['GE'][0]['E'][1][0]['C']), 2)
      if(match_data['Value']['GE'][1]['G'] == 8  and len(match_data['Value']['GE'][1]['E']) == 3): # Double Chance
        dc_data.extend((round(float(match_data['Value']['GE'][1]['E'][0][0]['C']), 2), 
                      round(float(match_data['Value']['GE'][1]['E'][2][0]['C']), 2), round(float(match_data['Value']['GE'][1]['E'][1][0]['C']), 2)))
      if(len(match_data['Value']['GE']) >= 4 and match_data['Value']['GE'][3]['G'] == 17): # OverUnder
          for line1, line2 in zip(match_data['Value']['GE'][3]["E"][0], match_data['Value']['GE'][3]["E"][1]):
            if(line1['P'] == 2.5):
              over[2.5] = round(float(line1['C']), 2)
            if(line2['P'] == 2.5):
              under[2.5] = round(float(line2['C']), 2)
      if(fh_data and fh_data['Error'] == "" and fh_data['Value']['GE'] and fh_data['Value']['GE'][0]['E'] and len(fh_data['Value']['GE'][0]['E']) > 2):
        fh.extend((round(float(fh_data['Value']['GE'][0]['E'][0][0]['C']), 2), round(float(fh_data['Value']['GE'][0]['E'][2][0]['C']), 2),
                   round(float(fh_data['Value']['GE'][0]['E'][1][0]['C']), 2)))
      if(match_data['Value']['GE'][2]['G'] == 19): #19 - BTTS GGNG
        ggng.extend((round(float(match_data['Value']['GE'][2]['E'][0][0]['C']), 2),
                    round(float(match_data['Value']['GE'][2]['E'][1][0]['C']), 2)))
      elif(len(match_data['Value']['GE']) >= 5 and match_data['Value']['GE'][4]['G'] == 19):
        ggng.extend((round(float(match_data['Value']['GE'][4]['E'][0][0]['C']), 2),
                    round(float(match_data['Value']['GE'][4]['E'][1][0]['C']), 2)))
      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      if(name1 == "Home" or name1 == 'Home (Special bets)' or name2 == "Away"):
        continue
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=dc_data, fh1x2=fh, ggng=ggng)
      matches.append(match)
  betwinner_dict = {"Name":"BetW", "Matches": matches}
  return betwinner_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeBetwinnerALPTeamNames,
        "BSA": normalizeBetwinnerBSATeamNames,
        "BSB": normalizeBetwinnerBSBTeamNames,
        "CPA": normalizeBetwinnerCPATeamNames,
        "CPB": normalizeBetwinnerCPBTeamNames,
        "PP": normalizeBetwinnerPPTeamNames,
        "ELP": normalizeBetwinnerELPTeamNames,
        "PL1": normalizeBetwinnerPL1TeamNames,
        "BPD": normalizeBetwinnerBPDTeamNames,
        "MLM": normalizeBetwinnerMLMTeamNames,
        "USM": normalizeBetwinnerUSMTeamNames,
        'EPL': normalizeBetwinnerEPLTeamNames,
        'EFL': normalizeBetwinnerEFLTeamNames,
        'EL1': normalizeBetwinnerEL1TeamNames,
        'EL2': normalizeBetwinnerEL2TeamNames,
        'SP': normalizeBetwinnerSPTeamNames,
        'SC': normalizeBetwinnerSCTeamNames,
        'IFD': normalizeBetwinnerIFDTeamNames,
        'IPD': normalizeBetwinnerIPDTeamNames,
        'SPD': normalizeBetwinnerSPDTeamNames,
        'SSD': normalizeBetwinnerSSDTeamNames,
        'FL1': normalizeBetwinnerFL1TeamNames,
        'FL2': normalizeBetwinnerFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeBetwinnerALPTeamNames(team_name):
  correct_name = team_name
  if("Central Cordoba de Santiago" in team_name):
    correct_name = "Central Cordoba SDE"
  elif("Instituto Atletico Central Cordoba" in team_name):
    correct_name = "Instituto AC Cordoba"
  else:
    correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizeBetwinnerBSATeamNames(team_name):
  correct_name = team_name
  if(team_name == "Gremio Porto Alegrense"):
    return "Gremio"
  elif(team_name == "Clube Atletico Mineiro"):
    return "Atletico MG"
  else:
    correct_name = process.extractOne(team_name, Brazil_Serie_A)[0]
  return correct_name
def normalizeBetwinnerBSBTeamNames(team_name):
  return process.extractOne(team_name, Brazil_Serie_B)[0]
def normalizeBetwinnerCPATeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_A)[0]
def normalizeBetwinnerCPBTeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_B)[0]
def normalizeBetwinnerPPTeamNames(team_name):
  return process.extractOne(team_name, Paraguay_Primera)[0]
def normalizeBetwinnerELPTeamNames(team_name):
  if(team_name == "Universidad Catolica Quito"): 
    return "Catolica del Ecuador"
  else:
    correct_name = process.extractOne(team_name, Ecuador_ProLiga)[0]
  return correct_name
def normalizeBetwinnerPL1TeamNames(team_name):
  return process.extractOne(team_name, Peru_Liga1)[0]
def normalizeBetwinnerBPDTeamNames(team_name):
  return process.extractOne(team_name, Bolivia_Primera)[0]
def normalizeBetwinnerMLMTeamNames(team_name):
  return process.extractOne(team_name, Mexico_Liga_MX)[0]
def normalizeBetwinnerUSMTeamNames(team_name):
  return process.extractOne(team_name, UnitedS_Major_League)[0]
def normalizeBetwinnerEPLTeamNames(team_name):
  return process.extractOne(team_name, English_Premier_League)[0]
def normalizeBetwinnerEFLTeamNames(team_name):
  return process.extractOne(team_name, English_Football_League)[0]
def normalizeBetwinnerEL1TeamNames(team_name):
  return process.extractOne(team_name, English_League_One)[0]
def normalizeBetwinnerEL2TeamNames(team_name):
  return process.extractOne(team_name, English_League_Two)[0]
def normalizeBetwinnerSPTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Premiership)[0]
def normalizeBetwinnerSCTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Championship)[0]
def normalizeBetwinnerIFDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_First_Division)[0]
def normalizeBetwinnerIPDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_Premier_Division)[0]
def normalizeBetwinnerSPDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Primera_Division)[0]
def normalizeBetwinnerSSDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Segunda_Division)[0]
def normalizeBetwinnerFL1TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue1)[0]
def normalizeBetwinnerFL2TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue2)[0]

if __name__ == '__main__':
    betwinner_dict = betwinnerEPL()
    pd.set_option('display.max_colwidth', None)
    betwinnerdF = pd.DataFrame.from_dict(betwinner_dict)
    print(betwinnerdF)