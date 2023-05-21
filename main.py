"""Точка запуска бота."""
import locale

from bot_commands import start
from configs import log_configured
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from utils.handlers import get_token

logger = log_configured.getLogger(__name__)
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

load_dotenv()
TOKEN = get_token('TG_TOKEN')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
