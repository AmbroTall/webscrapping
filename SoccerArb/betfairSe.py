from playwright.async_api import async_playwright, TimeoutError
import asyncio
from match import Match
from itertools import zip_longest
from thefuzz import process
import pandas as pd
import utils as u

from db import *

def betfairALP():
   url = 'https://www.betfair.com/sport/football/argentinian-primera-division/67387'
   return betfairGetData(url, "ALP", 'argentinian-primera-division', '67387')
def betfairBSA():
   url = "https://www.betfair.com/sport/football/brazilian-serie-a/13"
   return betfairGetData(url, "BSA", 'brazilian-serie-a', '13')
def betfairBSB():
   url = "https://www.betfair.com/sport/football/brazilian-serie-b/321319"
   return betfairGetData(url, "BSB", 'brazilian-serie-b', '321319')
def betfairCPA():
   url = "https://www.betfair.com/sport/football/colombian-primera-a/844197"
   return betfairGetData(url, "CPA", 'colombian-primera-a', '844197')
def betfairCPB():
   url = "https://www.betfair.com/sport/football/colombian-primera-b/856134"
   return betfairGetData(url, "CPB", 'colombian-primera-b', '856134')
def betfairELP():
   url = "https://www.betfair.com/sport/football/ecuadorian-serie-a/803690"
   return betfairGetData(url, "ELP", 'ecuadorian-serie-a', '803690')
def betfairPL1():
   url = "https://www.betfair.com/sport/football/peruvian-primera-division/8594603"
   return betfairGetData(url, "PL1", 'peruvian-primera-division', '8594603')
def betfairMLM():
   url = "https://www.betfair.com/sport/football/mexican-liga-mx/5627174"
   return betfairGetData(url, "MLM", 'mexican-liga-mx', '5627174')
def betfairUSM():
   url = "https://www.betfair.com/sport/football/us-major-league-football/141"
   return betfairGetData(url, "USM", 'us-major-league-football', '141')

async def betfairEPL():
   url = "https://www.betfair.com/sport/football/english-premier-league/10932509"
   return await betfairGetData(url, "EPL", 'english-premier-league', '10932509')
def betfairEFL():
   url = "https://www.betfair.com/sport/football/english-championship/7129730"
   return betfairGetData(url, "EFL", 'english-championship', '7129730')
def betfairEL1():
   url = "https://www.betfair.com/sport/football/english-league-1/35"
   return betfairGetData(url, "EL1", 'english-league-1', '35')
def betfairEL2():
   url = "https://www.betfair.com/sport/football/english-league-2/37"
   return betfairGetData(url, "EL2", 'english-league-2', '37')
def betfairSP():
   url = "https://www.betfair.com/sport/football/scottish-premiership/105"
   return betfairGetData(url, "SP", 'scottish-premiership', '105')
def betfairSC():
   url = "https://www.betfair.com/sport/football/scottish-championship/107"
   return betfairGetData(url, "SC", 'scottish-championship', '107')
def betfairIFD():
   url = "https://www.betfair.com/sport/football/irish-division-1/12005855"
   return betfairGetData(url, "IFD", 'irish-division-1', '12005855')
def betfairIPD():
   url = "https://www.betfair.com/sport/football/irish-premier-division/12203971"
   return betfairGetData(url, "IPD", 'irish-premier-division', '12203971')
def betfairSPD():
   url = "https://www.betfair.com/sport/football/spanish-la-liga/117"
   return betfairGetData(url, "SPD", 'spanish-la-liga', '117')
def betfairSSD():
   url = "https://www.betfair.com/sport/football/spanish-segunda-division/12204313"
   return betfairGetData(url, "SSD", 'spanish-segunda-division', '12204313')
def betfairFL1():
   url = "https://www.betfair.com/sport/football/french-ligue-1/55"
   return betfairGetData(url, "FL1", 'french-ligue-1', '55')
def betfairFL2():
   url = "https://www.betfair.com/sport/football/french-ligue-2/57"
   return betfairGetData(url, "FL2", 'french-ligue-2', '57')

proxy_url = 'http://geo.iproyal.com:12321'

async def betfairGetData(url, tag, league, id):
   try:
      async with async_playwright() as p:
        final = {"Name":"Betfair", "Matches": []}

        browser = await p.chromium.launch(proxy={
            "server": proxy_url,
            "username": 'phscrapingtest',
            "password": "strongzerocola_country-gb"
        })
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(url)
        matches = await betfairExtractData(tag, page)

        ggng_url = f"https://www.betfair.com/sport/football/{league}/{id}?marketType=BOTH_TEAMS_TO_SCORE"
        await page.goto(ggng_url)
        ggng_matches = await betfairExtractGGNG(tag, page)

        final = combineMatchesData(matches, ggng_matches)

        await page.close()
        await context.close()
        await browser.close()
        return final
   except TimeoutError:
      print("Betfair is not responding")
      return {"Name":"Betfair", "Matches": []}

