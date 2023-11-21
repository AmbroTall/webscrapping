from bs4 import BeautifulSoup
import pandas as pd
from thefuzz import process
from match import Match
from db import *
import network_utils as nu
import utils as u

headers = {
    'authority': 'lines.bookmaker.eu',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'affid=INTERNET; affidSource=DefaultWebConfig; _ga=GA1.1.1106753792.1686246053; LPVID=EwMmIzYjhhZWEzZTEwMTE3; PHPSESSID=93b3d09a012fd19d3b0b72b106fc4005; _ga_LSDLG6K4DN=GS1.1.1687209484.7.1.1687209491.53.0.0',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://lines.bookmaker.eu/en/sports/soccer/south-america/',
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
def bookmakereuALP():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/argentina-primera-division/"
    title = 'Argentina Primera Division Live Betting Odds'
    return bookmakerGetData(url, title, "ALP")
def bookmakereuBSA():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/brazil-serie-a/"
    title = 'Brazil Serie A Live Betting Odds'
    return bookmakerGetData(url, title, "BSA")
def bookmakereuBSB():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/brazil-serie-b/"
    title = 'Brazil Serie B Live Betting Odds'
    return bookmakerGetData(url, title, "BSB")
def bookmakereuCPA():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/colombia-primera-a-apertura/"
    title = 'Colombia Primera A Apertura Live Betting Odds'
    return bookmakerGetData(url, title, "CPA")
def bookmakereuCPB():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/colombia-primera-b/"
    title = 'Colombia Primera B Live Betting Odds'
    return bookmakerGetData(url, title, 'CPB')
def bookmakereuELP():
    url = "https://lines.bookmaker.eu/en/sports/soccer/south-america/ecuador-liga-serie-a/"
    title = 'Ecuador Liga Serie A Live Betting Odds'
    return bookmakerGetData(url, title, "ELP")
def bookmakereuPL1():
    url = 'https://lines.bookmaker.eu/en/sports/soccer/south-america/peru-primera-division/'
    title = 'Peru Primera Division Live Betting Odds'
    return bookmakerExtractData(url, title, 'PL1')
def bookmakereuMLM():
    url = 'https://lines.bookmaker.eu/en/sports/soccer/north-america/mexico-liga-mx-apertura/'
    title = 'Mexico Liga MX Apertura Live Betting Odds'
    return bookmakerGetData(url, title, 'MLM')
def bookmakereuUSM():
    url = "https://lines.bookmaker.eu/en/sports/soccer/north-america/usa-mls/"
    title = 'USA MLS Live Betting Odds'
    return bookmakerGetData(url, title, "USM")

def bookmakereuEFL():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/england-championship/"
    title = 'England Championship Live Betting Odds'
    return bookmakerGetData(url, title, "EFL")
def bookmakereuEL1():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/england-league-1/"
    title = 'England League 1 Live Betting Odds'
    return bookmakerGetData(url, title, "EL1")
def bookmakereuEL2():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/england-league-2/"
    title = 'England League 2 Live Betting Odds'
    return bookmakerGetData(url, title, "EL2")
def bookmakereuSP():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/scotland-premier-league/"
    title = 'Scotland Premier League Live Betting Odds'
    return bookmakerGetData(url, title, "SP")
def bookmakereuSC():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/scotland-championship/"
    title = 'Scotland Championship Live Betting Odds'
    return bookmakerGetData(url, title, "SC")
def bookmakereuIFD():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/ireland-first-division/"
    title = 'Ireland First Division Live Betting Odds'
    return bookmakerGetData(url, title, "IFD")
def bookmakereuIPD():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/ireland-eircom-league/"
    title = 'Ireland Eircom League Live Betting Odds'
    return bookmakerGetData(url, title, "IPD")
def bookmakereuSPD():
    url = "https://lines.bookmaker.eu/en/sports/soccer/top-leagues/spain-la-liga/"
    title = 'Spain LA Liga Live Betting Odds'
    return bookmakerGetData(url, title, "SPD")
def bookmakereuFL1():
    url = "https://lines.bookmaker.eu/en/sports/soccer/top-leagues/france-ligue-1/"
    title = 'France Ligue 1 Live Betting Odds'
    return bookmakerGetData(url, title, "FL1")
def bookmakereuFL2():
    url = "https://lines.bookmaker.eu/en/sports/soccer/europe/france-ligue-2/"
    title = 'France Ligue 2 Live Betting Odds'
    return bookmakerGetData(url, title, "FL2")

def bookmakerGetData(url, title, tag):
    html = nu.make_requestHTML(url, headers)
    bookmaker_dict = bookmakerExtractData(html, title, tag)
    return bookmaker_dict

def bookmakerExtractData(html, title, tag):
    table = []
    if(html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', title=title)
    matches = []
    if table:
        # Find all the rows in the table (excluding the header row)
        rows = table.find_all('tr')[1:]
        i = 1
        name = ""
        name1 = ""
        name2 = ""
        matches = []
        for row in rows:
            a_team = f"vTeam_{i}"
            h_team = f"hTeam_{i}"
            if row.get('id') == a_team:
                name2 = row.get('title').split(" betting ")[0].strip()
            if row.get('id') == h_team:
                name1 = row.get('title').split(" betting ")[0].strip()
                name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
                i = i + 1
            td_elements = row.find_all('td')
            for td in td_elements:
                if ('title' in td.attrs and f'{name1} moneyline' in td['title']):
                    h_odd = u.americanToDecimalOdds(int(td.find('a').text))
                if('title' in td.attrs and f'{name2} moneyline' in td['title']):
                    a_odd = u.americanToDecimalOdds(int(td.find('a').text))
                if ('title' in td.attrs and 'Draw line' in td['title']):
                    d_odd = u.americanToDecimalOdds(int(td.find('a').text))
                    match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd)
                    matches.append(match)

    if(len(matches) <= 1):
        return {"Name":"Bookmaker.eu", "Matches": matches}
    #result = {"Name":"Bookmaker.eu", "Matches": matches[:len(matches)//2]}
    result = {"Name":"Bookmaker.eu", "Matches": matches}
    return result

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeBookmALPTeamNames,
        "BSA": normalizeBookmBSATeamNames,
        "BSB": normalizeBookmBSBTeamNames,
        "CPA": normalizeBookmCPATeamNames,
        "CPB": normalizeBookmCPBTeamNames,
        "ELP": normalizeBookmELPTeamNames,
        "PL1": normalizeBookmPL1TeamNames,
        "MLM": normalizeBookmMLMTeamNames,
        "USM": normalizeBookmUSMTeamNames,
        'EFL': normalizeBookmEFLTeamNames,
        'EL1': normalizeBookmEL1TeamNames,
        'EL2': normalizeBookmEL2TeamNames,
        'SP': normalizeBookmSPTeamNames,
        'SC': normalizeBookmSCTeamNames,
        'IFD': normalizeBookmIFDTeamNames,
        'IPD': normalizeBookmIPDTeamNames,
        'SPD': normalizeBookmSPDTeamNames,
        'FL1': normalizeBookmFL1TeamNames,
        'FL2': normalizeBookmFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeBookmALPTeamNames(team_name):
    return process.extract(team_name, Liga_Profesional, limit=1)[0][0]
def normalizeBookmBSATeamNames(team_name):
    if(team_name == "CA Paranaense PR"):
        return "Atletico PR"
    if(team_name == "Atletico Mineiro MG"):
        return "Atletico MG"
    return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeBookmBSBTeamNames(team_name):
    if(team_name == 'AC Goianiense GO'):
        return 'Atletico-GO'
    return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeBookmCPATeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeBookmCPBTeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeBookmELPTeamNames(team_name):
    return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeBookmPL1TeamNames(team_name):
    return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeBookmMLMTeamNames(team_name):
    if(team_name == 'Pumas UNAM'):
        return 'Universidad Nacional'
    return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeBookmUSMTeamNames(team_name):
    if(team_name == "Saint Louis City SC"):
        return "St. Louis"
    return process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
def normalizeBookmEFLTeamNames(team_name):
    return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeBookmEL1TeamNames(team_name):
    return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeBookmEL2TeamNames(team_name):
    return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeBookmSPTeamNames(team_name):
    return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeBookmSCTeamNames(team_name):
    return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeBookmIFDTeamNames(team_name):
    return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeBookmIPDTeamNames(team_name):
    return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeBookmSPDTeamNames(team_name):
    return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeBookmFL1TeamNames(team_name):
    return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeBookmFL2TeamNames(team_name):
    return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    final = bookmakereuEL1()
    pd.set_option('display.max_colwidth', None)
    dF = pd.DataFrame.from_dict(final)
    print(dF)
