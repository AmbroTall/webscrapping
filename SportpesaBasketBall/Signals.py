import re
import time
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = 'ambrosetall@gmail.com'
sender_password = 'yhqihnpcxaujjggb'
receiver_emails = ['maziwamrefuajab@gmail.com', 'ndoneambrose@gmail.com']
def odds_api(event_id):
    url = f"https://www.ke.sportpesa.com/api/live/event/markets?eventId={event_id}"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.1526950031.1688206398; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _fbp=fb.1.1688206405545.1199616517; cookies_consented=1; _hjSessionUser_1199008=eyJpZCI6ImJmZGQzYmM3LTRlNTktNTVmNi1iYTZmLTljZmE5ZTBiOTdlMCIsImNyZWF0ZWQiOjE2ODgyMDY0MDU2MzIsImV4aXN0aW5nIjp0cnVlfQ==; LPVID=NhYmNmYzJiZmUxMWJjNzYw; _gid=GA1.2.1702937635.1688658222; locale=en; settings=%7B%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%22500.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Afalse%7D%2C%22first-time-bet-history-filter%22%3A%221%22%2C%22first-time-multijackpot%22%3A%221%22%7D; spkessid=o6mtffo7p56krk1bosljebkbmq; _ga=GA1.1.2044365440.1688206399; _ga_3Z30D041YQ=GS1.2.1689855732.86.0.1689855732.60.0.0; _hjIncludedInSessionSample_1199008=0; _hjSession_1199008=eyJpZCI6IjE1YTcxZWFkLTY4ZGYtNDA4Zi05NjAyLTVlMjQ4ODdhYTlkNiIsImNyZWF0ZWQiOjE2ODk4NTU3MzI0NjAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; LPSID-85738142=R-9828CARTK-C9z0CysMfw; _ga_5KBWG85NE7=GS1.1.1689855729.84.1.1689855785.4.0.0; spkessid=dufbmq45ebndoi074gv911ncd0; visited=1',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events/10319560/markets?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def quater_scores_api(event_id):
    url = f"https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/json?eventId={event_id}&cb=1688197270322"

    payload = {}
    headers = {
        'authority': 'sportpesa.betstream.betgenius.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'referer': f'https://sportpesa.betstream.betgenius.com/betstream-view/basketballscorecentre/sportpesabasketballscorecentre/html?eventId={event_id}',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    data = r['Scoreboard']

    league = data['CompetitionName']
    teams_playing = data['DisplayName']
    quarter = len(data['FirstDisplayed']['QuarterScores'])
    home_team_quarter_scores = data['FirstDisplayed']['QuarterScores'][quarter - 1]['Value']
    away_team_quarter_scores = data['SecondDisplayed']['QuarterScores'][quarter - 1]['Value']
    total_quarter_secs = data['Clock']['NumberOfQuarterSeconds']
    remaining_secs = r['Commentary']['Actions'][0]['Action']['QuarterTimeRemaining']
    remaining_quarter_secs = (int(remaining_secs) / 1000) - 3
    total_scores = int(home_team_quarter_scores) + int(away_team_quarter_scores)
    print(total_scores)
    return total_scores, total_quarter_secs, remaining_quarter_secs, league, teams_playing, quarter

def send_email(sender_email, sender_password, receiver_emails, subject, body):
    # Create a MIMEText object to represent the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)  # Join multiple recipients with commas
    msg['Subject'] = subject
    # Attach the body of the email to the MIMEText object
    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'html'))
    try:
        # Establish a connection to the email server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your email server and port
            server.starttls()  # Start a secure connection
            server.login(sender_email, sender_password)  # Login to the server

            # Send the email
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def market_odds(markets, quater):
    if quater == 3:
        quarter_name = "3rd"
    elif quater == 4:
        quarter_name = "4th"
    elif quater == 1:
        quarter_name = "1st"
    elif quater == 2:
        quarter_name = "2nd"
    else:
        return False
    for market in markets:
        if market['name'] == f"{quarter_name} Quarter Total Points Over/Under":
            outcome = market['selections'][0]['outcome']
            return outcome
    return False


def extract_integer_from_text(value):
    text = value
    match = re.search(r"\d+", text)
    if match:
        number = match.group()
        return int(number)


def predict_over_under(current_scores, remaining_quarter_secs, overall_total, total_quarter_secs):
    # Calculate the expected score per minute by the bookie
    expected_score_per_sec = overall_total / total_quarter_secs
    # Calculate the predicted total at the end of the current quarter
    predicted_total = current_scores + (expected_score_per_sec * remaining_quarter_secs)
    # Determine if the predicted total will be over or under the overall total
    if predicted_total > overall_total:
        prediction = "Over"
    else:
        prediction = "Under"
    return prediction


