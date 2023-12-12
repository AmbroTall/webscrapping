import time
import requests
from bs4 import BeautifulSoup
from SoccerArb.newbot.utils import map_teams, testing_function, request_function, request_function_bs4


def api_calls_events(event_id):
    r = request_function_bs4(f'https://parimatch.co.tz/football/prematch/1?tournaments={event_id}', {},{})
    # Create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')
    # Find all elements with class 'sportList__content'
    elements = soup.find_all(class_='event-card__wrapper')
    return elements

def api_call_odds(match_id, home_team, away_team):
    url = f"https://parimatch.co.tz/api/Football/events/{match_id}/popular/odds"

    payload = {}
    headers = {
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Channel': 'MOBILE_IOLITE',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
        'Referer': f'https://parimatch.co.tz/events/{home_team}_{away_team}_{match_id}',
        'sec-ch-ua-platform': '"Linux"',
        'Cookie': 'ISO2=TZ; ISO3=TZS; currencyId=20; defaultLanguage=sw; language=sw'
    }
    response = request_function(url, headers, payload)
    return response['markets']

def exctract_odds(match, league, bookie_name):
    filtered_list = [value for value in match.text.split('\n') if value != '']
    home_odd = filtered_list[2]
    draw_odd = filtered_list[4]
    away_odd = filtered_list[6]

    games = {}

    wager_types = []
    draw_no_bet = []
    double_chance = []
    handicap1 = []  # -1.5 / 1.5
    over_one_five = []
    over_two_five = []
    over_three_five = []
    fasthalf1X2 = []
    gg = []

    games['match_id'] = match.get('data-event-detail')

    # Get the team mapping for the specified bookie and league
    team_mapping = map_teams(bookie_name, league)

    # Use the default team names if mapping is available, otherwise use the original names
    games['home_team'] = team_mapping.get(filtered_list[0], filtered_list[0])
    games['away_team'] = team_mapping.get(filtered_list[1], filtered_list[1])


    odds_market = api_call_odds(match.get('data-event-detail'),filtered_list[0],filtered_list[1])
    # print(odds_market)

    # Loop over the odds dictionary to extract the different wager types odds

    home_draw_away = [home_odd, draw_odd, away_odd]
    wager_types.append({"1X2": home_draw_away})
    for x in odds_market:
        market_name = x['translation']
        if market_name == 'Double chance':
            market_odds = x['items'][0]['outcomes']
            dnbhome = market_odds[0]['odds']
            dnbdraw = market_odds[1]['odds']
            dnbaway = market_odds[2]['odds']
            double_chance = [dnbhome, dnbdraw, dnbaway]
            wager_types.append({"double_chance": double_chance})

        if market_name == 'Both teams to score':
            market_odds = x['items'][0]['outcomes']
            ggyes = market_odds[0]['odds']
            ggno = market_odds[1]['odds']
            gg = [ggyes, ggno]
            wager_types.append({"gg": gg})

        if market_name == 'Total':
            market_odds = x['items']
            for i in market_odds:
                if i['translations'][0] == '1.5':
                    over15 = i['outcomes'][0]['odds']
                    under15 = i['outcomes'][1]['odds']
                    over_one_five = [over15, under15]
                    wager_types.append({"over_one_five": over_one_five})
                if i['translations'][0] == '2.5':
                    over25 = i['outcomes'][0]['odds']
                    under25 = i['outcomes'][1]['odds']
                    over_two_five = [over25, under25]
                    wager_types.append({"over_two_five": over_two_five})
                if i['translations'][0] == '3.5':
                    over35 = i['outcomes'][0]['odds']
                    under35 = i['outcomes'][1]['odds']
                    over_three_five = [over35, under35]
                    wager_types.append({"over_three_five": over_three_five})

    handicap1 = []  # -1.5 / 1.5

    away2_home1X = [away_odd, double_chance[0]]
    home1_awayX2 = [home_odd, double_chance[2]]
    X_away12 = [draw_odd, double_chance[1]]

    wager_types.append({"over_one_five": over_one_five})
    wager_types.append({"over_three_five": over_three_five})
    wager_types.append({"21X": away2_home1X})
    wager_types.append({"12X": home1_awayX2})
    wager_types.append({"X12": X_away12})

    games['wager_types'] = wager_types
    return games


def check_team_names_in_match_details(team_names, match_details):
    # Extract team names from the match details
    team_names_from_matches = set()
    for match_detail in match_details:
        filtered_list = [value for value in match_detail.text.split('\n') if value != '']
        home_team = filtered_list[0]
        away_team = filtered_list[1]

        if home_team and isinstance(home_team, str):
            team_names_from_matches.add(home_team)
        if away_team and isinstance(away_team, str):
            team_names_from_matches.add(away_team)

    # Filter out non-string items from the team_names list
    team_names = [team.strip() for team in team_names if isinstance(team, str)]
    # Check if all team names are present in the extracted names
    missing_teams = [team for team in team_names if team not in team_names_from_matches]
    return missing_teams


def process_league(league_dict):
    for league_name, league_id in league_dict.items():
        return league_name, league_id



def main():
    bookie_name = 'parimatch'
    leagues = [
        {"England Premier League": "7f5506e872d14928adf0613efa509494"},
        {"England Championship": "eeb107510b84417f833551f3b6e2351c"},
        {"England League One": "f8bee2c7dcdb40fdb604f1a5c14976b6"},
        {"England League Two": "ddab861df0aa4411bb5b1f63fcd82a71"},
        {"Scotland Premiership": "10bed6b95e4e4d63a272f05aeab0980d"},
        {"Scotland Championship": "d7ce743def964991ac9d9ba22cc3299d"},
        {"Scotland League One": "3e4263310bbf420685824264cca7db0e"},
        {"Scotland League Two": "83613004614e43b1bdd88d9744e2225e"}
    ]
    bookmaker_data = []
    for league in leagues:
        try:

            print(league)
            league_name, league_id = process_league(league)
            match_details = api_calls_events(f"{league_id}")

            league_mapping = {
                "England Premier League": "England-Premier League",
                "England Championship": "England-EFL Cup",
                "England League One": "England-League One",
                "England League Two": "England-League Two",
                "Scotland Premiership": "Scotland-Premiership",
                "Scotland Championship": "Scotland-Championship",
                "Scotland League One": "Scotland-League One",
                "Scotland League Two": "Scotland-League Two",
            }
            # Check if the league_name is in the mapping dictionary, if yes, update it
            if league_name in league_mapping:
                league_name = league_mapping[league_name]

            # Testing Function To See if teams are correctly named
            testing = testing_function(bookie_name, league_name)
            missing_names = check_team_names_in_match_details(testing, match_details)
            print("**** This are the missing matches", missing_names)

            liga = {}
            league_data = []

            for match in match_details:
                    league_wager_dic = exctract_odds(match, league_name, bookie_name)
                    league_data.append(league_wager_dic)
            liga[league_name] = league_data
            bookmaker_data.append(liga)
            print("parimatch", bookmaker_data)
        except Exception as e:
            print("Ambrose", e)
            continue
    return bookmaker_data

if __name__ == '__main__':
    start_time = time.time()
    games = main()
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = elapsed_time_seconds / 60

    print(f"Elapsed Time: {elapsed_time_seconds:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")
    print("This is my output", games)
