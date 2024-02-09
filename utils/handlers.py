"""Penangan parameter."""
import os
from http import HTTPStatus

import requests

from configs import log_configured
from configs.base import API_URL
from exceptions import APIException, ServiceException
from requests import Response
from telegram.ext import ContextTypes

logger = log_configured.getLogger(__name__)


def get_token(key: str) -> str:
    """Memeriksa keberadaan token."""
    token: str = os.getenv(key)
    if token is not None:
        return token
    logger.error('Kesalahan, tidak ada tanda')
    raise APIException('Token untuk akses ke bot tidak ditransfer.')


async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Hapus langganan jika sudah ada."""
    current_jobs = context.job_queue.get_jobs_by_name(name)  # type: ignore
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def send_subscription(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kami mengirimkan pemberitahuan untuk mata uang berlangganan."""
    job = context.job
    resp = make_request().json()
    message: str = f'Lulus {job.data[0]} detik.'  # type: ignore
    for currency in job.data[1]:  # type: ignore
        message += f'\n{resp["Valute"][currency]["CharCode"]} = {resp["Valute"][currency]["Value"]:.3f}'
    await context.bot.send_message(str(job.chat_id), text=message)  # type: ignore


def make_request(url: str = API_URL) -> Response:
    """Menerima respons dari API Mata Uang."""
    resp = requests.get(url)
    if resp.status_code != HTTPStatus.OK:
        logger.error(f'Respon yang salah dari layanan nilai tukar: {resp.status_code}')
        raise ServiceException(f'Kesalahan respons dari {API_URL}: {resp.text}')
    return resp
