import pytz
from bot.Login import Login
from datetime import datetime
from bot.getstarttime import get_start_time
import time

# Sample list of game information
# games = [{'timgamese': 1694725200, 'competition_name': 'BBL', 'country': 'England', 'home_team': 'Newcastle Eagles', 'away_team': 'Sheffield Sharks'}]

# Define the Kenyan time zone (KST)
kenyan_tz = pytz.timezone('Africa/Nairobi')


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

# while True:
#     games = get_start_time()
#
#     # Get the next game's start time using Linux timestamps
#     next_start_time = find_next_start_time(games)
#
#     # Get the current time in Linux timestamp
#     current_time_unix = int(time.time())
#
#     if next_start_time:
#         # Calculate the delay until the next game's start time
#         days, seconds, delay, hours, minutes = convert_unix_timestampes_datetime(next_start_time, current_time_unix)
#
#         # Wait until the next game's start time is reached
#         if delay and delay > 0:
#             local_time = kenyan_time(next_start_time)
#             print(f"Exact Time to Start: {local_time} - Time difference: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
#             time.sleep(delay + 150)  # Sleep in seconds
#             # Now, your bot can start because the next game's start time has been reached
#             print("Starting the bot now!")
#             # Set the total duration in seconds (1800 seconds = 30 minutes)
#             total_duration = 1800
#             # Set the time interval for each iteration (in seconds)
#             interval = 60  # For example, perform tasks every 5 seconds
#             # Record the start time
#             start_time = time.time()
#             for _ in range(total_duration // interval):
#                 try:
#                     print("Started")
#                     bot = Login()
#                     bot.start_site()
#                     bot.maximize_window()
#
#                     bot.login(tel_no='0722808670', password='ambroseTall3436')
#                     time.sleep(5)
#                     x = bot.main_call()
#                     print("this is what I get from bot", x)
#                     if x == "No games":
#                         print("Hello Ambrose")
#                         bot.quit_automation()
#                         break
#                 except:
#                     bot.quit_automation()
#                     time.sleep(10)
#                     pass
#         else:
#             print("Game has started")
#             continue


bot = Login()
bot.start_site()
bot.maximize_window()

bot.login(tel_no='0722808670', password='ambroseTall3436')
time.sleep(5)
x = bot.main_call()