import threading
import asyncio
import warnings
import bet9ja, nairabet, betking, betwinner, merrybet, sunbet, sportybet, campeonbet, bet188
import bookmakereu, dafabet, marathonbet, sbobetSe, b365_Whill_Pinncl, betfairSe, coolbet, bovada
from db import soccer_leagues
import utils as utils
import pandas as pd
import colorama
from colorama import Fore, Style
from match import Arb

arbs = []
class MyThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = {"Name":"", "Matches": []}

    def run(self):
        self._result = self._target(*self._args)

def main():
    colorama.init()
    for league in soccer_leagues.keys():
        try:
            matchLeague(league)
        except:
            pass
    # matchLeague('EPL') #EPL - English Premier League

def matchBookmakers(sport_list, max_x_odds, max_x_odds_fh, max_x_odds_sh, league):
    for k in range(len(sport_list) - 1):
        for i in range(k + 1, len(sport_list)):
            if(sport_list[i]['Matches'] and sport_list[k]['Matches']):
                findArbOppThreeway(sport_list[k], sport_list[i], max_x_odds, max_x_odds_fh, max_x_odds_sh, league)

def matchLeague(league):
    tasks = []
    threads = []
    bookmakers = []
    # if hasattr(sbobetSe, f"sbobet{league}"):
    #     tasks.append(getattr(sbobetSe, f"sbobet{league}"))
    if hasattr(dafabet, f"dafabet{league}"):
        tasks.append(getattr(dafabet, f"dafabet{league}"))
    if hasattr(betking, f"betking{league}"):
        tasks.append(getattr(betking, f"betking{league}"))
    if hasattr(bet9ja, f"bet9ja{league}"):
        tasks.append(getattr(bet9ja, f"bet9ja{league}"))
    if hasattr(nairabet, f"nairabet{league}"):
        tasks.append(getattr(nairabet, f"nairabet{league}"))    
    if hasattr(merrybet, f"merrybet{league}"):
        tasks.append(getattr(merrybet, f"merrybet{league}"))
    if hasattr(bovada, f"bovada{league}"):
        tasks.append(getattr(bovada, f"bovada{league}"))
    if hasattr(sportybet, f"sportybet{league}"):
        tasks.append(getattr(sportybet, f"sportybet{league}"))
    if hasattr(sunbet, f"sunbet{league}"):
        tasks.append(getattr(sunbet, f"sunbet{league}"))
    if hasattr(coolbet, f"coolbet{league}"):
        tasks.append(getattr(coolbet, f"coolbet{league}"))
    if hasattr(campeonbet, f"campeonbet{league}"):
        tasks.append(getattr(campeonbet, f"campeonbet{league}"))
    #if hasattr(betwinner, f"betwinner{league}"):
    #    tasks.append(getattr(betwinner, f"betwinner{league}"))
    if hasattr(bookmakereu, f"bookmakereu{league}"):
        tasks.append(getattr(bookmakereu, f"bookmakereu{league}"))
    if hasattr(b365_Whill_Pinncl, f"{league}"):
        tasks.append(getattr(b365_Whill_Pinncl, f"{league}"))
    if hasattr(marathonbet, f"marathonbet{league}"):
        tasks.append(getattr(marathonbet, f"marathonbet{league}"))
    if hasattr(bet188, f"bet188{league}"):
        tasks.append(getattr(bet188, f"bet188{league}"))

    for function in tasks:
        thread = MyThread(target=function)
        threads.append(thread)
    # Start the threads
    for thread in threads:
        thread.start()
    # Wait for the threads to finish
    for thread in threads:
        thread.join()
    # Store the outputs
    for thread in threads:
        if(thread):
            if(type(thread._result) is list):
                bookmakers.extend(thread._result)
            else:
                bookmakers.append(thread._result)

    # if hasattr(betfairSe, f"betfair{league}"):
    #     betfair_dict = asyncio.run(getattr(betfairSe, f"betfair{league}")())
    #     bookmakers.append(betfair_dict)
    max_x_odds = highestDrawOdd(bookmakers, 'draw_odd')
    max_x_odds_fh = highestDrawOdd(bookmakers, 'fh1x2')
    max_x_odds_sh = highestDrawOdd(bookmakers, 'sh1x2')
    #max_nogoal_odds_fg = highestDrawOdd(bookmakers, 'fg')
    #max_nogoal_odds_lg = highestDrawOdd(bookmakers, 'ltts')
    print(bookmakers)
    return

    # matchBookmakers(bookmakers, max_x_odds, max_x_odds_fh, max_x_odds_sh, league)

