import json
import os
from itertools import combinations, product, groupby
from operator import itemgetter
from Levenshtein import distance
from odibet import odi_bets as odibet
from sportpesa import sport_pesa as sportpesa
from betika import betika as betika
import logging
import time
import concurrent.futures
import smtplib
from email.mime.text import MIMEText
from tabulate import tabulate
from collections import defaultdict
from fuzzywuzzy import fuzz, process

all_main_functions = {
    "odi": odibet,
    "sportpesa": sportpesa,
    "betika": betika,
}

sender_email = 'ambrosetall@gmail.com'
receiver_emails = ['maziwamrefuajab@gmail.com', 'paolosiroko@gmail.com']


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


def arbitrage_calc(odds, total_stake):
    prob = [1 / float(odd) for odd in odds]
    total_prob = sum(prob)

    # Calculate initial stakes without considering taxes
    initial_stakes = [(total_stake * p / total_prob) for p in prob]

    # Calculate total initial winnings without considering taxes
    initial_winnings = [float(stake) * float(odd) for stake, odd in zip(initial_stakes, odds)]

    # Define tax rates
    tax_on_stake = 0.125  # 12.5% tax on stake
    withholding_tax = 0.20  # 20% withholding tax on winnings

    # Adjust the initial stakes to cover both taxes
    adjusted_stakes = [stake / (1 - tax_on_stake - withholding_tax) for stake in initial_stakes]

    # Calculate adjusted winnings after withholding tax using adjusted_stakes
    adjusted_winnings = [float(adjusted_stake) * float(odd) for adjusted_stake, odd in zip(adjusted_stakes, odds)]

    # Calculate one winning value as the difference between the sum of adjusted winnings and the sum of adjusted stakes
    winning_value = adjusted_winnings[1] - sum(adjusted_stakes)
    # Return adjusted stakes, adjusted winnings, and one winning value
    return {
               f'adjusted_stake{i + 1} for Bookmaker {i + 1} with odds {odds[i]}': round(adjusted_stakes[i], 2)
               for i in range(len(odds))
           }, {
               f'adjusted_winnings{i + 1}': round(adjusted_winnings[i], 2)
               for i in range(len(odds))
           }, round(winning_value, 2)

def calculate_arbitrage(outcomes):
    total_implied_probability = sum(1 / float(odd) for odd in outcomes)
    arbitrage_percentage = (1 - total_implied_probability) / total_implied_probability * 100
    return arbitrage_percentage, total_implied_probability


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


def prepare_matches_calc_arbs(matches):
    array_1X2 = []
    array_gg = []
    array_dc = []
    array_21X = []
    array_12X = []
    array_X12 = []
    array_12 = []
    for key, matches in matches.items():
        bookie_name = key
        for match in matches:
            wager_types = match['wager_types']
            for wager in wager_types:
                key, values = next(iter(wager.items()))
                if key == "1X2":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['time'] = match['time']

                    match_data['home_team'] = match['home_team']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_1X2.append(match_data)

                    match_data2 = {}
                    match_data2['bookname'] = bookie_name
                    match_data2['event'] = "1 or 2 Risk!"
                    match_data2['time'] = match['time']
                    match_data2['home_team'] = match['home_team']
                    match_data2['away_team'] = match['away_team']
                    match_data2['odds'] = [values[0],values[-1]]
                    array_12.append(match_data2)
                if key == "dc":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['time'] = match['time']

                    match_data['home_team'] = match['home_team']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_dc.append(match_data)
                if key == "gg":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['time'] = match['time']

                    match_data['home_team'] = match['home_team']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_gg.append(match_data)
                if key == "21X":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['time'] = match['time']

                    match_data['home_team'] = match['home_team']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_21X.append(match_data)
                if key == "12X":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['home_team'] = match['home_team']
                    match_data['time'] = match['time']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_12X.append(match_data)
                if key == "X12":
                    match_data = {}
                    match_data['bookname'] = bookie_name
                    match_data['event'] = key
                    match_data['time'] = match['time']
                    match_data['home_team'] = match['home_team']
                    match_data['away_team'] = match['away_team']
                    match_data['odds'] = values
                    array_X12.append(match_data)

    return array_12, array_1X2, array_gg, array_21X, array_12X, array_X12, array_dc


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


def split_and_sort_team_names(team_name):
    return sorted(team_name.lower().split(), key=len, reverse=True)

def match_team_names(name1, name2):
    names1 = split_and_sort_team_names(name1)
    names2 = split_and_sort_team_names(name2)

    # Check if any words from home team match with any words from away team
    return any(word1 == word2 for word1 in names1 for word2 in names2)

def check_unique_booknames(match_data):
    booknames_set = set()
    for book_data in match_data:
        bookname = book_data['bookname']
        if bookname in booknames_set:
            # Bookname already seen, indicating a violation
            return False
        else:
            # Add the bookname to the set
            booknames_set.add(bookname)
    # All booknames in the group are unique
    return True

def group_matches(matches_lists, wager_type):
    print("Matches List")
    # Sort the list based on time, home_name, and away_name using word matching
    matches_lists.sort(key=lambda x: (x['time'], x['home_team'], x['away_team']))

    # Group matches by time, home_name, and away_name
    grouped_matches = {}
    current_key = None
    current_group = []

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
    # print(grouped_matches)
    arbs_opportunities = []
    games = []
    for key, matches in grouped_matches.items():
        # +++++ Debugging +++++
        games.append(matches)
        min_profit_percentage = 0
        fixed_stake = 1000
        try:
            if len(matches) > 1 and check_unique_booknames(matches):
                print(f"Key : {key} Match : {len(matches)} {matches}")
                arb = None
                if wager_type == "three_way":
                    arb = find_arbitrage_combinations(matches, min_profit_percentage, fixed_stake)
                elif wager_type == "two_way":
                    arb = find_arbitrage_combinations_two_way(matches, min_profit_percentage, fixed_stake)

                if arb:
                    print(f"+++++++++++++{arb}+++++++++++++++")
                    arbs_opportunities.append(arb)

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
                        save_arbs(arb, table_data)  # Add a separator line between each combination
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
        except Exception as e:
            print("Error in calculating arbs", e)
            continue

    return games, arbs_opportunities


def main():
    while True:
        results = fetch_all_matches(all_main_functions)
        print("This are the results", results)

        # Record start time
        start_time = time.time()

        array_12, array_1X2, array_gg, array_21X, array_12X, array_X12, array_dc = prepare_matches_calc_arbs(results)

        calculate_arbs = {"3_way_arbs": [array_1X2, array_dc],
                          "2_way_arbs": [array_12, array_gg, array_21X, array_12X, array_X12]}

        for key, value in calculate_arbs.items():
            if key == "3_way_arbs":
                for x in value:
                    try:
                        games, arbs_opportunities = group_matches(x, "three_way")
                    except Exception as e:
                        print(e)
                        continue
            if key == "2_way_arbs":
                for x in value:
                    try:
                        games, arbs_opportunities = group_matches(x, "two_way")
                        print(arbs_opportunities)
                    except Exception as e:
                        print(e)
                        continue

        # Record end time
        end_time = time.time()

        # Calculate elapsed timefind_arbitrage_combinations
        elapsed_time = end_time - start_time
        print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        time.sleep(5)

if __name__ == '__main__':
    main()
    # Get the keys
