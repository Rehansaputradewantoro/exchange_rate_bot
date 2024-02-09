"""Mendapatkan nilai tukar ke rubel yang dipilih oleh pengguna."""
from configs import log_configured
from configs.base import CURRENCIES
from exceptions import ServiceException
from telegram import Update
from telegram.ext import ContextTypes
from utils.handlers import remove_job_if_exists, send_subscription

logger = log_configured.getLogger(__name__)


async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """untuk menggunakannya ketik /sub."""
    if update.effective_chat is not None:
        message: str = (
            '<b>Anda dapat berlangganan mata uang berikut:</b>\n'
            f'{" ".join((cur for cur in CURRENCIES))}\n'
            'Hal ini dilakukan seperti contoh ini: /sub 10 USD CNY\n'
            'Parameter pertama adalah waktu dalam hitungan detik, sisanya adalah mata uang untuk berlangganan\n'
             'Minimum Anda perlu menentukan waktu dan setidaknya 1 mata uang, jika tidak, maka tidak akan berfungsi'
        )

        if context.args and context.args[0].isnumeric():
            if int(context.args[0]) <= 5:
                logger.warning('Parameter pertama dalam langganan kurang dari atau sama dengan 5 detik.')
                raise ServiceException(
                    f'Setel frekuensi berlangganan ke angka lebih dari 5 detik, bukan: {context.args[0]}',
                )
            subbed_curs: list = []
            for param in context.args[1:]:
                if param.upper() in CURRENCIES:
                    subbed_curs.append(param.upper())
                else:
                    logger.warning(f'Abaikan mata uang yang tidak tersedia untuk pengiriman: {param.upper()}')
            message = (
                f'Berlangganan mata uang = <b>{*subbed_curs, }</b> =.\nBuletin sekali setiap {context.args[0]} detik.'
            )

            await remove_job_if_exists(str(update.effective_chat.id), context)

            context.job_queue.run_repeating(  # type: ignore
                send_subscription, int(context.args[0]),
                chat_id=update.effective_chat.id,
                name=str(update.effective_chat.id),
                data=[int(context.args[0]), subbed_curs],
            )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message, parse_mode='HTML',
        )
    else:
        logger.warning('untuk memulai berlangganan /sub.')


async def unsub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Batalkan langganan."""
    if update.effective_chat is not None:
        job_removed = await remove_job_if_exists(str(update.effective_chat.id), context)
        message = 'Langganan dibatalkan' if job_removed else 'Tidak ada langganan. Tidak ada yang perlu dibatalkan.'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
    else:
        logger.warning('Tidak diteruskan ke berhenti berlangganan effective_chat.')