def highestDrawOdd(bookmakers, attribute):
    max_draw_odds = {}
    for bookmaker in bookmakers:
        print(bookmaker["Name"])
        bookmaker_name = bookmaker["Name"]
        matches = bookmaker["Matches"]
        for match in matches:
            match_name = match.name

            value = getattr(match, attribute)
            if(attribute == 'draw_odd'):
                if(value): # for 1X2 draw_odd
                    draw_odd = value
                else:
                    draw_odd = 0.0
            else:
                if(len(value) == 3): # for every other draw, since it is in an array
                    draw_odd = value[2]
                else:
                    draw_odd = 0.0

            if match_name not in max_draw_odds:
                # First occurrence of the match, initialize the max_draw_odd
                max_draw_odds[match_name] = {"bookmaker": bookmaker_name, "draw_odd": draw_odd}
            elif draw_odd > max_draw_odds[match_name]["draw_odd"]:
                # Update the max_draw_odd if a higher value is found
                max_draw_odds[match_name] = {"bookmaker": bookmaker_name, "draw_odd": draw_odd}
    return max_draw_odds

def findArbOppTwoway(bookie1_dict, bookie2_dict):
    print(f"---------- \033[31m{bookie1_dict['Name']}\033[0m AND \033[31m{bookie2_dict['Name']}\033[0m ----------")
    
    b1_teams = [m.name for m in bookie1_dict['Matches']]
    b2_teams = [m.name for m in bookie2_dict['Matches']]

    matches_dict = {i:name for i, name in enumerate(b1_teams) if name in b2_teams}
    matches_dict1 = {i:name for i, name in enumerate(b2_teams) if name in b1_teams}
    sorted_dict = dict(sorted(matches_dict.items(), key=lambda x: x[1]))
    sorted_dict1 = dict(sorted(matches_dict1.items(), key=lambda x: x[1]))
    
    for key in zip(sorted_dict, sorted_dict1):
        bookie1HomeOdd = float(bookie1_dict["Matches"][key[0]].home_odd)
        bookie2AwayOdd = float(bookie2_dict["Matches"][key[1]].away_odd)
        bookie1AwayOdd = float(bookie1_dict["Matches"][key[0]].away_odd)
        bookie2HomeOdd = float(bookie2_dict["Matches"][key[1]].home_odd)

        roi1 = utils.returnOnInvestment(bookie1HomeOdd, bookie2AwayOdd)
        roi2 = utils.returnOnInvestment(bookie1AwayOdd, bookie2HomeOdd)

        split_team = bookie1_dict["Matches"][key[0]].name.split("-")
        team1 = split_team[0].strip()
        team2 = split_team[1].strip()
        print(f"\033[33m{bookie1_dict['Name']:<42}\033[0m\033[33m{bookie2_dict['Name']:<42}\033[0m")

        if(roi1 > 0):
            print(f"{team1:<35} {bookie1HomeOdd:^5} {team2:<35} {bookie2AwayOdd:^5} ROI \033[32m{format(roi1, '.2f')}\033[0m")
        else:
            print(f"{team1:<35} {bookie1HomeOdd:^5} {team2:<35} {bookie2AwayOdd:^5} ROI \033[31m{format(roi1, '.2f')}\033[0m")
        if(roi2 > 0):
            print(f"{team2:<35} {bookie1AwayOdd:^5} {team1:<35} {bookie2HomeOdd:^5} ROI \033[32m{format(roi2, '.2f')}\033[0m")
        else:
            print(f"{team2:<35} {bookie1AwayOdd:^5} {team1:<35} {bookie2HomeOdd:^5} ROI \033[31m{format(roi2, '.2f')}\033[0m")
