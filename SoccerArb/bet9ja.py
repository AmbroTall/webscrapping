import pandas as pd
from match import Match
from thefuzz import process
from db import *
import time
import network_utils as nu

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Referer': 'https://sports.bet9ja.com/sportPage/1/competitions',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'TE': 'trailers'
}
def bet9jaALP():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1599390&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "ALP")
def bet9jaBSA():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=964311&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "BSA")
def bet9jaBSB():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1500335&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "BSB")
def bet9jaCPA():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=2344147&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "CPA")
def bet9jaCPB():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1427139&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "CPB")
def bet9jaPP():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1279442&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "PP")
def bet9jaELP():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1300552&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "ELP")
def bet9jaPL1():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1995124&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "PL1")
def bet9jaUSD():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1513082&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "USD")
def bet9jaBPD():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1340265&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "BPD")
def bet9jaMLM():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1458792&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "MLM")
def bet9jaUSM():
  url = "https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1387346&DISP=0&GROUPMARKETID=1&matches=false"
  return bet9jaGetData(url, headers, "USM")

def bet9jaEPL():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=170880&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "EPL")
def bet9jaEFL():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=170881&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "EFL")
def bet9jaEL1():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=995354&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "EL1")
def bet9jaEL2():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=995355&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "EL2")
def bet9jaSP():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=941378&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "SP")
def bet9jaSC():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1075222&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "SC")
def bet9jaIFD():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1370426&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "IFD")
def bet9jaIPD():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=1345657&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "IPD")
def bet9jaSPD():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=180928&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "SPD")
def bet9jaSSD():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=180929&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "SSD")
def bet9jaFL1():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=950503&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "FL1")
def bet9jaFL2():
  url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID=958691&DISP=0&GROUPMARKETID=1&matches=false'
  return bet9jaGetData(url, headers, "FL2")

def bet9jaGetData(url, headers, tag):
  urls = []
  response = nu.make_request(url, headers)
  bet9ja_dict = {"Name":"Bet9ja", "Matches": []}
  if(response != None and 'D' in response and 'E' in response['D']):
    event_list = [event['ID'] for event in response['D']['E']]
    for event in event_list:
      urls.append(f"https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEvent?EVENTID={event}")
    responses = nu.fetch_data(urls, headers)
    bet9ja_dict = bet9jaExtractData(tag, responses)
  return bet9ja_dict

def bet9jaExtractData(tag, responses):
  matches = []
  for response in responses:
      if(not response):
        continue
      resp = response.json()
      if('D' not in resp):
        continue
      match_data = resp['D']
      odds = match_data['O']
      dc_data = []
      fh1_data = []
      fh_dnb = []
      fh_ggng = []
      fh_odd_even = []
      odd_even = []
      first_goal = []
      sh1x2 = []
      ltts = []
      sh_dnb = []
      sh_ggng = []
      dnb = []
      ggng = []
      over = {}
      under = {}
      d_odd = 0
      h_odd = 0
      a_odd = 0
      d_odd = 0
      name = match_data['DS']
      name1 = name.split(" - ")[0]
      name2 = name.split(" - ")[1]
      if('S_1X2_1' in odds and 'S_1X2_2' in odds and 'S_1X2_X' in odds):
        h_odd = float(odds['S_1X2_1'])
        a_odd = float(odds['S_1X2_2'])
        d_odd = float(odds['S_1X2_X'])
      if('S_DC_1X' in odds and 'S_DC_X2' in odds and 'S_DC_12' in odds):
        dc_data.extend((float(odds['S_DC_1X']), float(odds['S_DC_X2']), float(odds['S_DC_12'])))
      if('S_OU@2.5_O' in odds and 'S_OU@2.5_U' in odds):
        over[2.5] = float(odds['S_OU@2.5_O'])
        under[2.5] = float(odds['S_OU@2.5_U'])
      if('S_DNB_1' in odds and 'S_DNB_2' in odds):
        dnb.extend((float(odds['S_DNB_1']), float(odds['S_DNB_2'])))
      if('S_1X21T_1' in odds and 'S_1X21T_2' in odds and 'S_1X21T_X' in odds):
        fh1_data.extend((float(odds['S_1X21T_1']), float(odds['S_1X21T_2']), float(odds['S_1X21T_X'])))
      if('S_GGNG_Y' in odds and 'S_GGNG_N' in odds):
        ggng.extend((float(odds['S_GGNG_Y']), float(odds['S_GGNG_N'])))
      if('S_GGNG2T_Y' in odds and 'S_GGNG2T_N' in odds):
        sh_ggng.extend((float(odds['S_GGNG2T_Y']), float(odds['S_GGNG2T_N'])))
      if('S_DNB2T_1' in odds and 'S_DNB2T_2' in odds):  
        sh_dnb.extend((float(odds['S_DNB2T_1']), float(odds['S_DNB2T_2'])))
      if('S_LASTSCORE_1' in odds and 'S_LASTSCORE_1' in odds and 'S_LASTSCORE_2' in odds and 'S_LASTSCORE_N' in odds):
        ltts.extend((float(odds['S_LASTSCORE_1']), float(odds['S_LASTSCORE_2']), float(odds['S_LASTSCORE_N'])))
      if('S_1X22T_1' in odds and 'S_1X22T_2' in odds and 'S_1X22T_1' in odds and 'S_1X22T_X' in odds):
        sh1x2.extend((float(odds['S_1X22T_1']), float(odds["S_1X22T_2"]), float(odds['S_1X22T_X'])))
      if('S_1STGOAL_1' in odds and 'S_1STGOAL_2' in odds and 'S_1STGOAL_X' in odds):
        first_goal.extend((float(odds['S_1STGOAL_1']), float(odds["S_1STGOAL_2"]), float(odds['S_1STGOAL_X'])))
      if('S_OE_OD' in odds and 'S_OE_EV' in odds):
        odd_even.extend((float(odds['S_OE_OD']), float(odds['S_OE_EV'])))
      if('S_OE1T_OD' in odds and 'S_OE1T_EV' in odds):
        fh_odd_even.extend((float(odds['S_OE1T_OD']), float(odds['S_OE1T_EV'])))
      if('S_GGNG1T_Y' in odds and 'S_GGNG1T_N' in odds):
        fh_ggng.extend((float(odds['S_GGNG1T_Y']), float(odds['S_GGNG1T_N'])))
      if('S_DNB1T_1' in odds and 'S_DNB1T_2' in odds):
        fh_dnb.extend((float(odds['S_DNB1T_1']), float(odds['S_DNB1T_2'])))
      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd, over=over, under=under, dc=dc_data, dnb=dnb,
                    fh1x2=fh1_data, ggng=ggng, fh_dnb=fh_dnb, fh_ggng=fh_ggng, odd_even=odd_even, fh_odd_even=fh_odd_even,
                    fg=first_goal, sh1x2=sh1x2, ltts=ltts, sh_dnb=sh_dnb, sh_ggng=sh_ggng)
      matches.append(match)

  bet9ja_dict = {"Name":"Bet9ja", "Matches": matches}
  return bet9ja_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeBet9jaALPTeamNames,
        "BSA": normalizeBet9jaBSATeamNames,
        "BSB": normalizeBet9jaBSBTeamNames,
        "CPA": normalizeBet9jaCPATeamNames,
        "CPB": normalizeBet9jaCPBTeamNames,
        "PP": normalizeBet9jaPPTeamNames,
        "ELP": normalizeBet9jaELPTeamNames,
        "PL1": normalizeBet9jaPL1TeamNames,
        "USD": normalizeBet9jaUSDTeamNames,
        "BPD": normalizeBet9jaBPDTeamNames,
        "MLM": normalizeBet9jaMLMTeamNames,
        "USM": normalizeBet9jaUSMTeamNames,
        "EPL": normalizeBet9jaEPLTeamNames,
        'EFL': normalizeBet9jaEFLTeamNames,
        'EL1': normalizeBet9jaEL1TeamNames,
        'EL2': normalizeBet9jaEL2TeamNames,
        'SP': normalizeBet9jaSPTeamNames,
        'SC': normalizeBet9jaSCTeamNames,
        'IFD': normalizeBet9jaIFDTeamNames,
        'IPD': normalizeBet9jaIPDTeamNames,
        'SPD': normalizeBet9jaSPDTeamNames,
        'SSD': normalizeBet9jaSSDTeamNames,
        'FL1': normalizeBet9jaFL1TeamNames,
        'FL2': normalizeBet9jaFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeBet9jaALPTeamNames(team_name):
  correct_name = team_name
  if("Tallares de Cordoba" == team_name):
      correct_name = "Talleres"
  elif("Atletico Rosario" == team_name):
      correct_name = "Rosario Central"
  else:
    correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
  return correct_name
