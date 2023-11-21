import pandas as pd
from match import Match
from thefuzz import process
from db import *
import time
import network_utils as nu

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Origin': 'https://campeonbet.com',
  'Connection': 'keep-alive',
  'Referer': 'https://campeonbet.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'TE': 'trailers'
}

def campeonbetALP():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3075&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-11T17%3A24%3A00.000Z&endDate=2023-05-18T17%3A24%3A00.000Z"
  return campeonbetGetData(url, "ALP") 
def campeonbetBSA():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=11318&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-16T23%3A32%3A00.000Z&endDate=2023-05-23T23%3A32%3A00.000Z"
  return campeonbetGetData(url, "BSA") 
def campeonbetBSB():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=11005&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-17T20%3A04%3A00.000Z&endDate=2023-05-24T20%3A04%3A00.000Z"
  return campeonbetGetData(url, "BSB") 
def campeonbetCPA():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3857&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-22T23%3A20%3A00.000Z&endDate=2023-05-29T23%3A20%3A00.000Z"
  return campeonbetGetData(url, "CPA") 
def campeonbetCPB():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=4009&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-23T00%3A15%3A00.000Z&endDate=2023-05-30T00%3A15%3A00.000Z"
  return campeonbetGetData(url, "CPB") 
def campeonbetPP():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=729&champids=0&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-24T23%3A38%3A00.000Z&endDate=2023-05-31T23%3A38%3A00.000Z"
  return campeonbetGetData(url, "PP") 
def campeonbetELP():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=4564&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-25T00%3A24%3A00.000Z&endDate=2023-06-01T00%3A24%3A00.000Z"
  return campeonbetGetData(url, "ELP") 
def campeonbetPL1():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=4042&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-27T10%3A22%3A00.000Z&endDate=2023-06-03T10%3A22%3A00.000Z"
  return campeonbetGetData(url, "PL1") 
def campeonbetUSD():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=10288&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-28T12%3A17%3A00.000Z&endDate=2023-06-04T12%3A17%3A00.000Z"
  return campeonbetGetData(url, "USD") 
def campeonbetBPD():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=518&champids=0&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-27T13%3A28%3A00.000Z&endDate=2023-06-03T13%3A28%3A00.000Z"
  return campeonbetGetData(url, "BPD") 
def campeonbetMLM():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=10009&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-27T16%3A20%3A00.000Z&endDate=2023-06-03T16%3A20%3A00.000Z"
  return campeonbetGetData(url, "MLM") 
def campeonbetUSM():
  url = "https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=SI&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=4610&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2023-05-27T18%3A38%3A00.000Z&endDate=2023-06-03T18%3A38%3A00.000Z"
  return campeonbetGetData(url, "USM") 

def campeonbetEPL():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=66&categoryids=0&champids=2936&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "EPL") 
def campeonbetEFL():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2937&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "EFL")
def campeonbetEL1():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2947&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "EL1")
def campeonbetEL2():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2946&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "EL2")
def campeonbetSP():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3023&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "SP")
def campeonbetSC():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2962&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "SC")
def campeonbetIFD():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=4208&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "IFD")
def campeonbetIPD():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3571&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "IPD")
def campeonbetSPD():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2941&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "SPD")
def campeonbetSSD():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3111&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "SSD")
def campeonbetFL1():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=2943&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "FL1")
def campeonbetFL2():
  url = 'https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&countryCode=MK&deviceType=Desktop&numformat=en&integration=campeonbet&sportids=0&categoryids=0&champids=3143&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0'
  return campeonbetGetData(url, "FL2")

def campeonbetGetData(url, tag):
  urls = []
  response = nu.make_request(url, headers)
  campeon_dict = {"Name":"Campeon", "Matches": []}
  if(response and 'Result' in response and 'Items' in response['Result'] and len(response['Result']['Items'])>0):
    event_list = [event['Id'] for event in response['Result']['Items'][0]['Events']]
    for event in event_list:
       urls.append(f"https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEventDetails?timezoneOffset=-120&langId=8&skinName=campeonbet&configId=12&culture=en-GB&deviceType=Desktop&numformat=en&integration=campeonbet&eventId={event}&sportId=66")
    responses = nu.fetch_data(urls, headers)
    campeon_dict = campeonbetExtractData(tag, responses)
  return campeon_dict  

