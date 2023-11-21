from bs4 import BeautifulSoup
import pandas as pd
from thefuzz import process
from match import Match
from db import *
import time
import network_utils as nu

headers = {
    'authority': 'www.marathonbet.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'puid=rBkp82SUuPxOxiGiAyD3Ag==; panbet.openeventnameseparately=true; panbet.openadditionalmarketsseparately=false; LIVE_TRENDS_STYLE=ARROW; panbet.oddstype=Decimal; lang=en; _gcl_au=1.1.1168786435.1687468285; MSESSION_KEY=006c8a060ee44e8a9a4ddff588afb9b6; favoriteAuthType=0; viewedNotificationItems=HOME; visitedNavBarItems=HOME; SESSION_KEY=5015a540783b4072a27c3d8053d71376; _dvs=0:lj7n1q0o:cw4IvCedUTDe3TOBD0JgluA9EuKmkD8T; _dvp=0:lj7n1q0o:JVUBkvuQwZdhwRAWtA0FHGZLIqTKb~aO; _gid=GA1.2.324362873.1687468288; _ym_uid=1687468289681914983; _ym_d=1687468289; _ym_isad=1; refererId=1643; ConsentCookie=true; amplitude_id_2bc40d65b6d44bc9ca9e8b69c152c0ae_cwmarathonbet.com=eyJkZXZpY2VJZCI6ImE1N2FjZTExLTQwZWYtNDE1Ni04NWRmLTQ3MjU3MzMyNjdlNlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY4NzQ2ODI4NTk3MCwibGFzdEV2ZW50VGltZSI6MTY4NzQ2ODU3Njk2MiwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; sportStat=5.14; _ga=GA1.2.240268660.1687468286; _ga_9QL4QPDSGN=GS1.1.1687468286.1.1.1687469020.60.0.0; MWSESSIONID=9FBE35E11AF938C753FFFCAD7651892D; MJSESSIONID=web4~16CCC14F69DAFD7D306711AE88FC19E5; JSESSIONID=web1~BB0CC495372B1DE6332F64B83B17FB29',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.marathonbet.com/en/?cppcids=all',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
headers2 = {
    'authority': 'www.marathonbet.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'puid=rBkp82SUuPxOxiGiAyD3Ag==; panbet.openeventnameseparately=true; panbet.openadditionalmarketsseparately=false; LIVE_TRENDS_STYLE=ARROW; panbet.oddstype=Decimal; lang=en; _gcl_au=1.1.1168786435.1687468285; favoriteAuthType=0; _dvp=0:lj7n1q0o:JVUBkvuQwZdhwRAWtA0FHGZLIqTKb~aO; _gid=GA1.2.324362873.1687468288; _ym_uid=1687468289681914983; _ym_d=1687468289; _ym_isad=1; refererId=1643; ConsentCookie=true; MSESSION_KEY=31d29f6e45b24ef4a06addf278b96b4b; viewedNotificationItems=HOME; visitedNavBarItems=HOME; _dvs=0:lj8rv1t0:ZxsisOH1JiJtYgd0rxgSgXvk28cPlUPO; SESSION_KEY=2a965c9c8b33492c8fda730bead9dd4a; amplitude_id_2bc40d65b6d44bc9ca9e8b69c152c0ae_cwmarathonbet.com=eyJkZXZpY2VJZCI6ImE1N2FjZTExLTQwZWYtNDE1Ni04NWRmLTQ3MjU3MzMyNjdlNlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY4NzUzNjgzOTM2MSwibGFzdEV2ZW50VGltZSI6MTY4NzUzNjk3MjExMiwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; _ga=GA1.2.240268660.1687468286; MJSESSIONID=web11~EFE0603395400371CA2C7269127799AA; JSESSIONID=web6~03955CCF46496C29776AB8E348C99236; _dc_gtm_UA-145186563-6=1; _ga_9QL4QPDSGN=GS1.1.1687536839.3.1.1687537463.59.0.0',
    'referer': 'https://www.marathonbet.com/en/?cppcids=all',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
def marathonbetALP():
    url = "https://www.marathonbet.com/en/betting/Football/Argentina/Primera+Division+-+10803"
    return marathonbetGetData(url, headers, 'ALP')
def marathonbetBSA():
    url = "https://www.marathonbet.com/en/betting/Football/Brazil/Serie+A+-+211229"
    return marathonbetGetData(url, headers, 'BSA')
def marathonbetBSB():
    url = "https://www.marathonbet.com/en/betting/Football/Brazil/Serie+B+-+386546"
    return marathonbetGetData(url, headers, 'BSB')
def marathonbetCPA():
    url = "https://www.marathonbet.com/en/betting/Football/Colombia/Primera+A+-+312055"
    return marathonbetGetData(url, headers, 'CPA')
def marathonbetPL1():
    url = "https://www.marathonbet.com/en/betting/Football/Peru/Liga+1+-+184178"
    return marathonbetGetData(url, headers, 'PL1')
def marathonbetUSD():
    url = "https://www.marathonbet.com/en/betting/Football/Uruguay/Segunda+Division+-+644712"
    return marathonbetGetData(url, headers, 'USD')
def marathonbetBPD():
    url = "https://www.marathonbet.com/en/betting/Football/Bolivia/Division+Profesional+-+339248"
    return marathonbetGetData(url, headers, 'BPD')
def marathonbetMLM():
    url = "https://www.marathonbet.com/en/betting/Football/Mexico/Primera+Division+-+223070"
    return marathonbetGetData(url, headers, 'MLM')
def marathonbetUSM():
    url = "https://www.marathonbet.com/en/betting/Football/USA/MLS+-+138152"
    return marathonbetGetData(url, headers, 'USM')

def marathonbetEPL():
    url = "https://www.marathonbet.com/en/betting/Football/England/Premier+League+-+21520"
    return marathonbetGetData(url, headers, 'EPL')
def marathonbetEFL():
    url = "https://www.marathonbet.com/en/betting/Football/England/Championship+-+22807"
    return marathonbetGetData(url, headers, 'EFL')
def marathonbetEL1():
    url = "https://www.marathonbet.com/en/betting/Football/England/League+1+-+22808"
    return marathonbetGetData(url, headers, 'EL1')
def marathonbetEL2():
    url = "https://www.marathonbet.com/en/betting/Football/England/League+2+-+22809"
    return marathonbetGetData(url, headers, 'EL2')
def marathonbetSP():
    url = 'https://www.marathonbet.com/en/betting/Football/Scotland/Premiership+-+22435'
    return marathonbetGetData(url, headers, 'SP')
def marathonbetSC():
    url = 'https://www.marathonbet.com/en/betting/Football/Scotland/Championship+-+37771'
    return marathonbetGetData(url, headers, 'SC')
def marathonbetIFD():
    url = 'https://www.marathonbet.com/en/betting/Football/Republic+of+Ireland/1st+Division+-+353449'
    return marathonbetGetData(url, headers, 'IFD')
def marathonbetIPD():
    url = 'https://www.marathonbet.com/en/betting/Football/Republic+of+Ireland/Premier+Division+-+46714'
    return marathonbetGetData(url, headers, 'IPD')
def marathonbetSPD():
    url = 'https://www.marathonbet.com/en/betting/Football/Spain/Primera+Division+-+8736'
    return marathonbetGetData(url, headers, 'SPD')
def marathonbetSSD():
    url = 'https://www.marathonbet.com/en/betting/Football/Spain/Segunda+Division+-+48300'
    return marathonbetGetData(url, headers, 'SSD')
def marathonbetFL1():
    url = 'https://www.marathonbet.com/en/betting/Football/France/Ligue+1+-+21533'
    return marathonbetGetData(url, headers, 'FL1')
def marathonbetFL2():
    url = 'https://www.marathonbet.com/en/betting/Football/France/Ligue+2+-+46785'
    return marathonbetGetData(url, headers, 'FL2')

def marathonbetGetData(url, headers, tag):
    html = nu.make_requestHTML(url, headers)
    soup = BeautifulSoup(html, 'html.parser')
    div_element = soup.find('div', attrs={"id": lambda x: x and x.startswith("category")})
    event_list = []
    urls = []
    if(div_element):
      matches = div_element.findAll('div', class_="bg coupon-row")
      if(matches):
        event_list = [match.get('data-event-path') for match in matches]
        for event in event_list:
           urls.append(f"https://www.marathonbet.com/en/betting/{event}")
        responses = nu.fetch_dataHTML(urls, headers2)
      else:
        return {"Name":"Marathon", "Matches": []}
    return marathonbetExtractData(responses, tag)

def marathonbetExtractData(responses, tag):
    matches = []
    for response in responses: 
        if(not response):
           continue
        match = response.content
        soup = BeautifulSoup(match, 'html.parser')
        title = soup.find('title').get_text()
        if(not title):
           continue
        name = title.split(' in ')[0].split(' on ')[1].split(' vs ')
        name1 = name[0]
        name2 = name[1]
        name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
        fh = []
        fg = []
        ltts = []
        ggng = []
        fh_fg = []
        fh_ggng = []
        sh_ggng = []
        odd_even = []
        fh_odd_even = []
        ov = {}
        un = {}
        odds_dc = {'0': 0, '1': 0, '2': 0}
        odds1x2 = {'0': 0, '1': 0, '2': 0}
        odds1x2_fh = {'0': 0, '1': 0, '2': 0}
        odds1x2_sh = {'0': 0, '1': 0, '2': 0}
        market_group = soup.find('div', class_="blocks-area")
        markets = market_group.findAll('div', class_="market-inline-block-table-wrapper")
        for market in markets:
            market_name = market.get('data-preference-id')
            if(market is not None and market_name is not None and 'RESULT_AND_DOUBLE_CHANCE_FOR_SIMPLE_STYLE_EVENTS' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:
                    h_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Match_Result.1" in x})
                    a_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Match_Result.3" in x})
                    d_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Match_Result.draw" in x})
                    odd_1x = row.find('span', attrs={"data-selection-key": lambda x: x and "Result.HD" in x})
                    odd_2x = row.find('span', attrs={"data-selection-key": lambda x: x and "Result.AD" in x})
                    odd_12 = row.find('span', attrs={"data-selection-key": lambda x: x and "Result.HA" in x})
                    if(h_odd): odds1x2['0'] = float(h_odd.get_text())
                    if(a_odd): odds1x2['1'] = float(a_odd.get_text())
                    if(d_odd): odds1x2['2'] = float(d_odd.get_text())
                    if(odd_1x): odds_dc['0'] = float(odd_1x.get_text())
                    if(odd_2x): odds_dc['1'] = float(odd_2x.get_text())
                    if(odd_12): odds_dc['2'] = float(odd_12.get_text())
            if(market is not None and market_name is not None and 'FIRST_HALF_RESULT_AND_DOUBLE_CHANCE' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:
                    h_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "1st_Half.RN_H" in x})
                    a_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "1st_Half.RN_A" in x})
                    d_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "1st_Half.RN_D" in x})
                    if(h_odd): odds1x2_fh['0'] = float(h_odd.get_text())
                    if(a_odd): odds1x2_fh['1'] = float(a_odd.get_text())
                    if(d_odd): odds1x2_fh['2'] = float(d_odd.get_text())
            if(market is not None and market_name is not None and market_name == 'GOALS_889339866'):
                rows = market.findAll('td', class_="price")
                for row in rows:
                    ggng_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Both_Teams_To_Score." in x})
                    fh_ggng_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Both_Teams_To_Score_-_1st_Half." in x})
                    sh_ggng_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Both_Teams_To_Score_-_2nd_Half." in x})
                    if(ggng_odd):
                        ggng.append(float(ggng_odd.get_text()))
                    if(fh_ggng_odd):
                       fh_ggng.append(float(fh_ggng_odd.get_text()))
                    if(sh_ggng_odd):
                       sh_ggng.append(float(sh_ggng_odd.get_text()))
                       
            if(market is not None and market_name is not None and 'MATCH_TOTALS_SEVERAL' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:                                                          
                    over = row.find('span', attrs={"data-selection-key": lambda x: x and "Total_Goals2.Over_2.5" in x or 'Total_Goals.Over_2.5' in x})
                    under = row.find('span', attrs={"data-selection-key": lambda x: x and "Total_Goals2.Under_2.5" in x or 'Total_Goals.Under_2.5' in x})
                    odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Total_Goals12.odd" in x})
                    even = row.find('span', attrs={"data-selection-key": lambda x: x and "Total_Goals12.even" in x})
                    if(over): ov[2.5] = float(over.get_text())
                    if(under): un[2.5] = float(under.get_text())
                    if(odd): odd_even.insert(0, float(odd.get_text()))
                    if(even): odd_even.insert(1, float(even.get_text()))
            if(market is not None and market_name is not None and 'ORDER_OF_GOALS_IN_EACH_HALVES' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:                                                          
                    fhfg_home = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_First_-_1st_Half.home" in x})
                    fhfg_away = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_First_-_1st_Half.away" in x})
                    fhfg_neither = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_First_-_1st_Half.neither" in x})
                    if(fhfg_home): fh_fg.insert(0, float(fhfg_home.get_text()))
                    if(fhfg_away): fh_fg.insert(1, float(fhfg_away.get_text()))
                    if(fhfg_neither): fh_fg.insert(2, float(fhfg_neither.get_text()))
            if(market is not None and market_name is not None and 'TOTALS_WITH_ODDEVEN1_2026104575' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:                                                          
                    odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Total_Goals_-_1st_Half" in x and ('odd' in x or 'even' in x)})
                    if(odd):
                       fh_odd_even.append(float(odd.get_text()))
            if(market is not None and market_name is not None and 'SECOND_HALF_RESULT_AND_DOUBLE_CHANCE' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:
                    h_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "2nd_Half.RN_H" in x})
                    a_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "2nd_Half.RN_A" in x})
                    d_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "2nd_Half.RN_D" in x})
                    if(h_odd): odds1x2_sh['0'] = float(h_odd.get_text())
                    if(a_odd): odds1x2_sh['1'] = float(a_odd.get_text())
                    if(d_odd): odds1x2_sh['2'] = float(d_odd.get_text())
            if(market is not None and market_name is not None and 'GOALS_AND_TIME' in market_name):
                rows = market.findAll('td', class_="price")
                for row in rows:
                    fgh_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_First.home" in x})
                    fga_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_First.away" in x})
                    fgd_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Time_Of_First_Goal.noGoals" in x})
                    lgh_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_Last.home" in x})
                    lga_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Team_To_Score_Last.away" in x})
                    lgd_odd = row.find('span', attrs={"data-selection-key": lambda x: x and "Time_Of_Last_Goal.noGoals" in x})
                    if(fgh_odd): fg.insert(0, float(fgh_odd.get_text()))
                    if(fga_odd): fg.insert(1, float(fga_odd.get_text()))
                    if(fgd_odd): fg.insert(2, float(fgd_odd.get_text()))
                    if(lgh_odd): ltts.insert(0, float(lgh_odd.get_text()))
                    if(lga_odd): ltts.insert(1, float(lga_odd.get_text()))
                    if(lgd_odd): ltts.insert(2, float(lgd_odd.get_text()))
                    
        fh = list(odds1x2_fh.values())
        sh_m = list(odds1x2_sh.values())
        dc = list(odds_dc.values())
        match = Match(name=name, home_odd=odds1x2['0'], away_odd=odds1x2['1'], draw_odd=odds1x2['2'], dc=dc, fh1x2=fh, ggng=ggng, 
                      over=ov, under=un, odd_even=odd_even, fh_fg=fh_fg, fh_odd_even=fh_odd_even, sh1x2=sh_m, fh_ggng=fh_ggng, sh_ggng=sh_ggng, fg=fg, ltts=ltts) 
        matches.append(match)
    return {"Name":"Marathon", "Matches": matches}

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeMarathonALPTeamNames,
        "BSA": normalizeMarathonBSATeamNames,
        "BSB": normalizeMarathonBSBTeamNames,
        "CPA": normalizeMarathonCPATeamNames,
        "PL1": normalizeMarathonPL1TeamNames,
        "USD": normalizeMarathonUSDTeamNames,
        "BPD": normalizeMarathonBPDTeamNames,
        "MLM": normalizeMarathonMLMTeamNames,
        "USM": normalizeMarathonUSMTeamNames,
        'EPL': normalizeMarathonEPLTeamNames,
        'EFL': normalizeMarathonEFLTeamNames,
        'EL1': normalizeMarathonEL1TeamNames,
        'EL2': normalizeMarathonEL2TeamNames,
        'SP': normalizeMarathonSPTeamNames,
        'SC': normalizeMarathonSCTeamNames,
        'IFD': normalizeMarathonIFDTeamNames,
        'IPD': normalizeMarathonIPDTeamNames,
        'SPD': normalizeMarathonSPDTeamNames,
        'SSD': normalizeMarathonSSDTeamNames,
        'FL1': normalizeMarathonFL1TeamNames,
        'FL2': normalizeMarathonFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeMarathonALPTeamNames(team_name):
  return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeMarathonBSATeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeMarathonBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeMarathonCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeMarathonPL1TeamNames(team_name):
  return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeMarathonUSDTeamNames(team_name):
  return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeMarathonBPDTeamNames(team_name):
  return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeMarathonMLMTeamNames(team_name):
  if(team_name == 'UNAM'): return 'Universidad Nacional'
  return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeMarathonUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeMarathonEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeMarathonEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeMarathonEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeMarathonEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeMarathonSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeMarathonSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeMarathonIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeMarathonIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeMarathonSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeMarathonSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeMarathonFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeMarathonFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    final = marathonbetEPL()
    pd.set_option('display.max_colwidth', None)
    dF = pd.DataFrame.from_dict(final)
    print(dF)
