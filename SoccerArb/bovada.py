import pandas as pd
from match import Match
from thefuzz import process, fuzz
from db import *
import network_utils as nu
import time

headers = {
    'authority': 'www.bovada.lv',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,mk;q=0.8,sr;q=0.7',
    'cache-control': 'no-cache',
    'referer': 'https://www.bovada.lv/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
def bovadaUSM():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/north-america/united-states/mls?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "USM")
def bovadaMLM():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/brazil/brasileirao-serie-a?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "MLM")
def bovadaBPD():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/bolivia/division-profesional?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "BPD")
def bovadaUSD():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/uruguay/segunda-division?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "USD")
def bovadaPL1():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/peru/primera-division?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "PL1")
def bovadaELP():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/ecuador/ligapro-primera-a?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "ELP")
def bovadaPP():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/paraguay/primera-division-apertura?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "PP")
def bovadaCPB():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/colombia/primera-b?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "CPB")
def bovadaCPA():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/colombia/primera-a-apertura?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "CPA")
def bovadaBSB():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/brazil/brasileiro-serie-b?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "BSB")
def bovadaBSA():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/brazil/brasileirao-serie-a?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "BSA")
def bovadaALP():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/south-america/argentina?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "ALP")

def bovadaEPL():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/england/premier-league?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "EPL")
def bovadaEFL():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/england/championship?marketFilterId=def&preMatchOnly=true&eventsLimit=5000&lang=en"
    return bovadaGetData(url, "EFL")
def bovadaEL1():
    url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/england/league-one?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en"
    return bovadaGetData(url, "EL1")
def bovadaEL2():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/england/league-two?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "EL2")
def bovadaSP():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/scotland/premiership?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "SP")
def bovadaSC():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/scotland/championship?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "SC")
def bovadaIFD():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/ireland/loi-1st-division?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "IFD")
def bovadaIPD():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/ireland/loi-premier-division?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "IPD")
def bovadaSPD():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/spain/la-liga?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "SPD")
def bovadaSSD():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/spain/laliga-2?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "SSD")
def bovadaFL1():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/france/ligue-1?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "FL1")
def bovadaFL2():
    url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/soccer/europe/france/ligue-2?marketFilterId=def&preMatchOnly=true&eventsLimit=9000&lang=en'
    return bovadaGetData(url, "FL2")

def bovadaGetData(url, tag):
    urls = []
    matchdata = nu.make_request(url, headers)
    bovada_dict = {"Name":"Bovada", "Matches": []}
    if(matchdata and matchdata[0] and 'events' in matchdata[0]):
        event_list = [event['link'] for event in matchdata[0]['events']]
        for event in event_list:
            urls.append(f"https://www.bovada.lv/services/sports/event/coupon/events/A/description{event}")
        responses = nu.fetch_data(urls, headers)
        bovada_dict = bovadaExtractData(tag, responses)
    return bovada_dict

def bovadaExtractData(tag, responses):
    matches = []
    for response in responses:
        if(not response):
            continue
        match_data = response.json()
        name = match_data[0]['events'][0]["description"]
        name1 = name.split(" vs ")[0]
        name2 = name.split(" vs ")[1]
        dc_data = []
        fh1_data = []
        dnb = []
        ggng = []
        over = {}
        under = {}
        for group in match_data[0]['events'][0]['displayGroups']:
            for market in group['markets']:
                if(market['description'] == "3-Way Moneyline" and market['period']['description'] == "Regulation Time" and len(market['outcomes']) == 3):
                    h_odd = round(float(market['outcomes'][0]['price']['decimal']), 2)
                    a_odd = round(float(market['outcomes'][1]['price']['decimal']), 2)
                    d_odd = round(float(market['outcomes'][2]['price']['decimal']), 2)
                if(market['description'] == "Total Goals O/U" and market['period']['description'] == "Regulation Time"):
                    for outcome in market['outcomes']:
                        if(outcome['description'] == 'Over' and outcome['price']['handicap'] == '2.5' and not 'handicap2' in outcome['price']):
                            over[2.5] = round(float(outcome['price']['decimal']), 2)
                        if(outcome['description'] == 'Under' and outcome['price']['handicap'] == '2.5' and not 'handicap2' in outcome['price']):
                            under[2.5] = round(float(outcome['price']['decimal']), 2)
                if(market['description'] == "3-Way Moneyline" and market['period']['description'] == "First Half" and len(market['outcomes']) == 3):
                    fh1_data.extend((round(float(market['outcomes'][0]['price']['decimal']), 2),
                                    round(float(market['outcomes'][1]['price']['decimal']), 2), 
                                    round(float(market['outcomes'][2]['price']['decimal']), 2)))
                if(market['description'] == "Double Chance" and market['period']['description'] == "Regulation Time" and len(market['outcomes']) == 3):
                    dc_data.extend((round(float(market['outcomes'][0]['price']['decimal']), 2), 
                                    round(float(market['outcomes'][1]['price']['decimal']), 2), 
                                    round(float(market['outcomes'][2]['price']['decimal']), 2)))
                if(market['description'] == "Both Teams To Score" and market['period']['description'] == "Regulation Time" and len(market['outcomes']) == 2):
                        ggng.extend((round(float(market['outcomes'][0]['price']['decimal']),2), 
                                    round(float(market['outcomes'][1]['price']['decimal']),2)))
                if(market['description'] == "Draw No Bet" and market['period']['description'] == "Regulation Time" and len(market['outcomes']) == 2):
                    dnb.extend((round(float(market['outcomes'][0]['price']['decimal']), 2), 
                                round(float(market['outcomes'][1]['price']['decimal']), 2)))
        name = f"{normalizeName(tag, name1)} - {normalizeName(tag, name2)}"
        match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd, over=over, under=under, dc=dc_data, dnb=dnb, fh1x2=fh1_data, ggng=ggng)
        matches.append(match)
    bovada_dict = {"Name":"Bovada", "Matches": matches}
    return  bovada_dict