def findArbOppThreeway(bookie1_dict, bookie2_dict, max_draw_odds, max_x_odds_fh, max_x_odds_sh, league):
    print(f"----------------------------------------- \033[31m{bookie1_dict['Name']}\033[0m AND \033[31m{bookie2_dict['Name']}\033[0m -----------------------------------------")
    
    b1_teams = [m.name for m in bookie1_dict['Matches']]
    b2_teams = [m.name for m in bookie2_dict['Matches']]

    matches_dict = {i:name for i, name in enumerate(b1_teams) if name in b2_teams}
    matches_dict1 = {i:name for i, name in enumerate(b2_teams) if name in b1_teams}
    sorted_dict = dict(sorted(matches_dict.items(), key=lambda x: x[1]))
    sorted_dict1 = dict(sorted(matches_dict1.items(), key=lambda x: x[1]))

    for key in zip(sorted_dict, sorted_dict1):
        bookie1HomeOdd = float(bookie1_dict["Matches"][key[0]].home_odd)
        bookie2AwayOdd = float(bookie2_dict["Matches"][key[1]].away_odd)
        bookie1AwayOdd = float(bookie1_dict["Matches"][key[0]].away_odd)
        bookie2HomeOdd = float(bookie2_dict["Matches"][key[1]].home_odd)
        bookie1DrawOdd = float(bookie1_dict["Matches"][key[0]].draw_odd)
        bookie2DrawOdd = float(bookie2_dict["Matches"][key[1]].draw_odd)

        # 1X2
        max_draw_bookie = ""
        if(bookie1DrawOdd > bookie2DrawOdd): max_draw_bookie = bookie1_dict['Name']
        else: max_draw_bookie = bookie2_dict['Name']
        max_draw = bookie1DrawOdd if bookie1DrawOdd > bookie2DrawOdd else bookie2DrawOdd
        if(bookie1_dict["Matches"][key[0]].name in max_draw_odds):
            max_draw = max_draw_odds[bookie1_dict["Matches"][key[0]].name]['draw_odd']
            max_draw_bookie = max_draw_odds[bookie1_dict["Matches"][key[0]].name]['bookmaker']

        roi1 = utils.returnOnInvestmentThreeway(bookie1HomeOdd, bookie2AwayOdd, max_draw)
        roi2 = utils.returnOnInvestmentThreeway(bookie1AwayOdd, bookie2HomeOdd, max_draw)

        split_team = bookie1_dict["Matches"][key[0]].name.split(" - ")
        team1 = split_team[0].strip()
        team2 = split_team[1].strip()

        ROI = "ROI"
        print(f"\033[33m{bookie1_dict['Name']:<42}\033[0m\033[33m{bookie2_dict['Name']:<42}\033[0m\033[33mHighest X {max_draw_bookie:<10}\033[0m\033[33m{ROI:>10}\033[0m")
        if(roi1 > 0):
            arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie1HomeOdd,
                      odd2=bookie2AwayOdd, odd3=max_draw, roi=roi1, wager_type="Moneyline 1x2", home_team=team1, away_team=team2, league=league) 
            arbs.append(arb)
            print(f"{team1:<35} {bookie1HomeOdd:^5} {team2:<35} {bookie2AwayOdd:^5} {max_draw:^5} \033[32m{format(roi1, '.2f'):>25}\033[0m")
        else:
            print(f"{team1:<35} {bookie1HomeOdd:^5} {team2:<35} {bookie2AwayOdd:^5} {max_draw:^5} \033[31m{format(roi1, '.2f'):>25}\033[0m")
        if(roi2 > 0):
            arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie2HomeOdd,
                      odd2=bookie1AwayOdd, odd3=max_draw, roi=roi2, wager_type="Moneyline 1x2", home_team=team1, away_team=team2, league=league) 
            arbs.append(arb)
            print(f"{team2:<35} {bookie1AwayOdd:^5} {team1:<35} {bookie2HomeOdd:^5} {max_draw:^5} \033[32m{format(roi2, '.2f'):>25}\033[0m")
        else:
                print(f"{team2:<35} {bookie1AwayOdd:^5} {team1:<35} {bookie2HomeOdd:^5} {max_draw:^5} \033[31m{format(roi2, '.2f'):>25}\033[0m")
        
        # FH 1X2
        if(bookie1_dict["Matches"][key[0]].fh1x2 and bookie2_dict["Matches"][key[1]].fh1x2):
            bookie1HomeOdd = bookie1_dict["Matches"][key[0]].fh1x2[0]
            bookie1AwayOdd = bookie1_dict["Matches"][key[0]].fh1x2[1]
            bookie2HomeOdd = bookie2_dict["Matches"][key[1]].fh1x2[0]
            bookie2AwayOdd = bookie2_dict["Matches"][key[1]].fh1x2[1]
            bookie1DrawOdd = bookie1_dict["Matches"][key[0]].fh1x2[2]
            bookie2DrawOdd = bookie2_dict["Matches"][key[1]].fh1x2[2]
            
            max_draw_bookie = ""
            if(bookie1DrawOdd > bookie2DrawOdd): max_draw_bookie = bookie1_dict['Name']
            else: max_draw_bookie = bookie2_dict['Name']
            max_draw = bookie1DrawOdd if bookie1DrawOdd > bookie2DrawOdd else bookie2DrawOdd
            if(bookie1_dict["Matches"][key[0]].name in max_x_odds_fh):
                max_draw = max_x_odds_fh[bookie1_dict["Matches"][key[0]].name]['draw_odd']
                max_draw_bookie = max_x_odds_fh[bookie1_dict["Matches"][key[0]].name]['bookmaker']

            roi1 = utils.returnOnInvestmentThreeway(bookie1HomeOdd, bookie2AwayOdd, max_draw)
            roi2 = utils.returnOnInvestmentThreeway(bookie1AwayOdd, bookie2HomeOdd, max_draw)
            if(roi1 > 0):
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie1HomeOdd,
                        odd2=bookie2AwayOdd, odd3=max_draw, roi=roi1, wager_type="First Half 1x2", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"(FH){team1:<31} {bookie1HomeOdd:^5} (FH){team2:<31} {bookie2AwayOdd:^5} {max_draw:^5} \033[32m{format(roi1, '.2f'):>25}\033[0m")
            else:
                print(f"(FH){team1:<31} {bookie1HomeOdd:^5} (FH){team2:<31} {bookie2AwayOdd:^5} {max_draw:^5} \033[31m{format(roi1, '.2f'):>25}\033[0m")
            if(roi2 > 0):
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie2HomeOdd,
                        odd2=bookie1AwayOdd, odd3=max_draw, roi=roi2, wager_type="First Half 1x2", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"(FH){team2:<31} {bookie1AwayOdd:^5} (FH){team1:<31} {bookie2HomeOdd:^5} {max_draw:^5} \033[32m{format(roi2, '.2f'):>25}\033[0m")
            else:
                print(f"(FH){team2:<31} {bookie1AwayOdd:^5} (FH){team1:<31} {bookie2HomeOdd:^5} {max_draw:^5} \033[31m{format(roi2, '.2f'):>25}\033[0m")
        
        # SH 1X2
        if(bookie1_dict["Matches"][key[0]].sh1x2 and bookie2_dict["Matches"][key[1]].sh1x2):
            bookie1HomeOdd = bookie1_dict["Matches"][key[0]].sh1x2[0]
            bookie1AwayOdd = bookie1_dict["Matches"][key[0]].sh1x2[1]
            bookie2HomeOdd = bookie2_dict["Matches"][key[1]].sh1x2[0]
            bookie2AwayOdd = bookie2_dict["Matches"][key[1]].sh1x2[1]
            bookie1DrawOdd = bookie1_dict["Matches"][key[0]].sh1x2[2]
            bookie2DrawOdd = bookie2_dict["Matches"][key[1]].sh1x2[2]
            
            max_draw_bookie = ""
            if(bookie1DrawOdd > bookie2DrawOdd): max_draw_bookie = bookie1_dict['Name']
            else: max_draw_bookie = bookie2_dict['Name']
            max_draw = bookie1DrawOdd if bookie1DrawOdd > bookie2DrawOdd else bookie2DrawOdd
            if(bookie1_dict["Matches"][key[0]].name in max_x_odds_sh):
                max_draw = max_x_odds_sh[bookie1_dict["Matches"][key[0]].name]['draw_odd']
                max_draw_bookie = max_x_odds_sh[bookie1_dict["Matches"][key[0]].name]['bookmaker']

            roi1 = utils.returnOnInvestmentThreeway(bookie1HomeOdd, bookie2AwayOdd, max_draw)
            roi2 = utils.returnOnInvestmentThreeway(bookie1AwayOdd, bookie2HomeOdd, max_draw)
            if(roi1 > 0):
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie1HomeOdd,
                        odd2=bookie2AwayOdd, odd3=max_draw, roi=roi1, wager_type="Second Half 1x2", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"(SH){team1:<31} {bookie1HomeOdd:^5} (SH){team2:<31} {bookie2AwayOdd:^5} {max_draw:^5} \033[32m{format(roi1, '.2f'):>25}\033[0m")
            else:
                print(f"(SH){team1:<31} {bookie1HomeOdd:^5} (SH){team2:<31} {bookie2AwayOdd:^5} {max_draw:^5} \033[31m{format(roi1, '.2f'):>25}\033[0m")
            if(roi2 > 0):
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], book3=max_draw_bookie, odd1=bookie2HomeOdd,
                        odd2=bookie1AwayOdd, odd3=max_draw, roi=roi2, wager_type="Second Half 1x2", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"(SH){team2:<31} {bookie1AwayOdd:^5} (SH){team1:<31} {bookie2HomeOdd:^5} {max_draw:^5} \033[32m{format(roi2, '.2f'):>25}\033[0m")
            else:
                print(f"(SH){team2:<31} {bookie1AwayOdd:^5} (SH){team1:<31} {bookie2HomeOdd:^5} {max_draw:^5} \033[31m{format(roi2, '.2f'):>25}\033[0m")
        
        # DRAW NO BET
        if(bookie1_dict['Matches'][key[0]].dnb and bookie2_dict['Matches'][key[1]].dnb):
            ou = checkDrawNoBet(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if ou[0] > 0:
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].dnb[0],
                        odd2=bookie2_dict['Matches'][key[1]].dnb[1], roi=ou[0], wager_type="Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}DNB {bookie1_dict['Matches'][key[0]].dnb[0]:>36} {bookie2_dict['Matches'][key[1]].dnb[1]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[0]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}DNB {bookie1_dict['Matches'][key[0]].dnb[0]:>36} {bookie2_dict['Matches'][key[1]].dnb[1]:>41} {Fore.YELLOW} {Fore.RED}{ou[0]:>31}{Style.RESET_ALL}")
            if ou[1] > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].dnb[1],
                        odd2=bookie2_dict['Matches'][key[1]].dnb[0], roi=ou[1], wager_type="Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}DNB {bookie1_dict['Matches'][key[0]].dnb[1]:>36} {bookie2_dict['Matches'][key[1]].dnb[0]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[1]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}DNB {bookie1_dict['Matches'][key[0]].dnb[1]:>36} {bookie2_dict['Matches'][key[1]].dnb[0]:>41} {Fore.YELLOW} {Fore.RED}{ou[1]:>31}{Style.RESET_ALL}")
        # FH DRAW NO BET
        if(bookie1_dict['Matches'][key[0]].fh_dnb and bookie2_dict['Matches'][key[1]].fh_dnb):
            ou = checkFHDrawNoBet(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if ou[0] > 0:
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_dnb[0],
                        odd2=bookie2_dict['Matches'][key[1]].fh_dnb[1], roi=ou[0], wager_type="First Half Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].fh_dnb[0]:>36} {bookie2_dict['Matches'][key[1]].fh_dnb[1]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[0]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].fh_dnb[0]:>36} {bookie2_dict['Matches'][key[1]].fh_dnb[1]:>41} {Fore.YELLOW} {Fore.RED}{ou[0]:>31}{Style.RESET_ALL}")
            if ou[1] > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_dnb[1],
                        odd2=bookie2_dict['Matches'][key[1]].fh_dnb[0], roi=ou[1], wager_type="First Half Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].fh_dnb[1]:>36} {bookie2_dict['Matches'][key[1]].fh_dnb[0]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[1]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].fh_dnb[1]:>36} {bookie2_dict['Matches'][key[1]].fh_dnb[0]:>41} {Fore.YELLOW} {Fore.RED}{ou[1]:>31}{Style.RESET_ALL}")
        # SH DRAW NO BET
        if(bookie1_dict['Matches'][key[0]].sh_dnb and bookie2_dict['Matches'][key[1]].sh_dnb):
            ou = checkSHDrawNoBet(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if ou[0] > 0:
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].sh_dnb[0],
                        odd2=bookie2_dict['Matches'][key[1]].sh_dnb[1], roi=ou[0], wager_type="Second Half Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}SHDNB {bookie1_dict['Matches'][key[0]].sh_dnb[0]:>36} {bookie2_dict['Matches'][key[1]].sh_dnb[1]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[0]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}SHDNB {bookie1_dict['Matches'][key[0]].sh_dnb[0]:>36} {bookie2_dict['Matches'][key[1]].sh_dnb[1]:>41} {Fore.YELLOW} {Fore.RED}{ou[0]:>31}{Style.RESET_ALL}")
            if ou[1] > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].sh_dnb[1],
                        odd2=bookie2_dict['Matches'][key[1]].sh_dnb[0], roi=ou[1], wager_type="First Half Draw No Bet", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].sh_dnb[1]:>36} {bookie2_dict['Matches'][key[1]].sh_dnb[0]:>41} {Fore.YELLOW} {Fore.GREEN}{ou[1]:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FHDNB {bookie1_dict['Matches'][key[0]].sh_dnb[1]:>36} {bookie2_dict['Matches'][key[1]].sh_dnb[0]:>41} {Fore.YELLOW} {Fore.RED}{ou[1]:>31}{Style.RESET_ALL}")
        # GGNG
        if(bookie1_dict['Matches'][key[0]].ggng and bookie2_dict['Matches'][key[1]].ggng):
            roi1, roi2 = checkGGNG(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if roi1 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].ggng[0],
                        odd2=bookie2_dict['Matches'][key[1]].ggng[1], roi=roi1, wager_type="GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}GGNG{bookie1_dict['Matches'][key[0]].ggng[0]:>36} {bookie2_dict['Matches'][key[1]].ggng[1]:>41} {Fore.YELLOW} {Fore.GREEN}{roi1:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}GGNG{bookie1_dict['Matches'][key[0]].ggng[0]:>36} {bookie2_dict['Matches'][key[1]].ggng[1]:>41} {Fore.YELLOW} {Fore.RED}{roi1:>31}{Style.RESET_ALL}")
            if roi2 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].ggng[1],
                        odd2=bookie2_dict['Matches'][key[1]].ggng[0], roi=roi2, wager_type="GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}GGNG{bookie1_dict['Matches'][key[0]].ggng[1]:>36} {bookie2_dict['Matches'][key[1]].ggng[0]:>41} {Fore.YELLOW} {Fore.GREEN}{roi2:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}GGNG{bookie1_dict['Matches'][key[0]].ggng[1]:>36} {bookie2_dict['Matches'][key[1]].ggng[0]:>41} {Fore.YELLOW} {Fore.RED}{roi2:>31}{Style.RESET_ALL}")
        # FH GGNG
        if(bookie1_dict['Matches'][key[0]].fh_ggng and bookie2_dict['Matches'][key[1]].fh_ggng):
            roi1, roi2 = checkFHGGNG(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if roi1 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_ggng[0],
                        odd2=bookie2_dict['Matches'][key[1]].fh_ggng[1], roi=roi1, wager_type="First Half GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FHGGNG{bookie1_dict['Matches'][key[0]].fh_ggng[0]:>36} {bookie2_dict['Matches'][key[1]].fh_ggng[1]:>41} {Fore.YELLOW} {Fore.GREEN}{roi1:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FHGGNG{bookie1_dict['Matches'][key[0]].fh_ggng[0]:>36} {bookie2_dict['Matches'][key[1]].fh_ggng[1]:>41} {Fore.YELLOW} {Fore.RED}{roi1:>31}{Style.RESET_ALL}")
            if roi2 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_ggng[1],
                        odd2=bookie2_dict['Matches'][key[1]].fh_ggng[0], roi=roi2, wager_type="First Half GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FHGGNG{bookie1_dict['Matches'][key[0]].fh_ggng[1]:>36} {bookie2_dict['Matches'][key[1]].fh_ggng[0]:>41} {Fore.YELLOW} {Fore.GREEN}{roi2:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FHGGNG{bookie1_dict['Matches'][key[0]].fh_ggng[1]:>36} {bookie2_dict['Matches'][key[1]].fh_ggng[0]:>41} {Fore.YELLOW} {Fore.RED}{roi2:>31}{Style.RESET_ALL}")
        # SH GGNG
        if(bookie1_dict['Matches'][key[0]].sh_ggng and bookie2_dict['Matches'][key[1]].sh_ggng):
            roi1, roi2 = checkSHGGNG(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if roi1 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].sh_ggng[0],
                        odd2=bookie2_dict['Matches'][key[1]].sh_ggng[1], roi=roi1, wager_type="Second Half GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}SHGGNG{bookie1_dict['Matches'][key[0]].sh_ggng[0]:>36} {bookie2_dict['Matches'][key[1]].sh_ggng[1]:>41} {Fore.YELLOW} {Fore.GREEN}{roi1:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}SHGGNG{bookie1_dict['Matches'][key[0]].sh_ggng[0]:>36} {bookie2_dict['Matches'][key[1]].sh_ggng[1]:>41} {Fore.YELLOW} {Fore.RED}{roi1:>31}{Style.RESET_ALL}")
            if roi2 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].sh_ggng[1],
                        odd2=bookie2_dict['Matches'][key[1]].sh_ggng[0], roi=roi2, wager_type="Second Half GG/NG", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}SHGGNG{bookie1_dict['Matches'][key[0]].sh_ggng[1]:>36} {bookie2_dict['Matches'][key[1]].sh_ggng[0]:>41} {Fore.YELLOW} {Fore.GREEN}{roi2:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}SHGGNG{bookie1_dict['Matches'][key[0]].sh_ggng[1]:>36} {bookie2_dict['Matches'][key[1]].sh_ggng[0]:>41} {Fore.YELLOW} {Fore.RED}{roi2:>31}{Style.RESET_ALL}")
        # ODD/EVEN
        if(bookie1_dict['Matches'][key[0]].odd_even and bookie2_dict['Matches'][key[1]].odd_even):
            roi1, roi2 = checkOE(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if roi1 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].odd_even[0],
                        odd2=bookie2_dict['Matches'][key[1]].odd_even[1], roi=roi1, wager_type="Total Goals Odd/Even", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}OE{bookie1_dict['Matches'][key[0]].odd_even[0]:>36} {bookie2_dict['Matches'][key[1]].odd_even[1]:>41} {Fore.YELLOW} {Fore.GREEN}{roi1:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}OE{bookie1_dict['Matches'][key[0]].odd_even[0]:>36} {bookie2_dict['Matches'][key[1]].odd_even[1]:>41} {Fore.YELLOW} {Fore.RED}{roi1:>31}{Style.RESET_ALL}")
            if roi2 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].odd_even[1],
                        odd2=bookie2_dict['Matches'][key[1]].odd_even[0], roi=roi2, wager_type="Total Goals Odd/Even", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}OE{bookie1_dict['Matches'][key[0]].odd_even[1]:>36} {bookie2_dict['Matches'][key[1]].odd_even[0]:>41} {Fore.YELLOW} {Fore.GREEN}{roi2:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}OE{bookie1_dict['Matches'][key[0]].odd_even[1]:>36} {bookie2_dict['Matches'][key[1]].odd_even[0]:>41} {Fore.YELLOW} {Fore.RED}{roi2:>31}{Style.RESET_ALL}")
        # FH ODD/EVEN
        if(bookie1_dict['Matches'][key[0]].fh_odd_even and bookie2_dict['Matches'][key[1]].fh_odd_even):
            roi1, roi2 = checkFHOE(bookie1_dict['Matches'][key[0]], bookie2_dict['Matches'][key[1]])
            if roi1 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_odd_even[0],
                        odd2=bookie2_dict['Matches'][key[1]].fh_odd_even[1], roi=roi1, wager_type="Total Goals First Half Odd/Even", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FH OE{bookie1_dict['Matches'][key[0]].fh_odd_even[0]:>36} {bookie2_dict['Matches'][key[1]].fh_odd_even[1]:>41} {Fore.YELLOW} {Fore.GREEN}{roi1:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FH OE{bookie1_dict['Matches'][key[0]].fh_odd_even[0]:>36} {bookie2_dict['Matches'][key[1]].fh_odd_even[1]:>41} {Fore.YELLOW} {Fore.RED}{roi1:>31}{Style.RESET_ALL}")
            if roi2 > 0: 
                arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=bookie1_dict['Matches'][key[0]].fh_odd_even[1],
                        odd2=bookie2_dict['Matches'][key[1]].fh_odd_even[0], roi=roi2, wager_type="Total Goals First Half Odd/Even", home_team=team1, away_team=team2, league=league) 
                arbs.append(arb)
                print(f"{Fore.CYAN}FH OE{bookie1_dict['Matches'][key[0]].fh_odd_even[1]:>36} {bookie2_dict['Matches'][key[1]].fh_odd_even[0]:>41} {Fore.YELLOW} {Fore.GREEN}{roi2:>31}{Style.RESET_ALL}")
            else: 
                print(f"{Fore.CYAN}FH OE{bookie1_dict['Matches'][key[0]].fh_odd_even[1]:>36} {bookie2_dict['Matches'][key[1]].fh_odd_even[0]:>41} {Fore.YELLOW} {Fore.RED}{roi2:>31}{Style.RESET_ALL}")
        # OVER / UNDER 
        if(bookie1_dict["Matches"][key[0]].over and bookie2_dict["Matches"][key[1]].under):
            ou = checkOverUnder(bookie1_dict["Matches"][key[0]], bookie2_dict["Matches"][key[1]])
            for key, value in ou[0].items(): # (over:2.5(1.6), under:2.5(2.2): ), (-7.37)
                if value < 0:
                    print(f"{key}: \033[31m{value}\033[0m", end=" \n")
                else:
                    home_odd, away_odd, line_h, line_a = extract_odds_lines(key)
                    arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=home_odd, odd2=away_odd, roi=value, 
                              wager_type="Over/Under", home_team=team1, away_team=team2, line_h=line_h, line_a=line_a, league=league) 
                    arbs.append(arb)
                    print(f"{key}: \033[32m{value}\033[0m", end=" \n")
            for key, value in ou[1].items():
                if value < 0:
                    print(f"{key}: \033[31m{value}\033[0m", end=" \n")
                else:
                    home_odd, away_odd, line_h, line_a = extract_odds_lines(key)
                    arb = Arb(book1=bookie1_dict['Name'], book2=bookie2_dict['Name'], odd1=away_odd, odd2=home_odd, roi=value, 
                              wager_type="Over/Under", home_team=team2, away_team=team1, line_h=line_h, line_a=line_a, league=league) 
                    arbs.append(arb)
                    print(f"{key}: \033[32m{value}\033[0m", end=" \n")

