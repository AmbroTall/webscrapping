from itertools import product

def calculate_arbitrage(outcomes):
    total_implied_probability = sum(1 / odd for odd in outcomes)
    arbitrage_percentage = (1 - total_implied_probability) / total_implied_probability * 100
    return arbitrage_percentage, total_implied_probability

def find_best_combination(bookmaker_odds):
    best_combination = None
    best_arbitrage_percentage = 0

    num_bookmakers = len(bookmaker_odds)

    for home_index, draw_index, away_index in product(range(num_bookmakers), repeat=3):
        outcome_combination = [
            bookmaker_odds[home_index][0],
            bookmaker_odds[draw_index][1],
            bookmaker_odds[away_index][2]
        ]

        arbitrage_percentage, total_implied_probability = calculate_arbitrage(outcome_combination)

        if arbitrage_percentage > best_arbitrage_percentage:
            best_arbitrage_percentage = arbitrage_percentage
            best_combination = outcome_combination

            print(f"Combination: {outcome_combination}, Implied Probability: {total_implied_probability:.2f}%, Arbitrage Percentage: {arbitrage_percentage:.2f}%")

    return best_combination, best_arbitrage_percentage

# Example odds from 15 bookmakers for 1 X 2 outcomes
bookmaker_odds = [
    [2.0, 3.0, 4.0],   # Bookmaker 1
    # ... (rest of the bookmakers)
    [2.6, 3.2, 3.99],   # Bookmaker 15
    [2.5, 3.58, 3.33],   # Bookmaker 16
    [2.8, 3.92, 3.46],   # Bookmaker 17
]

best_combination, best_arbitrage_percentage = find_best_combination(bookmaker_odds)

print(f"Best Odds Combination: {best_combination}")
print(f"Best Arbitrage Percentage: {best_arbitrage_percentage:.2f}%")
