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

keys_array = [
    "England Premier League",
    "England Championship",
    "England League One",
    "England League Two",
    "Scotland Premiership",
    "Scotland Championship",
    "Scotland League One",
    "Scotland League Two",
    "Irish Premier",
    "Northern Ireland",
    "France League One",
    "France League Two",
    "Laliga",
    "Copa del Ray",
    "Laliga 2",
    "German Bundesliga",
    "German Bundesliga 2",
    "German Bundesliga 3",
    "German DFB Pokal",
    "Italy Serie A",
    "Italy Serie B",
    "Italy Coppa Italia",
    "Netherlands Eredivisie",
    "Netherlands Erste Division",
    "Czech Liga 1",
    "Greece Super League 1",
    "Swedish Allsvenska",
    "Superatten",
    "Danish Superligan",
    "England FA",
]

def fetch_all_matches_for_league(all_main_functions, league_key, max_execution_time=1000, max_retries=5):
    results_for_league = {}
    def execute_function(name, func, key):
        try:
            result = func(key)
            return name, result
        except Exception as e:
            logging.error(f"Function {name} failed with exception: {e}")
            return name, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(all_main_functions)) as executor:
        futures = {name: executor.submit(execute_function, name, func, key) for name, func in all_main_functions.items() for key in keys_array if key.startswith(league_key)}

        for retry in range(max_retries):
            for name, future in futures.items():
                try:
                    name, result = future.result(timeout=max_execution_time)
                    if result is not None:
                        results_for_league[name] = result
                except concurrent.futures.TimeoutError:
                    logging.warning(f"Function {name} timed out. Restarting... (Retry {retry + 1}/{max_retries})")
                    future.cancel()
                    key = next((k for k in keys_array if k.startswith(league_key)), None)
                    if key:
                        restarted_future = executor.submit(execute_function, name, all_main_functions[name], key)
                        futures[name] = restarted_future

        executor.shutdown(wait=True)

    return results_for_league

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
    # # "bet188": bet188_main,
    # # "ps3838": ps3838_main,
    # "parimatch": parimatch_main,
}

