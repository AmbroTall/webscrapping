import pytz
import requests

from bot.Login import Login
from datetime import datetime
from bot.getstarttime import get_start_time
import time

# Sample list of game information
# games = [{'timgamese': 1694725200, 'competition_name': 'BBL', 'country': 'England', 'home_team': 'Newcastle Eagles', 'away_team': 'Sheffield Sharks'}]

# Define the Kenyan time zone (KST)
kenyan_tz = pytz.timezone('Africa/Nairobi')


def live_games_display():
    print("Checking Started Live Games")
    url = "https://www.ke.sportpesa.com/api/live/sports/4/events?count=15&offset=0"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'device_view=full; visited=1; _gcl_au=1.1.689064392.1693297828; initialTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set); __utmzzses=1; _ga_3Z30D041YQ=GS1.2.1693297830.1.0.1693297830.60.0.0; _fbp=fb.1.1693297833263.964665515; cookies_consented=1; LPVID=Q0ZjE4N2ViNGZiM2JkZDdh; _hjSessionUser_1199008=eyJpZCI6ImY1NmExZDIxLTZkY2YtNTM1ZC1hNDdlLWU0OTcwMWUzZGIwNyIsImNyZWF0ZWQiOjE2OTMyOTc4MjkyNzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1111460384.1694628076; settings=%7B%22first-time-multijackpot%22%3A%221%22%2C%22betslip%22%3A%7B%22acceptOdds%22%3A%221%22%2C%22amount%22%3A%2250.00%22%2C%22direct%22%3Atrue%2C%22betSpinnerSkipAnimation%22%3Atrue%7D%7D; locale=en; spkessid=u9335e7ldusjlra39bufefmndl; _ga=GA1.1.619053130.1693297829; LPSID-85738142=oBtwahmWT_GruGrVRahInw; _ga_5KBWG85NE7=GS1.1.1694886035.34.0.1694886035.60.0.0',
        'Referer': 'https://www.ke.sportpesa.com/en/live/events?sportId=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-App-Timezone': 'Africa/Nairobi',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.get(url, headers)
    r = response.json()
    if r['events']:
        print("Live games = ", r['events'])
        return r['events']
    return None


def kenyan_time(sec):
    print(sec)
    # Define the Nairobi time zone
    nairobi_tz = pytz.timezone('Africa/Nairobi')
    # Convert the Unix timestamp to a datetime object in UTC (without dividing by 1000)
    timestamp_seconds = sec
    date_time_utc = datetime.utcfromtimestamp(timestamp_seconds / 1000)
    # Localize the datetime object to Nairobi time zone
    date_time_nairobi = date_time_utc.replace(tzinfo=pytz.utc).astimezone(nairobi_tz)
    # Format the datetime object as a string
    formatted_datetime = date_time_nairobi.strftime("%Y-%m-%d %H:%M:%S %Z")
    return formatted_datetime


# Function to find the next game's start time using Linux timestamps
def find_next_start_time(games):
    current_time_unix = int(time.time())  # Current time in Linux timestamp (seconds)
    next_start_time = None
    for game in games:
        game_time_unix = game['time']  # Linux timestamp (seconds)

        if game_time_unix > current_time_unix and (next_start_time is None or game_time_unix < next_start_time):
            next_start_time = game_time_unix
    return next_start_time


# Convert Unix timestamps to datetime objects
def convert_unix_timestampes_datetime(next_start_time, current_time_unix):
    datetime1 = datetime.fromtimestamp(next_start_time / 1000)
    datetime2 = datetime.fromtimestamp(current_time_unix)
    # Calculate the time difference as a timedelta object
    time_difference = datetime1 - datetime2
    # Extract time difference components if needed
    days = time_difference.days
    seconds = time_difference.seconds
    delay = seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, seconds, delay, hours, minutes


while True:
    games = get_start_time()
    # Get the next game's start time using Linux timestamps
    next_start_time = find_next_start_time(games)
    # Get the current time in Linux timestamp
    current_time_unix = int(time.time())

    if next_start_time:
        # Calculate the delay until the next game's start time
        days, seconds, delay, hours, minutes = convert_unix_timestampes_datetime(next_start_time, current_time_unix)

        if delay and delay > 0:
            local_time = kenyan_time(next_start_time)
            print(f"Exact Time to Start: {local_time} - Time difference: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
            time.sleep(delay + 150)  # Sleep in seconds
            # Now, your bot can start because the next game's start time has been reached
            print("Starting the bot now!")
            # Set the total duration in seconds (1800 seconds = 30 minutes)
            total_duration = 1800
            # Set the time interval for each iteration (in seconds)
            interval = 60  # For example, perform tasks every 5 seconds
            # Record the start time
            start_time = time.time()
            for _ in range(total_duration // interval):
                print("Started")
                bot = Login()
                time.sleep(10)
                try:
                    print("Bot started successfully")
                    bot.start_site()
                    bot.maximize_window()

                    bot.login(tel_no='0722808670', password='ambroseTall3436')
                    time.sleep(5)
                    x = bot.main_call()
                    print("this is what I get from bot", x)
                    if x == "No games":
                        print("Hello Ambrose")
                        bot.quit_automation()
                        break
                except:
                    print("Qui")
                    bot.quit_automation()
                    time.sleep(10)
                    continue
        else:
            print("Game has started")
            continue


# for i in range(1,26):
#     try:
#         print("Started")
#         bot = Login()
#         time.sleep(10)
#         print("Bot started successfully")
#         bot.start_site()
#         bot.maximize_window()
#
#         bot.login(tel_no='0722808670', password='ambroseTall3436')
#         time.sleep(5)
#         bot.quit_automation()
#         bot.main_call()
#     except Exception as e:
#         print("Qui",e)
#         time.sleep(10)
#         continue
