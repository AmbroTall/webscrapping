import pandas as pd
from match import Match
from thefuzz import process
from db import *
import network_utils as nu
import requests

market_urls = ["https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/536/14",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/560/16",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/535/14",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/562/16",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/577/17",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/579/17",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/563/16",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/580/17",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/553/14",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/568/16",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/827/48",
               "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/tourn_id/821/48"]
headers = {
  'authority': 'sportsapicdn-desktop.betking.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
  'cache-control': 'no-cache',
  'dnt': '1',
  'origin': 'https://www.betking.com',
  'pragma': 'no-cache',
  'referer': 'https://www.betking.com/',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
def betkingALP():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522800/531/14"
    return betkingGetData(url, "ALP")
def betkingBSA():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/894/0/0"
    return betkingGetData(url, "BSA")
def betkingBSB():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1201/0/0"
    return betkingGetData(url, "BSB")
def betkingCPA():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/2926087/0/0"
    return betkingGetData(url, "CPA")
def betkingCPB():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522818/0/0"
    return betkingGetData(url, "CPB")
def betkingPP():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522843/0/0"
    return betkingGetData(url, "PP")
def betkingELP():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522822/0/0"
    return betkingGetData(url, "ELP")
def betkingPL1():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522847/0/0"
    return betkingGetData(url, "PL1")
def betkingUSD():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522859/0/0"
    return betkingGetData(url, "USD")
def betkingBPD():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522806/0/0"
    return betkingGetData(url, "BPD")
def betkingMLM():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1797260/0/0"
    return betkingGetData(url, "MLM")
def betkingUSM():
    url = "https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1720049/0/0"
    return betkingGetData(url, "USM")

def betkingEPL():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/841/0/0'
    return betkingGetData(url, "EPL")
def betkingEFL():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/863/0/0'
    return betkingGetData(url, "EFL")
def betkingEL1():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/909/0/0'
    return betkingGetData(url, "EL1")
def betkingEL2():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/939/0/0'
    return betkingGetData(url, "EL2")
def betkingSP():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522762/0/0'
    return betkingGetData(url, "SP")
def betkingSC():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522766/0/0'
    return betkingGetData(url, "SC")
def betkingIFD():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522760/0/0'
    return betkingGetData(url, "IFD")
def betkingIPD():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1522757/0/0'
    return betkingGetData(url, "IPD")
def betkingSPD():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1108/0/0'
    return betkingGetData(url, "SPD")
def betkingSSD():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/6274/0/0'
    return betkingGetData(url, "SSD")
def betkingFL1():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1104/0/0'
    return betkingGetData(url, "FL1")
def betkingFL2():
    url = 'https://sportsapicdn-desktop.betking.com/api/feeds/prematch/en/4/1179/0/0'
    return betkingGetData(url, "FL2")

def betkingGetData(url, tag):
  response = nu.make_request(url, headers)
  betking_dict = {"Name":"Betking", "Matches": []}
  if(response != None and 'AreaMatches' in response and len(response["AreaMatches"])>0):
    t_id = str(response["AreaMatches"][0]["Items"][0]['TournamentId'])
    for i in range(len(market_urls)):
        market_urls[i] = market_urls[i].replace('tourn_id', t_id)
    responses = nu.fetch_data(market_urls, headers)
    ordered_rs = order_responses(responses)
    betking_dict = betkingExtractData(response, tag, get_wager(ordered_rs[0]), get_wager(ordered_rs[1]), get_wager(ordered_rs[2]),
                                       get_wager(ordered_rs[3]), get_wager(ordered_rs[4]), get_wager(ordered_rs[5]), get_wager(ordered_rs[6]),
                                       get_wager(ordered_rs[7]), get_wager(ordered_rs[8]), get_wager(ordered_rs[9]), get_wager(ordered_rs[10]),
                                       get_wager(ordered_rs[11]))
  return betking_dict  

def order_responses(responses):
   wager_types = {
      'Draw No Bet': [],
      'GG/NG': [],
      'Odd/Even Goals': [],
      '1st Half - 1X2': [],
      '1st Half - Draw No Bet': [],
      '1st Half - Both Teams to Score': [],
      '1st Half - Odd/Even Goals': [],
      '2nd Half - 1X2': [],
      '2nd Half - Draw No Bet': [],
      '2nd Half - Both Teams to Score': [],
      'First Team Goal': [],
      'Last Team Goal': [],
   }
   ggng_r = []
   oddeven_r = []
   dnb_r = []
   fh1x2_r = []
   fh_dnb_r = []
   fh_ggng_r = []
   fh_oe_r = []
   sh1x2_r = []
   sh_dnb_r = []
   sh_ggng_r = []
   fg_r = []
   lg_r = []
   for resp in responses:
      r = []
      if(resp):
        r = resp.json()
      if(r and 'AreaMatches' in r and r["AreaMatches"] and r["AreaMatches"][0]["Items"] and r["AreaMatches"][0]["AreaMarkets"]):
         wager_type = r["AreaMatches"][0]["AreaMarkets"][0]['OddsType']['OddsTypeName']
         if(wager_type in wager_types):
            wager_types[wager_type] = r
   for key in wager_types:
      if(key == 'GG/NG'):
        ggng_r = wager_types[key]
      if(key == 'Draw No Bet'):
        dnb_r = wager_types[key]
      if(key == 'Odd/Even Goals'):
        oddeven_r = wager_types[key]
      if(key == '1st Half - 1X2'):
        fh1x2_r = wager_types[key]
      if(key == '1st Half - Draw No Bet'):
        fh_dnb_r = wager_types[key]
      if(key == '1st Half - Both Teams to Score'):
        fh_ggng_r = wager_types[key]
      if(key == '1st Half - Odd/Even Goals'):
        fh_oe_r = wager_types[key]
      if(key == '2nd Half - 1X2'):
        sh1x2_r = wager_types[key]
      if(key == '2nd Half - Draw No Bet'):
        sh_dnb_r = wager_types[key]
      if(key == '2nd Half - Both Teams to Score'):
        sh_ggng_r = wager_types[key]
      if(key == 'First Team Goal'):
        fg_r = wager_types[key]
      if(key == 'Last Team Goal'):
        lg_r = wager_types[key]
         
   responses = [dnb_r, fh1x2_r, ggng_r, fh_dnb_r, sh1x2_r, sh_dnb_r, fh_ggng_r, sh_ggng_r, oddeven_r, fh_oe_r, fg_r, lg_r]
   return responses

def get_wager(response):
    if('AreaMatches' in response and response["AreaMatches"] and response["AreaMatches"][0]["Items"]):
      return response["AreaMatches"][0]["Items"]
    return []

def betkingExtractData(soccer_data, tag, dnb_data, fh12x_data, ggng_data, fhdnb_data, sh12x_data, shdnb_data, fhggng_data, 
                       shggng_data, oe_data, fhoe_data, fg_data, lg_data):
    matches = []
    i = 0
    for match in soccer_data["AreaMatches"][0]["Items"]:
        lg = []
        oe = []
        fg = []
        sh_m = []
        ggng = []
        fh_oe = []
        fh_dnb = []
        sh_dnb = []
        fh_ggng = []
        sh_ggng = []
        dnb_list = []
        fh12x_list = []
        double_chance = []
        name = match["ItemName"]
        name1 = name.split(" - ")[0].strip()
        name2 = name.split(" - ")[1].strip()
        if(dnb_data and i < len(dnb_data) and name == dnb_data[i]["ItemName"] and len(dnb_data[i]["OddsCollection"][0]["MatchOdds"]) >= 2):
          dnb1 = (dnb_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"])
          dnb2 = (dnb_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"])
          dnb_list = [dnb1, dnb2]
        if(fh12x_data and i < len(fh12x_data) and name == fh12x_data[i]["ItemName"] and len(fh12x_data[i]["OddsCollection"][0]["MatchOdds"]) >= 3):
          fh1 = (fh12x_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"])
          fh2 = (fh12x_data[i]["OddsCollection"][0]["MatchOdds"][2]["Outcome"]["OddOutcome"])
          fhx = (fh12x_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"])
          fh12x_list = [fh1, fh2, fhx]
        if(sh12x_data and i < len(sh12x_data) and name == sh12x_data[i]["ItemName"]):
          sh1 = (sh12x_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"])
          sh2 = (sh12x_data[i]["OddsCollection"][0]["MatchOdds"][2]["Outcome"]["OddOutcome"])
          shx = (sh12x_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"])
          sh_m = [sh1, sh2, shx]
        home_odd = (match["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"])
        draw_odd = (match["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"])
        away_odd = (match["OddsCollection"][0]["MatchOdds"][2]["Outcome"]["OddOutcome"])
        if(len(match["OddsCollection"][1]["MatchOdds"]) == 3):
          dc_1x = (match["OddsCollection"][1]["MatchOdds"][0]["Outcome"]["OddOutcome"])
          dc_12 = (match["OddsCollection"][1]["MatchOdds"][1]["Outcome"]["OddOutcome"])
          dc_2x = (match["OddsCollection"][1]["MatchOdds"][2]["Outcome"]["OddOutcome"])
          double_chance.extend((dc_1x, dc_2x, dc_12))
        over = {2.5 : match["OddsCollection"][2]["MatchOdds"][0]["Outcome"]["OddOutcome"]}
        under = {2.5 : match["OddsCollection"][2]["MatchOdds"][1]["Outcome"]["OddOutcome"]}
        if(ggng_data and i < len(ggng_data) and name == ggng_data[i]["ItemName"]):
          ggng.extend((ggng_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                       ggng_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(fhggng_data and i < len(fhggng_data) and name == fhggng_data[i]["ItemName"]):
          fh_ggng.extend((fhggng_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                          fhggng_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(shggng_data and i < len(shggng_data) and name == shggng_data[i]["ItemName"]):
          sh_ggng.extend((shggng_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                          shggng_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(fhdnb_data and i < len(fhdnb_data) and name == fhdnb_data[i]["ItemName"]):
          fh_dnb.extend((fhdnb_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                         fhdnb_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(shdnb_data and i < len(shdnb_data) and name == shdnb_data[i]["ItemName"]):
          sh_dnb.extend((shdnb_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                         shdnb_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(oe_data and i < len(oe_data) and name == oe_data[i]["ItemName"]):
          oe.extend((oe_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                     oe_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(fhoe_data and i < len(fhoe_data) and name == fhoe_data[i]["ItemName"]):
          fh_oe.extend((fhoe_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                        fhoe_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(fg_data and i < len(fg_data) and name == fg_data[i]["ItemName"]):
          fg.extend((fg_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                     fg_data[i]["OddsCollection"][0]["MatchOdds"][2]["Outcome"]["OddOutcome"],
                     fg_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"]))
        if(lg_data and i < len(lg_data) and name == lg_data[i]["ItemName"]):
          lg.extend((lg_data[i]["OddsCollection"][0]["MatchOdds"][0]["Outcome"]["OddOutcome"], 
                     lg_data[i]["OddsCollection"][0]["MatchOdds"][1]["Outcome"]["OddOutcome"],
                     lg_data[i]["OddsCollection"][0]["MatchOdds"][2]["Outcome"]["OddOutcome"]))
        i += 1
        name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
        match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=double_chance, dnb=dnb_list,
                      fh1x2=fh12x_list, ggng=ggng, fh_dnb=fh_dnb, fh_ggng=fh_ggng, fh_odd_even=fh_oe, odd_even=oe, sh1x2=sh_m, sh_dnb=sh_dnb,
                      sh_ggng=sh_ggng, fg=fg, ltts=lg)
        matches.append(match)

    betking_dict = {"Name":"Betking", "Matches": matches}
    return betking_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeBetkingALPTeamNames,
        "BSA": normalizeBetkingBSATeamNames,
        "BSB": normalizeBetkingBSBTeamNames,
        "CPA": normalizeBetkingCPATeamNames,
        "CPB": normalizeBetkingCPBTeamNames,
        "PP": normalizeBetkingPPTeamNames,
        "ELP": normalizeBetkingELPTeamNames,
        "PL1": normalizeBetkingPL1TeamNames,
        "USD": normalizeBetkingUSDTeamNames,
        "BPD": normalizeBetkingBPDTeamNames,
        "MLM": normalizeBetkingMLMTeamNames,
        "USM": normalizeBetkingUSMTeamNames,
        'EPL': normalizeBetkingEPLTeamNames,
        'EFL': normalizeBetkingEFLTeamNames,
        'EL1': normalizeBetkingEL1TeamNames,
        'EL2': normalizeBetkingEL2TeamNames,
        'SP': normalizeBetkingSPTeamNames,
        'SC': normalizeBetkingSCTeamNames,
        'IFD': normalizeBetkingIFDTeamNames,
        'IPD': normalizeBetkingIPDTeamNames,
        'SPD': normalizeBetkingSPDTeamNames,
        'SSD': normalizeBetkingSSDTeamNames,
        'FL1': normalizeBetkingFL1TeamNames,
        'FL2': normalizeBetkingFL2TeamNames
    }

    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeBetkingALPTeamNames(team_name):
  correct_name = team_name
  if("CA Central Cordoba SE" == team_name):
      correct_name = "Central Cordoba SDE"
  else:
    correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizeBetkingBSATeamNames(team_name):
  correct_name = team_name
  if("CA Paranaense PR" == team_name):
    return "Atletico PR"
  elif("Atletico Mineiro MG" == team_name):
    return "Atletico MG"
  else:
    correct_name = process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
  return correct_name
def normalizeBetkingBSBTeamNames(team_name):
  if(team_name == "AC Goianiense GO"):
     return "Atletico-GO"
  else:
    correct_name = process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
  return correct_name
def normalizeBetkingCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeBetkingCPBTeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeBetkingPPTeamNames(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeBetkingELPTeamNames(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeBetkingPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeBetkingUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeBetkingBPDTeamNames(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeBetkingMLMTeamNames(team_name):
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeBetkingUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeBetkingEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeBetkingEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeBetkingEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeBetkingEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeBetkingSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeBetkingSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeBetkingIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeBetkingIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeBetkingSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeBetkingSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeBetkingFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeBetkingFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    betking_dict = betkingEPL()
    pd.set_option('display.max_colwidth', None)
    betkingdF = pd.DataFrame.from_dict(betking_dict)
    print(betkingdF)