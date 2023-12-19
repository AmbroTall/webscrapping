import json
import os

import schedule
import time
import json
from itertools import groupby, product, combinations
from operator import itemgetter
import concurrent.futures
import logging
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor

from parimatch import main as parimatch_main
from bet188 import main as bet188_main
from bet9ja import main as bet9ja_main
from ps3838 import main as ps3838_main
from betking import main as betking_main
from dafabet import main as dafabet_main
from nairabet import main as nairabet_main
from betbonanza import main as betbonanza_main
from sunbet import main as sunbet_main
from merrybet import main as merrybet_main
from sportybet import main as sportybet_main
from z22bet import main as z22bet_main
import smtplib
from email.mime.text import MIMEText
from tabulate import tabulate

# Create a list of all the main functions with their corresponding names
all_main_functions = {
    "bet9ja": bet9ja_main,
    "betbonanza": betbonanza_main,
    "sunbet": sunbet_main,
    "merrybet": merrybet_main,
    "sportybet": sportybet_main,
    "22bet": z22bet_main,
    "nairabet": nairabet_main,
    "dafabet": dafabet_main,
    "betking": betking_main,
    # "bet188": bet188_main,
    "ps3838": ps3838_main,
    "parimatch": parimatch_main,
}

sender_email = 'ambrosetall@gmail.com'
receiver_emails = ['ndoneambrose@gmail.com', ]


def send_mail(email, table_data):
    print("Sending mails")
    # Assuming you have an SMTP server and credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Update with your SMTP server port
    smtp_username = 'ambrosetall@gmail.com'
    smtp_password = "efinnhdzinwpshjm"

    # Sender and recipient email addresses
    sender_email = "ambrosetall@gmail.com"
    recipient_emails = email

    # Create the email message
    subject = 'Sure Bet Odds'
    body = tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid")
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_emails)  # Join the list of emails with commas

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use TLS encryption
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_emails, message.as_string())
    print("Email Sent Successfully")

def delete_jwt_file(file_path='jwt_token.txt'):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted {file_path}")
def fetch_all_matches(all_main_functions, max_execution_time=500, max_retries=5):
    results = {}

    def execute_function(name, func):
        try:
            result = func()
            return name, result
        except Exception as e:
            logging.error(f"Function {name} failed with exception: {e}")
            return name, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(all_main_functions)) as executor:
        futures = {name: executor.submit(execute_function, name, func) for name, func in all_main_functions.items()}

        for retry in range(max_retries):
            for name, future in futures.items():
                try:
                    name, result = future.result(timeout=max_execution_time)
                    if result is not None:
                        results[name] = result
                except concurrent.futures.TimeoutError:
                    logging.warning(f"Function {name} timed out. Restarting... (Retry {retry + 1}/{max_retries})")
                    future.cancel()
                    restarted_future = executor.submit(execute_function, name, all_main_functions[name])
                    futures[name] = restarted_future

        executor.shutdown(wait=True)

    return results


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
    best_arbitrage = None
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

            current_arbitrage = {
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
            }

            if best_arbitrage is None or current_arbitrage["guaranteed_profit"] > best_arbitrage["guaranteed_profit"]:
                best_arbitrage = current_arbitrage

    return best_arbitrage


# def find_arbitrage_combinations(bookmaker_data, min_profit_percentage=0, fixed_stake=1000):
#     arbitrage_combinations = []
#
#     num_bookmakers = len(bookmaker_data)
#
#     for home_index, draw_index, away_index in product(range(num_bookmakers), repeat=3):
#         home_bookie = bookmaker_data[home_index]["bookname"]
#         draw_bookie = bookmaker_data[draw_index]["bookname"]
#         away_bookie = bookmaker_data[away_index]["bookname"]
#         home_team = bookmaker_data[home_index]["home_team"]
#         away_team = bookmaker_data[away_index]["away_team"]
#
#         outcome_combination = [
#             bookmaker_data[home_index]["odds"][0],
#             bookmaker_data[draw_index]["odds"][1],
#             bookmaker_data[away_index]["odds"][2]
#         ]
#
#         arbitrage_percentage, total_implied_probability = calculate_arbitrage(outcome_combination)
#
#         if arbitrage_percentage > min_profit_percentage:
#             stakes_distribution, winnings, guaranteed_profit = arbitrage_calc(outcome_combination, fixed_stake)
#
#             arbitrage_combinations.append({
#                 "event": bookmaker_data[home_index]["event"],  # Add the event field here
#                 "home_bookie": home_bookie,
#                 "draw_bookie": draw_bookie,
#                 "away_bookie": away_bookie,
#                 "home_team": home_team,
#                 "away_team": away_team,
#                 "combination": outcome_combination,
#                 "implied_probability": total_implied_probability,
#                 "arbitrage_percentage": arbitrage_percentage,
#                 "stakes_distribution": stakes_distribution,
#                 "winnings": winnings,
#                 "guaranteed_profit": guaranteed_profit
#             })
#
#     return arbitrage_combinations


