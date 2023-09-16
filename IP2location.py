from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import IP2Location
import re

# Telegram Bot Token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize IP2Location
ip2loc = IP2Location.IP2Location()
ip2loc.open("path/to/your/database.bin")  # Replace with the path to your .BIN database file

# Start command handler
def start(update, context):
    update.message.reply_text("Welcome to the IP Location Bot. Send me an IP address to get its location information.")

# Location handler
def get_location(update, context):
    user_input = update.message.text

    # Use regular expression to validate if the input is a valid IP address
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', user_input):
        try:
            location = ip2loc.get_all(user_input)
            if location.country_short and location.city:
                response = f"IP Address: {user_input}\n"
                response += f"Country Code: {location.country_short}\n"
                response += f"Country Name: {location.country_long}\n"
                response += f"Region Name: {location.region}\n"
                response += f"City Name: {location.city}\n"
                response += f"Latitude: {location.latitude}\n"
                response += f"Longitude: {location.longitude}\n"
                response += f"ZIP Code: {location.zipcode}\n"
                response += f"Time Zone: {location.timezone}\n"
                
                # Send location on a map
                latitude = location.latitude
                longitude = location.longitude
                update.message.reply_location(latitude, longitude)
            else:
                response = "Location information not found for this IP."

            update.message.reply_text(response)
        except Exception as e:
            update.message.reply_text("An error occurred while processing your request.")
    else:
        update.message.reply_text("Please enter a valid IP address for location information.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_location))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
