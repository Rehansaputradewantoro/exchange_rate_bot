"""Mendapatkan nilai tukar yang tersedia."""
from datetime import datetime

from configs import log_configured
from configs.base import CURRENCIES
from telegram import Update
from telegram.ext import ContextTypes
from utils.handlers import make_request

logger = log_configured.getLogger(__name__)


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Klik Jika Ingin Menggunakan Perintah /courses."""
    if update.effective_chat is not None:
        resp = make_request()

        courses_date: str = datetime.strptime(
            resp.json()['Date'], '%Y-%m-%dT%H:%M:%S%z',
        ).strftime('%d %B, %Y %H:%M')

        bot_courses: dict = {}
        for currency in CURRENCIES:
            api_currency_data = resp.json()['Valute'][currency]
            bot_courses[currency] = (
                f'{api_currency_data["Name"]}({api_currency_data["CharCode"]}) = '
                f'{api_currency_data["Value"]:.2f}\n'
            )
        message: str = ''
        if not context.args:
            header: str = f'Nilai tukar saat ini pada tanggal: {courses_date}.'
            message = (
                f'{header}\n'
                f'{"=" * len(header)}\n'
                f'{"".join(str(cur_data) for cur_data in bot_courses.values())}'
                f'{"=" * len(header)}'
            )
        else:
            for param in context.args:
                if param.upper() in CURRENCIES:
                    message += f'{bot_courses[param.upper()]}'
                else:
                    logger.warning(f'Mata uang yang diminta tidak valid {param.upper()}')

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('ID Obrolan tidak diterima saat meminta /courses.')