sender_email = 'ambrosetall@gmail.com'
receiver_emails = ['ndoneambrose@gmail.com', 'd']


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
    handicap1 = []  # -1.5 / 1.5
    over_one_five = []
    over_two_five = []
    over_three_five = []
    fasthalf1X2 = []
    gg = []

    draw_no_bet_first_half = []
    draw_no_bet_second_half = []
    over_ofive_five = []
    over_ofive_five_first_half = []
    over_one_five_first_half = []
    over_two_five_first_half = []
    over_ofive_five_second_half = []
    over_one_five_second_half = []
    over_two_five_second_half = []
    away2_home1X = []
    home1_awayX2 = []
    X_away12 = []
    over_four_five = []
    over_five_five = []
    fasthalf_dc = []
    secondhalf_dc = []
    gg_firsthalf = []
    gg_secondhalf = []
    odd_even = []
    odd_even_firsthalf = []
    odd_even_secondhalf = []
    hometeam_odd_even = []
    awayteam_odd_even = []
    first_team_to_score = []  # hometeam, draw, away_team
    first_team_to_score_1st_half = []  # hometeam, draw, away_team
    first_team_to_score_2nd_half = []  # hometeam, draw, away_team
    last_team_to_score = []  # hometeam, draw, away_team
    home_team_overunder15 = []
    home_team_overunder25 = []
    home_team_overunder05 = []
    away_team_overunder15 = []
    away_team_overunder25 = []
    away_team_overunder05 = []
    home_clean_sheet = []
    away_clean_sheet = []
    home_clean_sheet_first_half = []
    away_clean_sheet_first_half = []
    home_clean_sheet_second_half = []
    away_clean_sheet_second_half = []
    first_half_home_team_overunder15 = []
    first_half_home_team_overunder25 = []
    first_half_home_team_overunder05 = []
    first_half_away_team_overunder15 = []
    first_half_away_team_overunder25 = []
    first_half_away_team_overunder05 = []

    second_half_home_team_overunder15 = []
    second_half_home_team_overunder25 = []
    second_half_home_team_overunder05 = []
    second_half_away_team_overunder15 = []
    second_half_away_team_overunder25 = []
    second_half_away_team_overunder05 = []
    second1X2 = []

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
                    if match['time'] > 1000000000000:
                        # Assuming the timestamp is in milliseconds, convert it to seconds
                        time /= 1000
                    else:
                        time = match['time']
                    wager_types = match['wager_types']
                    for wager in wager_types:
                        # print(wager)
                        key, values = next(iter(wager.items()))
                        if key == "1X2":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_draw_win.append(match_data)

                            match_data2 = {}
                            match_data2['bookname'] = bookie_name
                            match_data2['league'] = league_name
                            match_data2['event'] = key
                            match_data2['time'] = time
                            match_data2['home_team'] = home_team
                            match_data2['away_team'] = away_team
                            match_data2['odds'] = [values[0], values[-1]]
                            testing.append(match_data2)
                            print(match_data2)
                        if key == "draw_no_bet":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            draw_no_bet.append(match_data)
                        if key == "double_chance":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            double_chance.append(match_data)
                        if key == "over_one_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_one_five.append(match_data)
                        if key == "over_two_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_two_five.append(match_data)
                        if key == "over_three_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_three_five.append(match_data)
                        if key == "fasthalf1X2":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            fasthalf1X2.append(match_data)
                        if key == "gg":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            gg.append(match_data)
                        if key == "21X":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away2_home1X.append(match_data)
                        if key == "12X":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home1_awayX2.append(match_data)
                        if key == "X12":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            X_away12.append(match_data)
                        if key == "draw_no_bet_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            draw_no_bet_first_half.append(match_data)
                        if key == "draw_no_bet_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            draw_no_bet_second_half.append(match_data)
                        if key == "over_ofive_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five.append(match_data)
                        if key == "over_ofive_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five_first_half.append(match_data)
                        if key == "over_one_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_one_five_first_half.append(match_data)
                        if key == "over_two_five_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_two_five_first_half.append(match_data)
                        if key == "over_four_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_four_five.append(match_data)
                        if key == "over_five_five":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_five_five.append(match_data)
                        if key == "fasthalf_dc":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            fasthalf_dc.append(match_data)
                        if key == "gg_firsthalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            gg_firsthalf.append(match_data)
                        if key == "odd_even":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            odd_even.append(match_data)
                        if key == "odd_even_firsthalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            odd_even_firsthalf.append(match_data)
                        if key == "first_team_to_score":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_team_to_score.append(match_data)
                        if key == "home_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder15.append(match_data)
                        if key == "home_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder25.append(match_data)
                        if key == "home_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_team_overunder05.append(match_data)
                        if key == "away_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder15.append(match_data)
                        if key == "away_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder25.append(match_data)
                        if key == "away_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_team_overunder05.append(match_data)
                        if key == "over_ofive_five_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five_second_half.append(match_data)

                        if key == "over_ofive_five_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_ofive_five_second_half.append(match_data)

                        if key == "over_one_five_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_one_five_second_half.append(match_data)
                        if key == "over_two_five_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            over_two_five_second_half.append(match_data)
                        if key == "secondhalf_dc":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            secondhalf_dc.append(match_data)
                        if key == "gg_secondhalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            gg_secondhalf.append(match_data)
                        if key == "odd_even_secondhalf":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            odd_even_secondhalf.append(match_data)
                        if key == "hometeam_odd_even":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            hometeam_odd_even.append(match_data)
                        if key == "awayteam_odd_even":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            awayteam_odd_even.append(match_data)
                        if key == "first_team_to_score_1st_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_team_to_score_1st_half.append(match_data)
                        if key == "first_team_to_score_2nd_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_team_to_score_2nd_half.append(match_data)
                        if key == "last_team_to_score":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            last_team_to_score.append(match_data)
                        if key == "home_clean_sheet":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_clean_sheet.append(match_data)
                        if key == "home_clean_sheet":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_clean_sheet.append(match_data)
                        if key == "away_clean_sheet":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_clean_sheet.append(match_data)
                        if key == "home_clean_sheet_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_clean_sheet_first_half.append(match_data)
                        if key == "away_clean_sheet_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_clean_sheet_first_half.append(match_data)
                        if key == "away_clean_sheet_first_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_clean_sheet_first_half.append(match_data)
                        if key == "home_clean_sheet_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            home_clean_sheet_second_half.append(match_data)
                        if key == "away_clean_sheet_second_half":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            away_clean_sheet_second_half.append(match_data)
                        if key == "first_half_home_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_home_team_overunder15.append(match_data)
                        if key == "first_half_home_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_home_team_overunder25.append(match_data)
                        if key == "first_half_home_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_home_team_overunder05.append(match_data)
                        if key == "first_half_away_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_away_team_overunder15.append(match_data)
                        if key == "first_half_away_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_away_team_overunder25.append(match_data)
                        if key == "first_half_away_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            first_half_away_team_overunder05.append(match_data)
                        if key == "second_half_home_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_home_team_overunder15.append(match_data)

                        if key == "second_half_home_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_home_team_overunder25.append(match_data)
                        if key == "second_half_home_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_home_team_overunder05.append(match_data)
                        if key == "second_half_away_team_overunder15":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_away_team_overunder15.append(match_data)
                        if key == "second_half_away_team_overunder25":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_away_team_overunder25.append(match_data)

                        if key == "second_half_away_team_overunder05":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second_half_away_team_overunder05.append(match_data)

                        if key == "second1X2":
                            match_data = {}
                            match_data['bookname'] = bookie_name
                            match_data['league'] = league_name
                            match_data['event'] = key
                            match_data['time'] = time
                            match_data['home_team'] = home_team
                            match_data['away_team'] = away_team
                            match_data['odds'] = values
                            second1X2.append(match_data)

    return testing, awayteam_odd_even,hometeam_odd_even, second_half_away_team_overunder05, second1X2,home_clean_sheet_second_half,second_half_away_team_overunder25, second_half_away_team_overunder15,second_half_home_team_overunder25,second_half_home_team_overunder05, second_half_home_team_overunder15,first_half_away_team_overunder05,first_half_away_team_overunder25,first_half_home_team_overunder05,first_half_away_team_overunder15, first_half_home_team_overunder25,first_half_home_team_overunder15,away_clean_sheet_second_half, over_ofive_five_second_half,away_clean_sheet_first_half,home_clean_sheet_first_half, away_clean_sheet,home_clean_sheet,last_team_to_score,first_team_to_score_2nd_half,first_team_to_score_1st_half,odd_even_secondhalf,gg_secondhalf,secondhalf_dc,over_two_five_second_half,over_one_five_second_half,draw_no_bet_second_half,home_draw_win, draw_no_bet, double_chance, over_one_five, over_two_five, over_three_five, fasthalf1X2, gg, away2_home1X, home1_awayX2, X_away12, draw_no_bet_first_half, over_ofive_five, over_ofive_five_first_half, over_one_five_first_half, over_two_five_first_half, over_four_five, over_five_five, fasthalf_dc, gg_firsthalf, odd_even, odd_even_firsthalf, first_team_to_score, home_team_overunder15, home_team_overunder25, home_team_overunder05, away_team_overunder15, away_team_overunder25, away_team_overunder05

