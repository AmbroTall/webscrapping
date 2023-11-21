from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth
from match import Match
from thefuzz import process
from bs4 import BeautifulSoup
import pandas as pd
import time

from db import *

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument("start-maximized")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument( '--disable-blink-features=AutomationControlled' )
option.add_argument("--no-sandbox");
option.add_argument("--disable-dev-shm-usage");
option.add_argument("--disable-renderer-backgrounding");
option.add_argument("--disable-background-timer-throttling");
option.add_argument("--disable-backgrounding-occluded-windows");
option.add_argument("--disable-client-side-phishing-detection");
option.add_argument("--disable-crash-reporter");
option.add_argument("--disable-oopr-debug-crash-dump");
option.add_argument("--no-crash-upload");
option.add_argument("--disable-gpu");
option.add_argument("--disable-extensions");
option.add_argument("--disable-low-res-tiling");
option.add_argument("--log-level=3");
option.add_argument("--silent");

ser = Service(r"C:\Program Files (x86)\chromedriver.exe")
PATH = "C:\Program Files (x86)\chromedriver.exe"

def sbobetALP():
   url = 'https://www.sbobet.com/euro/football/argentina-liga-profesional'
   return sbobetGetData(url, "ALP")
def sbobetBSA():
   url = 'https://www.sbobet.com/en/euro/football/brazil-serie-a'
   return sbobetGetData(url, "BSA")
def sbobetBSB():
    url = 'https://www.sbobet.com/euro/football/brazil-serie-b'
    return sbobetGetData(url, "BSB")
def sbobetCPA():
    url = 'https://www.sbobet.com/euro/football/colombia'
    return sbobetGetData(url, "CPA")
def sbobetELP():
   url = "https://www.sbobet.com/en/euro/football/ecuador"
   return sbobetGetData(url, "ELP")
def sbobetUSM():
   url = "https://www.sbobet.com/euro/football/usa"
   return sbobetGetData(url, "USM")

def sbobetEPL():
   url = "https://www.sbobet.com/euro/football/english-premier-league"
   return sbobetGetData(url, "EPL")
def sbobetEFL():
   url = "https://www.sbobet.com/euro/football/english-championship"
   return sbobetGetData(url, "EFL")
def sbobetEL1():
   url = "https://www.sbobet.com/euro/football/english-league-one"
   return sbobetGetData(url, "EL1")
def sbobetEL2():
   url = "https://www.sbobet.com/euro/football/english-league-two"
   return sbobetGetData(url, "EL2")
def sbobetSP():
   url = "https://www.sbobet.com/euro/football/scotland-premiership"
   return sbobetGetData(url, "SP")
#def sbobetSC():
   #url = "https://www.sbobet.com/euro/football/scotland-championship"
   #return sbobetGetData(url, "SC")
def sbobetIFD():
   url = "https://www.sbobet.com/euro/football/ireland-1st-div"
   return sbobetGetData(url, "IFD")
def sbobetIPD():
   url = "https://www.sbobet.com/euro/football/ireland-premier-division"
   return sbobetGetData(url, "IPD")
def sbobetSPD():
   url = "https://www.sbobet.com/euro/football/spain-la-liga"
   return sbobetGetData(url, "SPD")
def sbobetSSD():
   url = "https://www.sbobet.com/euro/football/spain-la-liga-2"
   return sbobetGetData(url, "SSD")
def sbobetFL1():
   url = "https://www.sbobet.com/euro/football/france-ligue-1"
   return sbobetGetData(url, "FL1")
def sbobetFL2():
   url = "https://www.sbobet.com/euro/football/france-ligue-2"
   return sbobetGetData(url, "FL2")

def sbobetGetData(url, tag):
   driver = webdriver.Chrome(service=ser, options=option)
   try:
      driver.get(url)
      element = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, 'bu:od:go:mt:4')))
      element.click()
      time.sleep(2)
      html = driver.page_source
      today_dict = sbobetExtractData(html, tag)
      current_selected_day = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "Bd")]/table/tbody/tr/td[contains(@class, "Sel")]/a[1]')))
      current_day = current_selected_day.get_attribute("id")[-1]
      if(current_day != 7):
         xpath = f'//div[contains(@class, "Bd")]/table/tbody/tr/td[{int(current_day)+1}]/a[1]'
         next_day_url = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
      driver.get(next_day_url.get_attribute("href"))
      element = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, 'bu:od:go:mt:4')))
      element.click()
      time.sleep(2)
      html = driver.page_source
      nextday_dict = sbobetExtractData(html, tag)
      joined_dict = {"Name": "Sbobet", "Matches": today_dict["Matches"] + nextday_dict["Matches"]}
   except TimeoutException:
      print("No matches next day. Continuing with the rest of the code.")
      return today_dict
   finally:
      driver.quit()
   return joined_dict#today_dict#joined_dict

