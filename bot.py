# bot.py

import logging
import os
import random
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from dotenv import load_dotenv
from responses import RESPONSES

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    response = None

    # Check if the message is a reply to the bot
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        update.message.reply_text("Don't @ me, bitch")
        return

    # Check for variations of the trigger words
    for word in text.split():
        for trigger in RESPONSES:
            if word.startswith(trigger):
                response = random.choice(RESPONSES[trigger])
                break
        if response:
            break

    # Send a reply if a trigger word or variation is found
    if response:
        update.message.reply_text(response)

# Error handling function
def error(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates."""
    logger.warning(f'Update {update} caused error {context.error}')

# Main function to start the bot
def main() -> None:
    # Get the bot token from the environment variable
    bot_token = os.getenv('TG_BOT_TOKEN')
    if not bot_token:
        logger.error('Bot token not set in the .env file')
        return

    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handle all text messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Register the error handler
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