def get_games():
    import requests

    url = "https://www.ke.sportpesa.com/api/live/sports/4/events?count=15&offset=0"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.1526950031.1688206398; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _fbp=fb.1.1688206405545.1199616517; cookies_consented=1; _hjSessionUser_1199008=eyJpZCI6ImJmZGQzYmM3LTRlNTktNTVmNi1iYTZmLTljZmE5ZTBiOTdlMCIsImNyZWF0ZWQiOjE2ODgyMDY0MDU2MzIsImV4aXN0aW5nIjp0cnVlfQ==; LPVID=NhYmNmYzJiZmUxMWJjNzYw; _gid=GA1.2.1702937635.1688658222; locale=en; _hjSession_1199008=eyJpZCI6Ijg2M2Q3OWQ3LTY0YTktNGJjMi05ZTAzLTA0OWY2ZWE3NmQ3MiIsImNyZWF0ZWQiOjE2ODk4MzQ5NTk0OTAsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; LPSID-85738142=IoBFuYMTRa-uK5gicxFJ7Q; _hjIncludedInSessionSample_1199008=0; spkessid=ikvu50cm4j4drfjb2rc2rnrppa; settings=%7B%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%22500.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Afalse%7D%2C%22first-time-bet-history-filter%22%3A%221%22%2C%22first-time-multijackpot%22%3A%221%22%7D; _gat_UA-47970910-1=1; _ga_3Z30D041YQ=GS1.2.1689834960.85.1.1689840811.43.0.0; _ga_5KBWG85NE7=GS1.1.1689834959.83.1.1689840840.10.0.0; _ga=GA1.2.2044365440.1688206399',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    i = 0
    games = r['events']
    if len(r['events']) == 0:
        return "No game bro"
    # for game in r['events']:

    while True:
        if i >= len(games):
            i = 0
        game = games[i]
        game_id = game['id']

        if game['state']['status'] != 'STARTED':
            i += 1
            time.sleep(10)
            quater_scores_api(game_id)
            continue

        _, _, remaining_quarter_secs, _, _, quarter = quater_scores_api(game_id)
        print("min",remaining_quarter_secs/60)
        print("sec",remaining_quarter_secs)
        # print(int(remaining_quarter_secs) > 180)

        if int(remaining_quarter_secs) > 260:
            print("Not yet time")
            i += 1
            time.sleep(10)
            quater_scores_api(game_id)
            continue
        markets = odds_api(game_id)
        markets = markets['markets']

        outcome = market_odds(markets, quarter)
        if outcome == False:
            i += 1
            time.sleep(10)
            quater_scores_api(game_id)
            continue
        odds = extract_integer_from_text(outcome) + 1
        total_scores, total_quarter_secs, remaining_quarter_secs, league, teams_playing, _ = quater_scores_api(game_id)
        print("Total Scores", total_scores)
        print("Remaining Quarter Seconds", remaining_quarter_secs)
        prediction = predict_over_under(total_scores, int(remaining_quarter_secs), odds, int(total_quarter_secs))

        # Send Signals
        subject = f'BOT SIGNAL SPORTPESA BASKETBALL LIVE {teams_playing}'
        body = f"""
        <p style="font-weight: bold;">LEAGUE: {league} </p>
        <p style="font-weight: bold; font-size: 28px; color: '#ccc'">{teams_playing} </p>
        <p style="font-weight: bold; font-size: 24px">💰Signal: {prediction.upper()} {prediction.upper()} {prediction.upper()} {odds}💰</p>
        <p style="font-weight: bold; font-size: 24px; text: center">💰💰💰Stake High!💰💰💰</p>
        <p style="font-weight: bold; font-size: 14px; float: right">Signals by <a>Wamaploty Don</a></p>
        """
        if int(remaining_quarter_secs) > 150 and prediction == "Over":
            send_email(sender_email, sender_password, receiver_emails, subject, body)

        print(f"\n--------+LEAGUE: \033[1m{league}\033[0m +---------")
        print(f"--------+GAME: \033[1m{teams_playing}\033[0m +---------")
        print(f"++++++++💰💰💰Signal (Stake High): \033[1m{prediction.upper()}\033[0m \033[1m{prediction.upper()}\033[0m \033[1m{prediction.upper()}\033[0m {odds}💰💰💰")
        i += 1
        time.sleep(10)
        quater_scores_api(game_id)
try:
    get_games()
except:
    get_games()
