# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext import filters

from src.settings import Settings
from src.handlers import handler_start, handler_help, handler_button, handler_message, native_error_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    settings = Settings()
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', handler_start))
    application.add_handler(CommandHandler('help', handler_help))
    application.add_handler(CallbackQueryHandler(handler_button))
    application.add_handler(MessageHandler(filters.Entity("mention"), handler_message))
    application.add_error_handler(native_error_handler)
    application.run_polling()
