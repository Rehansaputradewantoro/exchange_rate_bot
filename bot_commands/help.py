"""Informasi tentang fungsi bot."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """untuk melihat sebuah perintah /help."""
    if update.effective_chat is not None:
        message: str = (
            'Bot dirancang untuk menampilkan nilai tukar rubel terhadap mata uang berikut:\n'
             '1. Dolar AS (USD)\n'
             '2. Euro (EUR)\n'
             '3. Yuan Tiongkok (CNY)\n'
             '4. Rubel Belarusia (BYN)\n'
             '5. Rupiah Indonesia (RP)\n'
             'Anda dapat berlangganan mata uang tertentu (termasuk tidak semua)'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Untuk Melihat Sebuah Perintah /help.')
