def calculate_arbitrage_bet(odds1, odds2, stake_or_profit, value):
        # Calculate the implied probabilities
        prob1 = 1 / odds1
        prob2 = 1 / odds2

        # Check if arbitrage opportunity exists
        arbitrage_percentage = (prob1 + prob2) * 100
        if arbitrage_percentage >= 100:
            result = {'total_stake': 'N/A', 'bet1': 'N/A', 'bet2': 'N/A', 'actual_profit': 'N/A'}
            return result


        # Calculate the total stake for a desired profit
        if stake_or_profit == "profit":
            total_stake = value / (prob1 + prob2 - prob1 * prob2)
        elif stake_or_profit == "stake":
            # Calculate the required total stake for a specified profit
            total_stake = value / (1 - (1 / prob1 + 1 / prob2))

        # Calculate individual bet amounts
        bet1 = total_stake * prob2
        bet2 = total_stake * prob1

        # Calculate the actual profit
        actual_profit = total_stake - (bet1 + bet2)

        # Return the results
        return {
            "total_stake": total_stake,
            "bet1": bet1,
            "bet2": bet2,
            "actual_profit": actual_profit
        }


def arbitrage_calc(odds, total_stake):
    prob = [1 / odd for odd in odds]
    total_prob = sum(prob)

    stakes = [(total_stake * p / total_prob) for p in prob]
    winnings = [stake * odd for stake, odd in zip(stakes, odds)]
    guaranteed_profit = (total_stake / total_prob) - total_stake

    # stake1 = round(stakes[0], 2)
    # stake2 = round(stakes[1], 2)
    # return {
    #         "total_desired_stake": total_stake,
    #         "stake1": stake1,
    #         "stake1_winning": round(winnings[0]),
    #         "stake2": stake2,
    #         "stake2_winning": round(winnings[1]),

    #         "total_suggested_stake": stake1 + stake2,
    #         "guaranteed_profit": round(guaranteed_profit, 2)
    #     }
    return {
        f'stake{i + 1} for Bookmaker {i + 1} with odds {odds[i]}': round(stakes[i], 2)
        for i in range(len(odds))
    }, {
        f'winnings{i + 1}': round(winnings[i], 2)
        for i in range(len(odds))
    }, round(guaranteed_profit, 2)

v = arbitrage_calc([2.23, 1.61], 1000)
print(v)