def sbobetExtractData(html, tag):                                                            
    matches = []
    moneylines = []
    fh_moneylines = []
    oddevens = []
    fgs = []
    lgs = []
    match_name = ""
    soup = BeautifulSoup(html, 'html.parser')
    markets = soup.find_all('div', class_="MarketT Open")
    for market in markets:
       market_name = market.find('span').text
       if(market_name == "1X2"):
          names = market.find_all('span', class_="OddsL")
          odds = market.find_all('span', class_="OddsR")
          if(odds):
            for i in range(0, len(names), 3):
               name = f"{names[i].text} - {names[i+2].text}"
               h_odd = float(odds[i].text)
               a_odd = float(odds[i+2].text)
               d_odd = float(odds[i+1].text)
               moneyline = {"name":name, "ho":h_odd, "ao":a_odd, "do":d_odd}
               moneylines.append(moneyline)
       if(market_name == "First Half 1X2"):
          names = market.find_all('span', class_="OddsL")
          odds = market.find_all('span', class_="OddsR")
          if(odds):
            for i in range(0, len(names), 3):
               name = f"{names[i].text} - {names[i+2].text}"
               fh_m = [float(odds[i].text), float(odds[i+2].text), float(odds[i+1].text)]
               fh_moneyline = {"name":name, "fh_m":fh_m}
               fh_moneylines.append(fh_moneyline)
       if(market_name == "Odd Even"):
          names = market.find_all('span', class_="EventName")
          odds = market.find_all('span', class_="OddsR")
          if(odds):
            for i, j in zip(range(len(names)), range(0, len(odds), 2)):
               name = f"{names[i].text}"
               oe = [float(odds[j].text), float(odds[j+1].text)]
               oddeven = {"name":name, "oe":oe}
               oddevens.append(oddeven)
       if(market_name == "First Goal Last Goal"):
          names = market.find_all('span', class_="OddsL")
          odds = market.find_all('span', class_="OddsR")
          if(odds):
            for i in range(0, len(names), 5):
               fg = [float(odds[i].text), float(odds[i+3].text), float(odds[i+2].text)]
               ltts = [float(odds[i+1].text), float(odds[i+4].text), float(odds[i+2].text)]
               fgs.append({'name':names[i], 'fg':fg})
               lgs.append({'name':names[i], 'lg':ltts})
    
    number_of_matches = len(moneylines)
    for i in range(0, number_of_matches):
        name = moneylines[i]['name'].split(' - ')
        match_name = f"{normalizeName(tag, name[0])} - {normalizeName(tag, name[1])}"

        fg_value = fgs[i]['fg'] if i < len(fgs) else []  # Check if i is within the bounds of fgs list
        lg_value = lgs[i]['lg'] if i < len(lgs) else []
        odd_even_value = oddevens[i]['oe'] if i < len(oddevens) else []
        fh1x2_value = fh_moneylines[i]['fh_m'] if i < len(fh_moneylines) else []

        match = Match(name=match_name, home_odd=moneylines[i]['ho'], away_odd=moneylines[i]['ao'], draw_odd=moneylines[i]['do'],
                      fh1x2=fh1x2_value, odd_even=odd_even_value, fg=fg_value, ltts=lg_value)
        matches.append(match)
    sbob_dict = {"Name":"Sbobet", "Matches": matches}
    return sbob_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeSbobetALPTeamNames,
        "BSA": normalizeSbobetBSATeamNames,
        "BSB": normalizeSbobetBSBTeamNames,
        "CPA": normalizeSbobetCPATeamNames,
        "ELP": normalizeSbobetELPTeamNames,
        "USM": normalizeSbobetUSMTeamNames,
        'EPL': normalizeSbobetEPLTeamNames,
        'EFL': normalizeSbobetEFLTeamNames,
        'EL1': normalizeSbobetEL1TeamNames,
        'EL2': normalizeSbobetEL2TeamNames,
        'SP': normalizeSbobetSPTeamNames,
        'SC': normalizeSbobetSCTeamNames,
        'IFD': normalizeSbobetIFDTeamNames,
        'IPD': normalizeSbobetIPDTeamNames,
        'SPD': normalizeSbobetSPDTeamNames,
        'SSD': normalizeSbobetSSDTeamNames,
        'FL1': normalizeSbobetFL1TeamNames,
        'FL2': normalizeSbobetFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeSbobetALPTeamNames(team_name):
  return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeSbobetBSATeamNames(team_name):
  if("Atletico Mineiro" == team_name):
      return "Atletico MG"
  else:
      return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeSbobetBSBTeamNames(team_name):
  return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeSbobetCPATeamNames(team_name):
  return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeSbobetUSMTeamNames(team_name):
  return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeSbobetELPTeamNames(team_name):
  if(team_name == "El Nacional Quito"): return "El Nacional"
  else:
      correct_name = process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
  return correct_name
def normalizeSbobetEPLTeamNames(team_name):
  return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeSbobetEFLTeamNames(team_name):
  return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeSbobetEL1TeamNames(team_name):
  return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeSbobetEL2TeamNames(team_name):
  return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeSbobetSPTeamNames(team_name):
  return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeSbobetSCTeamNames(team_name):
  return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeSbobetIFDTeamNames(team_name):
  return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeSbobetIPDTeamNames(team_name):
  return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeSbobetSPDTeamNames(team_name):
  return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeSbobetSSDTeamNames(team_name):
  return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeSbobetFL1TeamNames(team_name):
  return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeSbobetFL2TeamNames(team_name):
  return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    sbobet_dict = sbobetSSD()
    pd.set_option('display.max_colwidth', None)
    sbobetdF = pd.DataFrame.from_dict(sbobet_dict)
    print(sbobetdF)
