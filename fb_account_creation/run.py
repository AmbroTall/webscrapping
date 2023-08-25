from bot.fb_account_create import CreateFacebookAccount
from bot.gmail_create_account import CreateGmailAccount

first_name = "Money"
surname = "Money"
mail = "amrt@gmail.com"
pwd = "Ambrose12345."
day = "2"
month = "March"
year = "1975"
gender = "Male"
recovery_mail = "ambrosetall"

bot = CreateGmailAccount()
bot.start_site()
bot.maximize_window()
bot.create_account(first_name, surname, pwd, day, month, year, gender, recovery_mail)
# bot.betting()
# bot.quit_automation()
