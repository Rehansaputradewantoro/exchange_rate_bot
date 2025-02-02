"""Titik peluncuran bot."""
import locale

from bot_commands import start, help_command, courses, sub, unsub
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

    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)

    courses_handler = CommandHandler('courses', courses)
    application.add_handler(courses_handler)

    sub_handler = CommandHandler('sub', sub)
    application.add_handler(sub_handler)

    unsub_handler = CommandHandler('unsub', unsub)
    application.add_handler(unsub_handler)

    application.run_polling()