async def betfairExtractData(tag, page):
    home_teams = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[3]/div[1]/a/div[1]/span[1]')
    away_teams = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[3]/div[1]/a/div[1]/span[2]')
    home_odds = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[2]/div[2]/ul/li[1]/a/span')
    away_odds = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[2]/div[2]/ul/li[3]/a/span')
    draw_odds = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[2]/div[2]/ul/li[2]/a/span')
    over_odds = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[1]/div[2]/ul/li[1]/a[1]/span[1]')
    under_odds = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[1]/div[2]/ul/li[2]/a[1]/span[1]')
    matches = []
    # Process and store the data as needed
    for ht, at, h_odd, a_odd, d_odd, ov, un in zip(home_teams, away_teams, home_odds, away_odds, draw_odds, over_odds, under_odds):
        home_team_name = await ht.evaluate('(element) => element.textContent')
        away_team_name = await at.evaluate('(element) => element.textContent')
        name = f"{normalizeName(tag, home_team_name.strip())} - {normalizeName(tag, away_team_name.strip())}"

        homeodd = await h_odd.evaluate('(element) => element.textContent')
        awayodd = await a_odd.evaluate('(element) => element.textContent')
        drawodd = await d_odd.evaluate('(element) => element.textContent')

        h_odd = u.fractionalToDecimal(homeodd.replace('\n', ''))
        a_odd = u.fractionalToDecimal(awayodd.replace('\n', ''))
        d_odd = u.fractionalToDecimal(drawodd.replace('\n', ''))

        overodd = await ov.evaluate('(element) => element.textContent')
        underodd = await un.evaluate('(element) => element.textContent')
        ovr = u.fractionalToDecimal(overodd.replace('\n', ''))
        und = u.fractionalToDecimal(underodd.replace('\n', ''))
        over = {2.5: ovr}
        under = {2.5: und}
        home_odd = h_odd
        away_odd = a_odd
        draw_odd = d_odd
        match = Match(name=name, home_odd=home_odd, away_odd=away_odd, draw_odd=draw_odd, over=over, under=under)
        matches.append(match)
    return matches
async def betfairExtractGGNG(tag, page):
    home_teams = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[3]/div[1]/a/div[1]/span[1]')
    away_teams = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[3]/div[1]/a/div[1]/span[2]')
    ggs = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[1]/div[2]/ul/li[1]/a[1]/span[1]')
    ngs = await page.query_selector_all('//li[contains(@class, "com-coupon-line-new-layout betbutton-layout")]/div[contains(@class, "event-information ui-event")]/div[2]/div[1]/div[2]/ul/li[2]/a[1]/span[1]')
    matches = []
    for ht, at, gg, ng in zip(home_teams, away_teams, ggs, ngs):
        ggng = []
        home_team_name = await ht.evaluate('(element) => element.textContent')
        away_team_name = await at.evaluate('(element) => element.textContent')
        name = f"{normalizeName(tag, home_team_name.strip())} - {normalizeName(tag, away_team_name.strip())}"
        gg_yes = await gg.evaluate('(element) => element.textContent')
        gg_no = await ng.evaluate('(element) => element.textContent')
        ggng.extend((u.fractionalToDecimal(gg_yes.replace('\n', '')), 
                     u.fractionalToDecimal(gg_no.replace('\n', ''))))
        match = Match(name=name, home_odd=0, away_odd=0, draw_odd=0, ggng=ggng)
        matches.append(match)
    
    return matches

def combineMatchesData(matches, ggng):
   for match, ggng_match in zip_longest(matches, ggng):
       try:
          if(match.name == ggng_match.name):
             match.ggng = ggng_match.ggng
       except:
           pass
   betfair_dict = {"Name":"Betfair", "Matches": matches}
   return betfair_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeSbobetALPTeamNames,
        "BSA": normalizeBetfairBSATeamNames,
        "BSB": normalizeBetfairBSBTeamNames,
        "CPA": normalizeBetfairCPATeamNames,
        "CPB": normalizeBetfairCPBTeamNames,
        "ELP": normalizeBetfairELPTeamNames,
        "PL1": normalizeBetfairPL1TeamNames,
        "MLM": normalizeBetfairMLMTeamNames,
        "USM": normalizeBetfairUSMTeamNames,
        'EPL': normalizeBetfairEPLTeamNames,
        'EFL': normalizeBetfairEFLTeamNames,
        'EL1': normalizeBetfairEL1TeamNames,
        'EL2': normalizeBetfairEL2TeamNames,
        'SP': normalizeBetfairSPTeamNames,
        'SC': normalizeBetfairSCTeamNames,
        'IFD': normalizeBetfairIFDTeamNames,
        'IPD': normalizeBetfairIPDTeamNames,
        'SPD': normalizeBetfairSPDTeamNames,
        'SSD': normalizeBetfairSSDTeamNames,
        'FL1': normalizeBetfairFL1TeamNames,
        'FL2': normalizeBetfairFL1TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeSbobetALPTeamNames(team_name):
    return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeBetfairBSATeamNames(team_name):
    return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeBetfairBSBTeamNames(team_name):
    return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeBetfairCPATeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeBetfairCPBTeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeBetfairELPTeamNames(team_name):
    return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeBetfairPL1TeamNames(team_name):
    return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeBetfairMLMTeamNames(team_name):
    if(team_name == 'Pumas UNAM'):
       return 'Universidad Nacional'
    return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]   
def normalizeBetfairUSMTeamNames(team_name):
    return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeBetfairEPLTeamNames(team_name):
    return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeBetfairEFLTeamNames(team_name):
    return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeBetfairEL1TeamNames(team_name):
    return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeBetfairEL2TeamNames(team_name):
    return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeBetfairSPTeamNames(team_name):
    return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeBetfairSCTeamNames(team_name):
    return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeBetfairIFDTeamNames(team_name):
    return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeBetfairIPDTeamNames(team_name):
    if(team_name == 'UCD'): return 'Uni College Dublin'
    return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeBetfairSPDTeamNames(team_name):
    return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeBetfairSSDTeamNames(team_name):
    return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeBetfairFL1TeamNames(team_name):
    return process.extract(team_name, France_Ligue2, limit=1)[0][0]

async def main():
    final = await betfairEL1()
    pd.set_option('display.max_colwidth', None)
    dF = pd.DataFrame.from_dict(final)
    print(dF)

if __name__ == '__main__':
    asyncio.run(main())