def normalizeName(tag, team_name):
    normalization_functions = {
        "BSA": normalizeBovadaBSATeamNames,
        "ALP": normalizeBovadaALPTeamNames,
        "BSB": normalizeBovadaBSBTeamNames,
        "CPA": normalizeBovadaCPATeamNames,
        "CPB": normalizeBovadaCPBTeamNames,
        "PP": normalizeBovadaPPTeamNames,
        "EC": normalizeBovadaECTeamNames,
        "PL1": normalizeBovadaPL1TeamNames,
        "USD": normalizeBovadaUSDTeamNames,
        "BPD": normalizeBovadaBPDTeamNames,
        "MLM": normalizeBovadaMLMTeamNames,
        'EPL': normalizeBovadaEPLTeamNames,
        'EFL': normalizeBovadaEFLTeamNames,
        'EL1': normalizeBovadaEL1TeamNames,
        'EL2': normalizeBovadaEL2TeamNames,
        'SP': normalizeBovadaSPTeamNames,
        'SC': normalizeBovadaSCTeamNames,
        'IFD': normalizeBovadaIFDTeamNames,
        'IPD': normalizeBovadaIPDTeamNames,
        'SPD': normalizeBovadaSPDTeamNames,
        'SSD': normalizeBovadaSSDTeamNames,
        'FL1': normalizeBovadaFL1TeamNames,
        'FL2': normalizeBovadaFL2TeamNames
    }
    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeBovadaALPTeamNames(team_name):
    correct_name = team_name
    if("Tallares de Cordoba" == team_name):
        correct_name = "Talleres"
    if("Unión de Santa Fe" == team_name):
        correct_name = "Union"
    else:
        correct_name = process.extract(team_name, Liga_Profesional, limit=1)[0][0]
    return correct_name
def normalizeBovadaBSATeamNames(team_name):
    if team_name == 'Atlético Mineiro': return 'Atletico MG'
    return process.extract(team_name, Brazil_Serie_A, limit=1)[0][0]
def normalizeBovadaBSBTeamNames(team_name):
    return process.extract(team_name, Brazil_Serie_B, limit=1)[0][0]
def normalizeBovadaCPATeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_A, limit=1)[0][0]
def normalizeBovadaCPBTeamNames(team_name):
    return process.extract(team_name, Colombia_Primera_B, limit=1)[0][0]
def normalizeBovadaPPTeamNames(team_name):
    return process.extract(team_name, Paraguay_Primera, limit=1)[0][0]
def normalizeBovadaECTeamNames(team_name):
    return process.extract(team_name, Ecuador_ProLiga, limit=1)[0][0]
def normalizeBovadaPL1TeamNames(team_name):
    return process.extract(team_name, Peru_Liga1, limit=1)[0][0]
def normalizeBovadaUSDTeamNames(team_name):
    return process.extract(team_name, Uruguay_Seg_Div, limit=1)[0][0]
def normalizeBovadaBPDTeamNames(team_name):
    return process.extract(team_name, Bolivia_Primera, limit=1)[0][0]
def normalizeBovadaUSMTeamNames(team_name):
    correct_name = team_name
    if("Columbus Crew" == team_name):
        correct_name = "Columbus Crew"
    if("New York City FC" == team_name):
        correct_name = "New York City Football"
    else:
        correct_name = process.extract(team_name, UnitedS_Major_League, limit=1)[0][0]
    return correct_name
def normalizeBovadaMLMTeamNames(team_name):
    return process.extract(team_name, Mexico_Liga_MX, limit=1)[0][0]
def normalizeBovadaEPLTeamNames(team_name):
    return process.extract(team_name, English_Premier_League, limit=1)[0][0]
def normalizeBovadaEFLTeamNames(team_name):
    return process.extract(team_name, English_Football_League, limit=1)[0][0]
def normalizeBovadaEL1TeamNames(team_name):
    return process.extract(team_name, English_League_One, limit=1)[0][0]
def normalizeBovadaEL2TeamNames(team_name):
    return process.extract(team_name, English_League_Two, limit=1)[0][0]
def normalizeBovadaSPTeamNames(team_name):
    return process.extract(team_name, Scotland_Premiership, limit=1)[0][0]
def normalizeBovadaSCTeamNames(team_name):
    return process.extract(team_name, Scotland_Championship, limit=1)[0][0]
def normalizeBovadaIFDTeamNames(team_name):
    return process.extract(team_name, Ireland_First_Division, limit=1)[0][0]
def normalizeBovadaIPDTeamNames(team_name):
    return process.extract(team_name, Ireland_Premier_Division, limit=1)[0][0]
def normalizeBovadaSPDTeamNames(team_name):
    return process.extract(team_name, Spain_Primera_Division, limit=1)[0][0]
def normalizeBovadaSSDTeamNames(team_name):
    return process.extract(team_name, Spain_Segunda_Division, limit=1)[0][0]
def normalizeBovadaFL1TeamNames(team_name):
    return process.extract(team_name, France_Ligue1, limit=1)[0][0]
def normalizeBovadaFL2TeamNames(team_name):
    return process.extract(team_name, France_Ligue2, limit=1)[0][0]

if __name__ == '__main__':
    bovada_dict = bovadaBSA()
    pd.set_option('display.max_colwidth', None)
    bovadadF = pd.DataFrame.from_dict(bovada_dict)
    print(bovadadF)