def campeonbetExtractData(tag, responses):
  matches = []
  for response in responses:
      if(not response):
         continue
      fg = []
      oe = []
      lg = []
      dnb = []
      shm = []
      ggng = []
      fh_m = []
      fh_oe = []
      fh_fg = []
      fh_dnb = []
      sh_dnb = []
      dc_data = []
      fh_ggng = []
      sh_ggng = []
      over = {}
      under = {}
      draw_odd = 0
      home_odd = 0
      away_odd = 0
      match_data = response.json()
      name1 = match_data['Result']['Name'].split("vs.")[0].strip()
      name2 = match_data['Result']['Name'].split("vs.")[1].strip()
      
      if(not match_data['Result']['MarketGroups']):
         continue
      
      marketgroups = match_data['Result']['MarketGroups']
      for marketgroup in marketgroups:
        if(marketgroup['Name'] == 'Main'):
          markets = marketgroup['Items']
          for market in markets:
              if(market['Name'] == "1x2"):
                  home_odd = round(market['Items'][0]['Price'], 2)
                  away_odd = round(market['Items'][2]['Price'], 2)
                  draw_odd = round(market['Items'][1]['Price'], 2)
              if(market['Name'] == "Double chance"):
                  dc_data.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2),
                                  round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "Draw no bet"):
                  dnb.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "Total"):
                  for item in market["Items"]:
                      if(item['Name'] == "Over 2.5"):
                          over[2.5] = round(item['Price'], 2)
                      if(item['Name'] == "Under 2.5"):
                          under[2.5] = round(item['Price'], 2)
              if(market['Name'] == "GG/NG"):
                  ggng.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "First goal"):
                  fg.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "Last goal"):
                  lg.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "Odd/even"):
                  oe.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
        if(marketgroup['Name'] == '1st Half'):
          markets = marketgroup['Items']        
          for market in markets:
              if(market['Name'] == "1st half - 1x2"):
                  fh_m.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "1st half - first goal"):
                  fh_fg.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "1st half - both teams to score"):
                  fh_ggng.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "1st half - draw no bet"):
                  fh_dnb.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "1st half - odd/even"):
                  fh_oe.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
        if(marketgroup['Name'] == '2nd Half'):
          markets = marketgroup['Items']        
          for market in markets:
              if(market['Name'] == "2nd half - 1x2"):
                  shm.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][2]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "2nd half - both teams to score"):
                  sh_ggng.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
              if(market['Name'] == "2nd half - draw no bet"):
                  sh_dnb.extend((round(market['Items'][0]['Price'], 2), round(market['Items'][1]['Price'], 2)))
             
      name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
      match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under, dc=dc_data, dnb=dnb,
                    fh1x2=fh_m, ggng=ggng, fh_ggng=fh_ggng, fh_dnb=fh_dnb, fh_fg=fh_fg, fh_odd_even=fh_oe, fg=fg, ltts=lg, odd_even=oe,
                    sh1x2=shm, sh_ggng=sh_ggng, sh_dnb=sh_dnb)
      matches.append(match)

  campeon_dict = {"Name":"Campeon", "Matches": matches}
  return campeon_dict

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
  return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeSportBetBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeSportBetCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeSportBetCPBTeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeSportBetPPTeamNames(team_name):
  return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeSportBetELPTeamNames(team_name):
  return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
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
  if(team_name == 'Athletic Club'): return 'A Bilbao'
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeSportBetSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeSportBetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeSportBetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    campeonbet_dict = campeonbetEPL()
    pd.set_option('display.max_colwidth', None)
    campeonbetdF = pd.DataFrame.from_dict(campeonbet_dict)
    print(campeonbetdF)
