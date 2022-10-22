from bot.Booking import Booking

bot = Booking()
bot.start_site()
bot.change_currency("USD")
bot.destination("Kenya")
bot.checkin_checkout()
bot.number_of_people(adults=10)
bot.number_of_children(age=9)
bot.room_numbers(room=3)
bot.search_results()
# bot.refresh()
bot.filtration()