def split_and_sort_team_names(team_name):
    return sorted(team_name.lower().split(), key=len, reverse=True)

def match_team_names(name1, name2):
    # Define keywords to exclude from matching
    exclusion_keywords = ["fc", "f.c","city","united","utd"]

    # Split and sort team names
    names1 = split_and_sort_team_names(name1)
    names2 = split_and_sort_team_names(name2)

    # Check if any words from home team match with any words from away team, excluding certain keywords
    return any(word1 == word2 for word1 in names1 for word2 in names2 if word1.lower() not in exclusion_keywords and word2.lower() not in exclusion_keywords)

def group_teams_matches(matches_lists, wager_type):
    matches_lists.sort(key=itemgetter('time', 'home_team', 'away_team', 'league'))
    arbs_opportunities = []
    games = []
    # Group matches by time, home_name, and away_name
    grouped_matches = {}
    current_key = None
    current_group = []

    # print(matches_lists)
    for match in matches_lists:

        match_key = (match['time'], match['home_team'], match['away_team'])

        if current_key is None or match_team_names(match_key[1], current_key[1]) and match_team_names(match_key[2], current_key[2]):
            current_group.append(match)
        else:
            grouped_matches[current_key] = current_group
            current_group = [match]

        current_key = match_key

    if current_group:
        grouped_matches[current_key] = current_group

    for key, matchess in grouped_matches.items():
        # +++++ Debugging +++++
        matches = [match for match in matchess if match['odds']]

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
                if wager_type == "three_way" and arb['home_bookie'] != arb['draw_bookie'] != arb['away_bookie']:
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
                    if arb['arbitrage_percentage'] > 2:
                        save_arbs(arb, table_data)
                    # Add a separator line between each combination
                    print("\n" + "-" * 40 + "\n")
                elif wager_type == "two_way" and arb['home_bookie'] != arb['away_bookie']:
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
                    if arb['arbitrage_percentage'] > 2:
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