def normalizeBet9jaBSATeamNames(team_name):
  return process.extractOne(team_name, Brazil_Serie_A)[0]
def normalizeBet9jaBSBTeamNames(team_name):
  return process.extractOne(team_name, Brazil_Serie_B)[0]
def normalizeBet9jaCPATeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_A)[0]
def normalizeBet9jaCPBTeamNames(team_name):
  return process.extractOne(team_name, Colombia_Primera_B)[0]
def normalizeBet9jaPPTeamNames(team_name):
  return process.extractOne(team_name, Paraguay_Primera)[0]
def normalizeBet9jaELPTeamNames(team_name):
  return process.extractOne(team_name, Ecuador_ProLiga)[0]
def normalizeBet9jaPL1TeamNames(team_name):
  return process.extractOne(team_name, Peru_Liga1)[0]
def normalizeBet9jaUSDTeamNames(team_name):
  return process.extractOne(team_name, Uruguay_Seg_Div)[0]
def normalizeBet9jaBPDTeamNames(team_name):
  return process.extractOne(team_name, Bolivia_Primera)[0]
def normalizeBet9jaMLMTeamNames(team_name):
  return process.extractOne(team_name, Mexico_Liga_MX)[0]
def normalizeBet9jaUSMTeamNames(team_name):
  return process.extractOne(team_name, UnitedS_Major_League)[0]
def normalizeBet9jaEPLTeamNames(team_name):
  return process.extractOne(team_name, English_Premier_League)[0]
def normalizeBet9jaEFLTeamNames(team_name):
  return process.extractOne(team_name, English_Football_League)[0]
def normalizeBet9jaEL1TeamNames(team_name):
  return process.extractOne(team_name, English_League_One)[0]
def normalizeBet9jaEL2TeamNames(team_name):
  return process.extractOne(team_name, English_League_Two)[0]
def normalizeBet9jaSPTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Premiership)[0]
def normalizeBet9jaSCTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Championship)[0]
def normalizeBet9jaIFDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_First_Division)[0]
def normalizeBet9jaIPDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_Premier_Division)[0]
def normalizeBet9jaSPDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Primera_Division)[0]
def normalizeBet9jaSSDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Segunda_Division)[0]
def normalizeBet9jaFL1TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue1)[0]
def normalizeBet9jaFL2TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue2)[0]

if __name__ == '__main__':
  bet9ja_dict = bet9jaBSA()
  pd.set_option('display.max_colwidth', None)
  bet9jadF = pd.DataFrame.from_dict(bet9ja_dict)
  print(bet9jadF)

