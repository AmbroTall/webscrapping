from bot.Login import Login
import time

bot = Login()
bot.start_site()
bot.maximize_window()

bot.login(tel_no='0722808670', password='ambroseTall3436')
time.sleep(5)
bot.main_call()
# bot.quit_automation()