# def main():
#     print("Ambrose")
#     while True:
#         # Loop over each league in keys_array and fetch results concurrently
#         for league_key in keys_array:
#             try:
#                 # Record start time
#                 start_time = time.time()
#                 
#                 # Fetch All Matches
#                 results = fetch_all_matches_for_league(all_main_functions, league_key)
#                 # print(f"Results for {league_key}: {results}")
# 
#                 # TESTING DATA
#                 # json_filename = 'arbitrage_main2_results.json'
#                 # # Save the combined data back to the JSON file
#                 # with open(json_filename, 'r') as json_file:
#                 #     results = json.load(json_file)
#                 # Save the results to the JSON file
#                 # with open(json_filename, 'w') as json_file:
#                 #     json.dump(results, json_file)
# 
#                 testing,awayteam_odd_even,hometeam_odd_even, second_half_away_team_overunder05, second1X2, home_clean_sheet_second_half, second_half_away_team_overunder25, second_half_away_team_overunder15, second_half_home_team_overunder25, second_half_home_team_overunder05, second_half_home_team_overunder15, first_half_away_team_overunder05, first_half_away_team_overunder25, first_half_home_team_overunder05, first_half_away_team_overunder15, first_half_home_team_overunder25, first_half_home_team_overunder15, away_clean_sheet_second_half, over_ofive_five_second_half, away_clean_sheet_first_half, home_clean_sheet_first_half, away_clean_sheet, home_clean_sheet, last_team_to_score, first_team_to_score_2nd_half, first_team_to_score_1st_half, odd_even_secondhalf, gg_secondhalf, secondhalf_dc, over_two_five_second_half, over_one_five_second_half, draw_no_bet_second_half, home_draw_win, draw_no_bet, double_chance, over_one_five, over_two_five, over_three_five, fasthalf1X2, gg, away2_home1X, home1_awayX2, X_away12, draw_no_bet_first_half, over_ofive_five, over_ofive_five_first_half, over_one_five_first_half, over_two_five_first_half, over_four_five, over_five_five, fasthalf_dc, gg_firsthalf, odd_even, odd_even_firsthalf, first_team_to_score, home_team_overunder15, home_team_overunder25, home_team_overunder05, away_team_overunder15, away_team_overunder25, away_team_overunder05= prepare_matches_calc_arbs(results)
#                 print(f"\n\n This is my testing {testing} \n\n")
#                 calculate_arbs = {"3_way_arbs": [home_draw_win, double_chance,first_team_to_score, fasthalf1X2,fasthalf_dc,first_team_to_score,first_team_to_score_1st_half,first_team_to_score_2nd_half,second1X2,last_team_to_score, fasthalf_dc,secondhalf_dc ],
#                                   "2_way_arbs": [over_ofive_five,away_team_overunder25,away_team_overunder15,away_team_overunder05,home_clean_sheet, first_half_away_team_overunder15,first_half_home_team_overunder05,first_half_home_team_overunder25, first_half_home_team_overunder15,away_clean_sheet_second_half, home_clean_sheet_second_half,away_clean_sheet, home_clean_sheet,home_clean_sheet_first_half,away_clean_sheet_first_half,first_half_away_team_overunder25,first_half_away_team_overunder05, second_half_away_team_overunder05,second_half_away_team_overunder25, second_half_away_team_overunder15,second_half_home_team_overunder05,second_half_home_team_overunder25, second_half_home_team_overunder15,away_team_overunder05,home_team_overunder15,away_team_overunder25, away_team_overunder15,  home_team_overunder05, home_team_overunder25, odd_even_firsthalf, odd_even,gg_firsthalf, over_five_five,over_four_five, over_two_five_first_half, over_one_five_first_half, over_ofive_five_first_half, draw_no_bet, draw_no_bet_first_half, over_three_five, over_two_five, over_one_five, gg, away2_home1X,
#                                                  home1_awayX2, X_away12, home_team_overunder05,home_team_overunder25,home_team_overunder15,awayteam_odd_even,hometeam_odd_even,odd_even_secondhalf,odd_even_firsthalf,odd_even,gg_secondhalf,gg_firsthalf,over_two_five_second_half,over_one_five_second_half, over_ofive_five_second_half,over_two_five_first_half,over_one_five_first_half,over_ofive_five_first_half,over_ofive_five, draw_no_bet_second_half,draw_no_bet_first_half, ]}
# 
#                 for key, value in calculate_arbs.items():
#                     if key == "3_way_arbs":
#                         # print(value)
#                         for x in value:
#                             try:
#                                 games, arbs_opportunities = group_teams_matches(x, "three_way")
#                                 print(arbs_opportunities)
#                             except:
#                                 continue
#                     if key == "2_way_arbs":
#                         for x in value:
#                             try:
#                                 games, arbs_opportunities = group_teams_matches(x, "two_way")
#                                 print(arbs_opportunities)
#                             except:
#                                 continue
# 
#                 # Record end time
#                 end_time = time.time()
# 
#                 # Calculate elapsed timefind_arbitrage_combinations
#                 elapsed_time = end_time - start_time
#                 print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
#                 time.sleep(1)
#             except:
#                 continue

