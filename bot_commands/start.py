"""Perintah memulai bot.."""
from configs import log_configured
from telegram import Update
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """untuk memulai bot /start."""
    if update.effective_chat is not None:
        message: str = (
            f'Saya menunjukkan nilai tukar rubel khusus untuk Anda, {update.effective_chat.first_name}.'
            '\n======<b>Perintah yang tersedia</b>======\n'
            '- /start - untuk memulai bot\n'
            '- /help - untuk melihat tombol perintah\n'
            '- /courses - nilai tukar semua mata uang terhadap rubel\n'
            '- /sub - berlangganan buletin (frekuensi dalam hitungan detik, untuk mata uang yang dipilih)\n'
            '- /unsub - Berhenti Berlangganan'
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message, parse_mode='HTML',
        )
    else:
        logger.warning('untuk memulai bot /start.')
