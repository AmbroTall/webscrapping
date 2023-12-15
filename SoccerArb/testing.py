from typing import List
from prettytable import PrettyTable
import bet9ja, nairabet, betking, betwinner, merrybet, sunbet, sportybet, campeonbet, bet188
import bookmakereu, dafabet, marathonbet, sbobetSe, b365_Whill_Pinncl, betfairSe, coolbet, bovada


def arbitrage_calc(odds1, odds2, total_stake):
    # Calculate the implied probabilities of each outcome
    prob1 = 1 / odds1
    prob2 = 1 / odds2

    # Calculate the total implied probability
    total_prob = prob1 + prob2

    # Calculate the fair odds for each outcome
    fair_odds1 = prob1 / total_prob
    fair_odds2 = prob2 / total_prob

    # Calculate the stake for each outcome
    stake1 = (total_stake * fair_odds1) / (fair_odds1 + fair_odds2)
    stake2 = (total_stake * fair_odds2) / (fair_odds1 + fair_odds2)

    # Calculate the possible winnings for each outcome
    winnings1 = stake1 * odds1
    winnings2 = stake2 * odds2

    # Calculate the guaranteed profit
    guaranteed_profit = (total_stake / total_prob) - total_stake

    # Return the results as a dictionary
    return {f'stake1 for SportPesa with odds {odds1}': round(stake1, 2),
            f'stake2 for Odi with odds {odds2}': round(stake2, 2),
            'winnings1': round(winnings1, 2),
            'winnings2': round(winnings2, 2),
            'guaranteed_profit': round(guaranteed_profit, 2)}
def caller_function(odds_1_player_1,odds_1_player_2,odds_2_player_1,odds_2_player_2 ):
    odds_1_player_1 = float(odds_1_player_1)
    odds_1_player_2 = float(odds_1_player_2)
    odds_2_player_1 = float(odds_2_player_1)
    odds_2_player_2 = float(odds_2_player_2)
    # Arbitrage ccalcualculations
    prob_player_1_bookmaker_1 = 1 / odds_1_player_1
    prob_player_1_bookmaker_2 = 1 / odds_2_player_2
    total_prob_player_1 = prob_player_1_bookmaker_1 + prob_player_1_bookmaker_2

    # print("Prob 1", total_prob_player_1)
    prob_player_2_bookmaker_1 = 1 / odds_1_player_2
    prob_player_2_bookmaker_2 = 1 / odds_2_player_1
    total_prob_player_2 = prob_player_2_bookmaker_1 + prob_player_2_bookmaker_2

    # print("Prob 2", total_prob_player_2)

    arbitrage_margin_player_1 = 1 - total_prob_player_1
    arbitrage_margin_player_2 = 1 - total_prob_player_2

    if arbitrage_margin_player_2 > 0:
        # print("Arbitrage opportunity found!1")
        # print(f"Bookmaker 1 with odds {odds_1_player_2} || and Bookmaker 2 with odd {odds_2_player_1}")
        potential_profit = arbitrage_calc(odds_1_player_2, odds_2_player_1, 50000)
        # print("Potential profit: $", potential_profit)
        return potential_profit
    elif arbitrage_margin_player_1 > 0:
        # print("Arbitrage opportunity found!2")
        # print(f"Bookmaker 1 with odds {odds_1_player_1} || and Bookmaker 2 with odd {odds_2_player_2}")
        potential_profit = arbitrage_calc(odds_1_player_1, odds_2_player_2, 50000)
        # print("Potential profit: $", potential_profit)
        return potential_profit
    else:
        # print("No arbitrage opportunity")
        return "😢"

def merge_odds_lists(list1: List[dict], list2: List[dict]) -> str:
    merged_list = []
    for game1 in list1:
        for game2 in list2:
            # Compare using team names
            if (
                game1['home_team'] == game2['home_team']
                and game1['away_team'] == game2['away_team']
            ):
                merged_list.append({
                    'home_team1': game1['home_team'],
                    'away_team1': game1['away_team'],
                    'home_odds1': game1['home_odds'],
                    'away_odds1': game1['away_odds'],
                    'home_team2': game2['home_team'],
                    'away_team2': game2['away_team'],
                    'home_odds2': game2['home_odds'],
                    'away_odds2': game2['away_odds'],
                    'arbitrage': caller_function(
                        game1['home_odds'],
                        game1['away_odds'],
                        game2['home_odds'],
                        game2['away_odds']
                    )
                })

    table = PrettyTable()
    profits = 0
    rows = 0
    total_funds_sportpesa = 0
    total_funds_odi = 0
    table.field_names = ["SportPesa Home Team", "SportPesa Away Team", "SportPesa Home Odds",
                         "SportPesa Away Odds", "Odi Home Team", "Odi Away Team", "Odi Home Odds", "Odi Away Odds",
                         "Arbitrage"]
    print(len(merged_list))
    for row in merged_list:
        rows += 1

        print("This are the rows",row)
        print("This are the rows",row['arbitrage'])
        print("This are the rows",type(row['arbitrage']))
        # total_funds_sportpesa += float(row['arbitrage'][list(row['arbitrage'].keys())[0]])
        # total_funds_odi += float(row['arbitrage'][list(row['arbitrage'].keys())[1]])
        # profits += int(row['arbitrage']['guaranteed_profit'])
        table.add_row([row['home_team1'], row['away_team1'], row['home_odds1'], row['away_odds1'], row['home_team2'],
             row['away_team2'], row['home_odds2'], row['away_odds2'], row['arbitrage']])

    # stake = rows * 2000
    # print("******** Table Raws:", rows, "*********")
    # print("******** Total Stake/Spending:", stake, "*********")
    # print("******** Potential Income:", profits, "*********")
    # print("******** Potential Profits:", profits - stake, "*********")
    # print("******** Total Funds Sportpesa:", total_funds_sportpesa, "*********")
    # print("******** Total Funds Odi:", total_funds_odi, "*********")
    # print("******** Loss:", stake, "********* \n")
    return str(table)


bet9 = bet9ja.run_bet9ja_code()
bov = bovada.bovada_code()
print(bet9)
print("\n")
print("\n")
print("\n")
print(bov)

merged_list = merge_odds_lists(bov, bet9)
print("hello",merged_list)