def run_main_for_league(league_key):
    try:
        # Record start time
        start_time = time.time()

        # Fetch All Matches
        results = fetch_all_matches_for_league(all_main_functions, league_key)
        # print(f"Results for {league_key}: {results}")

        # TESTING DATA
        # json_filename = 'arbitrage_main2_results.json'
        # # Save the combined data back to the JSON file
        # with open(json_filename, 'r') as json_file:
        #     results = json.load(json_file)
        # Save the results to the JSON file
        # with open(json_filename, 'w') as json_file:
        #     json.dump(results, json_file)

        testing, awayteam_odd_even, hometeam_odd_even, second_half_away_team_overunder05, second1X2, home_clean_sheet_second_half, second_half_away_team_overunder25, second_half_away_team_overunder15, second_half_home_team_overunder25, second_half_home_team_overunder05, second_half_home_team_overunder15, first_half_away_team_overunder05, first_half_away_team_overunder25, first_half_home_team_overunder05, first_half_away_team_overunder15, first_half_home_team_overunder25, first_half_home_team_overunder15, away_clean_sheet_second_half, over_ofive_five_second_half, away_clean_sheet_first_half, home_clean_sheet_first_half, away_clean_sheet, home_clean_sheet, last_team_to_score, first_team_to_score_2nd_half, first_team_to_score_1st_half, odd_even_secondhalf, gg_secondhalf, secondhalf_dc, over_two_five_second_half, over_one_five_second_half, draw_no_bet_second_half, home_draw_win, draw_no_bet, double_chance, over_one_five, over_two_five, over_three_five, fasthalf1X2, gg, away2_home1X, home1_awayX2, X_away12, draw_no_bet_first_half, over_ofive_five, over_ofive_five_first_half, over_one_five_first_half, over_two_five_first_half, over_four_five, over_five_five, fasthalf_dc, gg_firsthalf, odd_even, odd_even_firsthalf, first_team_to_score, home_team_overunder15, home_team_overunder25, home_team_overunder05, away_team_overunder15, away_team_overunder25, away_team_overunder05 = prepare_matches_calc_arbs(
            results)
        print(f"\n\n This is my testing {testing} \n\n")
        calculate_arbs = {
            "3_way_arbs": [home_draw_win, double_chance, first_team_to_score, fasthalf1X2, fasthalf_dc, first_team_to_score,
                           first_team_to_score_1st_half, first_team_to_score_2nd_half, second1X2, last_team_to_score,
                           fasthalf_dc, secondhalf_dc],
            "2_way_arbs": [over_ofive_five, away_team_overunder25, away_team_overunder15, away_team_overunder05,
                           home_clean_sheet, first_half_away_team_overunder15, first_half_home_team_overunder05,
                           first_half_home_team_overunder25, first_half_home_team_overunder15, away_clean_sheet_second_half,
                           home_clean_sheet_second_half, away_clean_sheet, home_clean_sheet, home_clean_sheet_first_half,
                           away_clean_sheet_first_half, first_half_away_team_overunder25, first_half_away_team_overunder05,
                           second_half_away_team_overunder05, second_half_away_team_overunder25,
                           second_half_away_team_overunder15, second_half_home_team_overunder05,
                           second_half_home_team_overunder25, second_half_home_team_overunder15, away_team_overunder05,
                           home_team_overunder15, away_team_overunder25, away_team_overunder15, home_team_overunder05,
                           home_team_overunder25, odd_even_firsthalf, odd_even, gg_firsthalf, over_five_five,
                           over_four_five, over_two_five_first_half, over_one_five_first_half, over_ofive_five_first_half,
                           draw_no_bet, draw_no_bet_first_half, over_three_five, over_two_five, over_one_five, gg,
                           away2_home1X,
                           home1_awayX2, X_away12, home_team_overunder05, home_team_overunder25, home_team_overunder15,
                           awayteam_odd_even, hometeam_odd_even, odd_even_secondhalf, odd_even_firsthalf, odd_even,
                           gg_secondhalf, gg_firsthalf, over_two_five_second_half, over_one_five_second_half,
                           over_ofive_five_second_half, over_two_five_first_half, over_one_five_first_half,
                           over_ofive_five_first_half, over_ofive_five, draw_no_bet_second_half, draw_no_bet_first_half, ]}

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
        time.sleep(1)
    except Exception as e:
        print(f"Error for {league_key}: {e}")
def main():
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(keys_array)) as executor:
            futures = [executor.submit(run_main_for_league, league_key) for league_key in keys_array]

            # Wait for any future to complete (as_completed returns completed futures in the order they were completed)
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Get the result of the completed future (this may raise an exception if the task failed)
                    result = future.result()
                    print(f"Task completed for league: {result}")
                except Exception as e:
                    print(f"Task failed with exception: {e}")

        print("All tasks completed. Waiting for 3 minutes...")
        time.sleep(30)  # Wait for 3 minutes before the next iteration

if __name__ == '__main__':
    main()
    # Get the keys