def find_arbitrage_combinations(bookmaker_data, min_profit_percentage=0, fixed_stake=1000):
    best_arbitrage = None

    num_bookmakers = len(bookmaker_data)

    for home_index, draw_index, away_index in product(range(num_bookmakers), repeat=3):
        home_bookie = bookmaker_data[home_index]["bookname"]
        draw_bookie = bookmaker_data[draw_index]["bookname"]
        away_bookie = bookmaker_data[away_index]["bookname"]
        home_team = bookmaker_data[home_index]["home_team"]
        away_team = bookmaker_data[away_index]["away_team"]

        outcome_combination = [
            bookmaker_data[home_index]["odds"][0],
            bookmaker_data[draw_index]["odds"][1],
            bookmaker_data[away_index]["odds"][2]
        ]

        arbitrage_percentage, total_implied_probability = calculate_arbitrage(outcome_combination)

        if arbitrage_percentage > min_profit_percentage:
            stakes_distribution, winnings, guaranteed_profit = arbitrage_calc(outcome_combination, fixed_stake)

            current_arbitrage = {
                "event": bookmaker_data[home_index]["event"],  # Add the event field here
                "home_bookie": home_bookie,
                "draw_bookie": draw_bookie,
                "away_bookie": away_bookie,
                "home_team": home_team,
                "away_team": away_team,
                "combination": outcome_combination,
                "implied_probability": total_implied_probability,
                "arbitrage_percentage": arbitrage_percentage,
                "stakes_distribution": stakes_distribution,
                "winnings": winnings,
                "guaranteed_profit": guaranteed_profit
            }

            if best_arbitrage is None or current_arbitrage["guaranteed_profit"] > best_arbitrage["guaranteed_profit"]:
                best_arbitrage = current_arbitrage

    return best_arbitrage


def prepare_matches_calc_arbs(results):
    testing = []
    home_draw_win = []
    draw_no_bet = []
    double_chance = []
    over_one_five = []
    over_two_five = []
    over_three_five = []
    fasthalf1X2 = []
    gg = []
    away2_home1X = []
    home1_awayX2 = []
    X_away12 = []

    draw_no_bet_first_half = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_four_five = []
    over_five_five = []
    fasthalf_dc = []

    gg_firsthalf = []
    odd_even = []
    odd_even_firsthalf = []
    first_team_to_score = []  # hometeam, draw, away_team
    home_team_overunder15 = []
    home_team_overunder25 = []
    home_team_overunder05 = []
    away_team_overunder15 = []
    away_team_overunder25 = []
    away_team_overunder05 = []

    # Now all_arbitrage_results contains the data from the JSON file
    for key, value in results.items():
        bookie_name = key
        leagues = value
        for league in leagues:
            league_name, values = next(iter(league.items()))
            for key_league, value_matches in league.items():
                matches = value_matches
                for match in matches:
                    # print(match)
                    home_team = match['home_team']
                    away_team = match['away_team']
                    # time = match['time']
                    wager_types = match['wager_types']
                    for wager in wager_types:
                        # print(wager)
                        key, values = next(iter(wager.items()))
                        if key == "1X2":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_draw_win.append(match_data)

                            # match_data2 = {}
                            # match_data2['bookname'] = bookie_name
                            # match_data2['league'] = league_name
                            # match_data2['event'] = key
                            # match_data2['home_team'] = home_team
                            # match_data2['away_team'] = away_team
                            # match_data2['odds'] = [values[0], values[-1]]
                            # testing.append(match_data2)
                        if key == "draw_no_bet":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            draw_no_bet.append(match_data)
                        if key == "double_chance":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            double_chance.append(match_data)
                        if key == "over_one_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_one_five.append(match_data)
                        if key == "over_two_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_two_five.append(match_data)
                        if key == "over_three_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_three_five.append(match_data)
                        if key == "fasthalf1X2":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            fasthalf1X2.append(match_data)
                        if key == "gg":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            gg.append(match_data)
                        if key == "21X":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away2_home1X.append(match_data)
                        if key == "12X":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home1_awayX2.append(match_data)
                        if key == "X12":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            X_away12.append(match_data)
                        if key == "draw_no_bet_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            draw_no_bet_first_half.append(match_data)
                        if key == "over_ofive_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five.append(match_data)
                        if key == "over_ofive_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five_first_half.append(match_data)
                        if key == "over_one_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_one_five_first_half.append(match_data)
                        if key == "over_two_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_two_five_first_half.append(match_data)
                        if key == "over_four_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_four_five.append(match_data)
                        if key == "over_five_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_five_five.append(match_data)
                        if key == "fasthalf_dc":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            fasthalf_dc.append(match_data)
                        if key == "gg_firsthalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            gg_firsthalf.append(match_data)
                        if key == "odd_even":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            odd_even.append(match_data)
                        if key == "odd_even_firsthalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            odd_even_firsthalf.append(match_data)
                        if key == "first_team_to_score":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_team_to_score.append(match_data)
                        if key == "home_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder15.append(match_data)
                        if key == "home_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder25.append(match_data)
                        if key == "home_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder05.append(match_data)
                        if key == "away_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder15.append(match_data)
                        if key == "away_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder25.append(match_data)
                        if key == "away_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder05.append(match_data)

    return testing, home_draw_win, draw_no_bet, double_chance, over_one_five, over_two_five, over_three_five, fasthalf1X2, gg, away2_home1X, home1_awayX2, X_away12, draw_no_bet_first_half, over_ofive_five, over_ofive_five_first_half, over_one_five_first_half, over_two_five_first_half, over_four_five, over_five_five, fasthalf_dc, gg_firsthalf, odd_even, odd_even_firsthalf, first_team_to_score, home_team_overunder15, home_team_overunder25, home_team_overunder05, away_team_overunder15, away_team_overunder25, away_team_overunder05


