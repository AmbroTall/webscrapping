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
    # Arbitrage calculations
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

odds_1_player_1 = 2.13
odds_1_player_2 = 1.68
odds_2_player_1 = 1.96
odds_2_player_2 = 1.77



print(caller_function(odds_1_player_1, odds_1_player_2, odds_2_player_1, odds_2_player_2))
