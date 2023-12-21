from itertools import combinations


def calculate_arbitrage(outcomes):
    total_implied_probability = sum(1 / odd for odd in outcomes)
    arbitrage_percentage = (1 - total_implied_probability) / total_implied_probability * 100
    return arbitrage_percentage, total_implied_probability

def arbitrage_calc(odds, total_stake):
    prob = [1 / odd for odd in odds]
    total_prob = sum(prob)

    stakes = [(total_stake * p / total_prob) for p in prob]
    winnings = [stake * odd for stake, odd in zip(stakes, odds)]
    guaranteed_profit = (total_stake / total_prob) - total_stake

    return {
        f'stake{i + 1} for Bookmaker {i + 1} with odds {odds[i]}': round(stakes[i], 2)
        for i in range(len(odds))
    }, {
        f'winnings{i + 1}': round(winnings[i], 2)
        for i in range(len(odds))
    }, round(guaranteed_profit, 2)

def find_arbitrage_combinations_two_way(bookmaker_data, min_profit_percentage=0, fixed_stake=1000):
    arbitrage_combinations = []

    num_bookmakers = len(bookmaker_data)

    for home_index, away_index in combinations(range(num_bookmakers), 2):
        home_bookie = bookmaker_data[home_index]["bookname"]
        away_bookie = bookmaker_data[away_index]["bookname"]
        home_team = bookmaker_data[home_index]["home_team"]
        away_team = bookmaker_data[away_index]["away_team"]

        # Changed the combination to use the first and last odds
        outcome_combination = [
            bookmaker_data[home_index]["odds"][0],
            bookmaker_data[away_index]["odds"][1]
        ]

        arbitrage_percentage, total_implied_probability = calculate_arbitrage(outcome_combination)

        if arbitrage_percentage > min_profit_percentage:
            stakes_distribution, winnings, guaranteed_profit = arbitrage_calc(outcome_combination, fixed_stake)

            arbitrage_combinations.append({
                "event": bookmaker_data[home_index]["event"],
                "home_bookie": home_bookie,
                "away_bookie": away_bookie,
                "home_team": home_team,
                "away_team": away_team,
                "combination": outcome_combination,
                "implied_probability": total_implied_probability,
                "arbitrage_percentage": arbitrage_percentage,
                "stakes_distribution": stakes_distribution,
                "winnings": winnings,
                "guaranteed_profit": guaranteed_profit
            })

    return arbitrage_combinations


