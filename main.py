import random
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import requests

from brain import get_message
from quotes import get_quote
from utils import escape_html
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TG_API_KEY")


category = "happiness"
api_url = "https://api.api-ninjas.com/v1/quotes?category={}".format(category)
response = requests.get(api_url, headers={"X-Api-Key": "YOUR_API_KEY"})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        rf"""Hello {user.name}, Welcome to Pyfuse Bot.
I am Pyfuse's personal assistant"""
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        Use the following commands to interact with me.
    /start: Start the convo!
    /help: Get help!
    /quote: Get a quote!
    """
    )


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Getting quote...")
    q = get_quote("happiness")
    await update.message.reply_text(f"\"{q['quote']}\" ~{q['author']}")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text

    try:
        await update.message.reply_text("Generating...")
        ai_response = get_message(update.effective_user.full_name, msg)
        await update.message.reply_html(escape_html(ai_response))
    except Exception as e:
        print(e)
        await update.message.reply_text(
            f"An error occured,\nPlease resend your prompt.\n Error:{e}"
        )


def main() -> None:
    try:
        # Create the application
        application = Application.builder().token(API_KEY).build()

        # Add commands
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help))
        application.add_handler(CommandHandler("quote", quote))

        # Handle non command messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

        print("Server running!")
        #  Running the main app
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print("Error occured: ", e)


if __name__ == "__main__":
    main()