def extract_odds_lines(key): # For Over/Under
    relevant_part_h = key.split("over:")[1].split(",")[0]
    home_odd = relevant_part_h.split("(")[1].split(")")[0]
    relevant_part_a = key.split("under:")[1]
    away_odd = relevant_part_a.split("(")[1].split(")")[0]
    line_h = key.split("(")[0]
    line_a = key.split(", ")[1].split("(")[0]
    return home_odd, away_odd, line_h, line_a
def makeTwoDictionariesSameLength(dict1, dict2):
    max_len = max(len(dict1), len(dict2))
    diff = max_len - len(dict1)
    if diff > 0:
        dict1.update({len(dict1)+i+1: 'Team' for i in range(diff)})
    return dict1
def checkOverUnder(bookie1, bookie2):
    roi1 = {f"over:{key1}({bookie1.over[key1]}), under:{key2}({bookie2.under[key2]})": utils.returnOnInvestment(float(bookie1.over[key1]), float(bookie2.under[key2]))
           for key1 in bookie1.over
           for key2 in bookie2.under
           if float(key1) <= float(key2)}
    roi2 = {f"over:{key1}({bookie2.over[key1]}), under:{key2}({bookie1.under[key2]})": utils.returnOnInvestment(float(bookie2.over[key1]), float(bookie1.under[key2]))
           for key1 in bookie2.over
           for key2 in bookie1.under
           if float(key1) <= float(key2)}
    return roi1, roi2