def group_teams_matches(matches_lists, wager_type):
    # Sort the list based on home and away team names
    matches_lists.sort(key=itemgetter('home_team', 'away_team', 'league'))
    arbs_opportunities = []
    games = []
    # Group matches by home and away team names
    grouped_matches = {key: list(group) for key, group in
                       groupby(matches_lists, key=itemgetter('home_team', 'away_team', 'league'))}
    # Iterate over groups and calculate arbitrage
    grouped_matches.items()
    for key, matches in grouped_matches.items():
        # +++++ Debugging +++++
        games.append(matches)
        min_profit_percentage = 0
        fixed_stake = 1000
        print(f"Key : {key} Match : {len(matches)} {matches}")
        try:
            arb = None
            if wager_type == "three_way":
                arb = find_arbitrage_combinations(matches, min_profit_percentage, fixed_stake)
            elif wager_type == "two_way":
                arb = find_arbitrage_combinations_two_way(matches, min_profit_percentage, fixed_stake)
            if arb:
                arbs_opportunities.append(arb)
                if "home" in arb['home_team'].lower() or "away" in arb['away_team'].lower():
                    continue
                if wager_type == "three_way":
                    table_data = [
                        ["Event", arb['event']],
                        ["Home Bookie", arb['home_bookie']],
                        ["Draw Bookie", arb['draw_bookie']],
                        ["Away Bookie", arb['away_bookie']],
                        ["Home Team", arb['home_team']],
                        ["Away Team", arb['away_team']],
                        ["Combination", arb['combination']],
                        ["Implied Probability", f"{arb['implied_probability']:.2f}%"],
                        ["Arbitrage Percentage", f"{arb['arbitrage_percentage']:.2f}%"],
                        ["Stakes Distribution", arb['stakes_distribution']],
                        ["Winnings", arb['winnings']],
                        ["Guaranteed Profit", arb['guaranteed_profit']],
                    ]
                    print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
                    save_arbs(arb, table_data)
                    # Add a separator line between each combination
                    print("\n" + "-" * 40 + "\n")
                elif wager_type == "two_way":
                    table_data = [
                        ["Event", arb['event']],
                        ["Home Bookie", arb['home_bookie']],
                        ["Away Bookie", arb['away_bookie']],
                        ["Home Team", arb['home_team']],
                        ["Away Team", arb['away_team']],
                        ["Combination", arb['combination']],
                        ["Implied Probability", f"{arb['implied_probability']:.2f}%"],
                        ["Arbitrage Percentage", f"{arb['arbitrage_percentage']:.2f}%"],
                        ["Stakes Distribution", arb['stakes_distribution']],
                        ["Winnings", arb['winnings']],
                        ["Guaranteed Profit", arb['guaranteed_profit']],
                    ]
                    save_arbs(arb, table_data)
                    print(tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid"))
                    # Add a separator line between each combination
                    print("\n" + "-" * 40 + "\n")
            else:
                print("No Arbs")
        except:
            print("Error in calculating arbs")
            continue

    return games, arbs_opportunities


def is_arbitrage_data_unique(existing_data, new_arbitrage_data):
    # Check if the combination of event, home_team, away_team, and implied_probability already exists
    for data in existing_data:
        if (
                data['event'] == new_arbitrage_data['event'] and
                data['home_team'] == new_arbitrage_data['home_team'] and
                data['away_team'] == new_arbitrage_data['away_team'] and
                data['implied_probability'] == new_arbitrage_data['implied_probability']
        ):
            return False
    return True


# Save Arbs And Send Mail If arb is unique
def save_arbs(arbitrage_data, table_data):
    json_filename = "arbs.json"
    # Create a new JSON file if it doesn't exist
    if not os.path.exists(json_filename):
        with open(json_filename, 'w') as json_file:
            json.dump([], json_file)

        # Load existing data from the JSON file
    with open(json_filename, 'r') as json_file:
        existing_data = json.load(json_file)

        # Check if the new arbitrage data is unique
    if is_arbitrage_data_unique(existing_data, arbitrage_data):
        send_mail(receiver_emails, table_data)
        # Append the new arbitrage data
        existing_data.append(arbitrage_data)
        # Write the updated data back to the JSON file
        with open(json_filename, 'w') as json_file:
            json.dump(existing_data, json_file)
    else:
        print("Arbitrage data already exists. Not saving.")


def fetch_all_matches_job():
    results = fetch_all_matches(all_main_functions)
    return results


def main():
    results = None
    # Delete the JWT file when needed
    delete_jwt_file()
    # Define the job to fetch all matches
    def fetch_all_matches_and_update_results():
        # Access the outer (nonlocal) results variable
        nonlocal results
        results = fetch_all_matches_job()

    # Schedule the job every 8 minutes
    schedule.every(6).minutes.do(fetch_all_matches_and_update_results)

    while True:
        # Run pending scheduled jobs
        schedule.run_pending()

        # Record start time
        start_time = time.time()

        # Fetch all matches
        fetch_all_matches_and_update_results()

        # TESTING DATA
        # results = fetch_all_matches(all_main_functions)
        # json_filename = 'arbitrage_results.json'
        # Save the combined data back to the JSON file
        # with open(json_filename, 'r') as json_file:
        #     results = json.load(json_file)
        # Save the results to the JSON file
        # with open(json_filename, 'w') as json_file:
        #     json.dump(results, json_file)

        testing, home_draw_win, draw_no_bet, double_chance, over_one_five, over_two_five, over_three_five, fasthalf1X2, gg, away2_home1X, home1_awayX2, X_away12, draw_no_bet_first_half, over_ofive_five, over_ofive_five_first_half, over_one_five_first_half, over_two_five_first_half, over_four_five, over_five_five, fasthalf_dc, gg_firsthalf, odd_even, odd_even_firsthalf, first_team_to_score, home_team_overunder15, home_team_overunder25, home_team_overunder05, away_team_overunder15, away_team_overunder25, away_team_overunder05 = prepare_matches_calc_arbs(results)
        calculate_arbs = {"3_way_arbs": [home_draw_win, double_chance,first_team_to_score, fasthalf1X2,fasthalf_dc],
                          "2_way_arbs": [over_ofive_five, away_team_overunder05,home_team_overunder15,away_team_overunder25, away_team_overunder15,  home_team_overunder05, home_team_overunder25, odd_even_firsthalf, odd_even,gg_firsthalf, over_five_five,over_four_five, over_two_five_first_half, over_one_five_first_half, over_ofive_five_first_half, draw_no_bet, draw_no_bet_first_half, over_three_five, over_two_five, over_one_five, gg, away2_home1X,
                                         home1_awayX2, X_away12]}

        for key, value in calculate_arbs.items():
            if key == "3_way_arbs":
                # print(value)
                for x in value:
                    try:
                        games, arbs_opportunities = group_teams_matches(x, "three_way")
                        print(arbs_opportunities)
                    except:
                        continue
            if key == "2_way_arbs":
                for x in value:
                    try:
                        games, arbs_opportunities = group_teams_matches(x, "two_way")
                        print(arbs_opportunities)
                    except:
                        continue

        # Record end time
        end_time = time.time()

        # Calculate elapsed timefind_arbitrage_combinations
        elapsed_time = end_time - start_time
        print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        time.sleep(90)


if __name__ == '__main__':
    main()
    # Get the keys
