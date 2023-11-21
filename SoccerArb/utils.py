from db import soccer_leagues
import random
import json

#returns roi given two odds 1 2
def returnOnInvestment(odd1, odd2):
    odd1_percentage = 100/odd1
    odd2_percentage = 100/odd2
    sum = odd1_percentage + odd2_percentage
    roi = round(((100/sum)*100)-100, 2)
    return roi
#threeway roi 1 X 2
def returnOnInvestmentThreeway(odd1, odd2, odd3):
    if(odd2 == 0): odd2 = 1.00
    if(odd1 == 0): odd1 = 1.00
    if(odd3 == 0): odd3 = 1.00
    odd1_percentage = 100/odd1
    odd2_percentage = 100/odd2
    odd3_percentage = 100/odd3
    sum = odd1_percentage + odd2_percentage + odd3_percentage
    roi = round(((100/sum)*100)-100, 2)
    return roi
#returns how much to bet given a stake and two odds
def howMuchToBet(stake, odd1, odd2):
    odd1_percentage = 100/odd1
    odd2_percentage = 100/odd2
    sum = odd1_percentage + odd2_percentage
    stake1 = round((stake*odd1_percentage)/sum, 2)
    stake2 = round((stake*odd2_percentage)/sum, 2)
    profit = round((stake1*odd1)-stake, 2)
    return stake1, stake2, profit

def americanToDecimalOdds(american_odds):
    if(american_odds < 0):
        return abs(round((100/american_odds)-1, 2))
    return abs(round((american_odds/100)+1, 2))
def fractionalToDecimal(fractional_odds):
    if type(fractional_odds) == str:
        if(fractional_odds == "EVS"):
            return 1.01
        if(fractional_odds == " "):
            return 1.01
        numerator, denominator = map(int, fractional_odds.split('/'))
        decimal_odds = 1 + (numerator / denominator)
        return round(decimal_odds, 2)
    elif type(fractional_odds) == float:
        return round((1 + fractional_odds), 2)
#adjust coefficent based on betfair 5% comission on winning margin
def betfair_adjust_odd(odd):
    odd = float(odd)
    comission = 0.05 # 5%
    return round(odd - ((comission * odd) - comission), 2)