def checkDrawNoBet(bookie1, bookie2):
    roi2 = utils.returnOnInvestment(bookie1.dnb[1], bookie2.dnb[0])
    roi1 = utils.returnOnInvestment(bookie1.dnb[0], bookie2.dnb[1])
    return roi1, roi2
def checkFHDrawNoBet(bookie1, bookie2):
    roi2 = utils.returnOnInvestment(bookie1.fh_dnb[1], bookie2.fh_dnb[0])
    roi1 = utils.returnOnInvestment(bookie1.fh_dnb[0], bookie2.fh_dnb[1])
    return roi1, roi2
def checkSHDrawNoBet(bookie1, bookie2):
    roi2 = utils.returnOnInvestment(bookie1.sh_dnb[1], bookie2.sh_dnb[0])
    roi1 = utils.returnOnInvestment(bookie1.sh_dnb[0], bookie2.sh_dnb[1])
    return roi1, roi2
def checkGGNG(bookie1, bookie2):
    roi1 = utils.returnOnInvestment(bookie1.ggng[0], bookie2.ggng[1])
    roi2 = utils.returnOnInvestment(bookie1.ggng[1], bookie2.ggng[0])
    return roi1, roi2
def checkFHGGNG(bookie1, bookie2):
    roi1 = utils.returnOnInvestment(bookie1.fh_ggng[0], bookie2.fh_ggng[1])
    roi2 = utils.returnOnInvestment(bookie1.fh_ggng[1], bookie2.fh_ggng[0])
    return roi1, roi2
def checkSHGGNG(bookie1, bookie2):
    roi1 = utils.returnOnInvestment(bookie1.sh_ggng[0], bookie2.sh_ggng[1])
    roi2 = utils.returnOnInvestment(bookie1.sh_ggng[1], bookie2.sh_ggng[0])
    return roi1, roi2
def checkOE(bookie1, bookie2):
    roi1 = utils.returnOnInvestment(bookie1.odd_even[0], bookie2.odd_even[1])
    roi2 = utils.returnOnInvestment(bookie1.odd_even[1], bookie2.odd_even[0])
    return roi1, roi2
def checkFHOE(bookie1, bookie2):
    roi1 = utils.returnOnInvestment(bookie1.fh_odd_even[0], bookie2.fh_odd_even[1])
    roi2 = utils.returnOnInvestment(bookie1.fh_odd_even[1], bookie2.fh_odd_even[0])
    return roi1, roi2

if __name__ == '__main__':
    main()
    print('FINISHED')
    if(arbs):
        for arb in arbs:
            print(arb)
    else:
        print("No arbs opportunity found")