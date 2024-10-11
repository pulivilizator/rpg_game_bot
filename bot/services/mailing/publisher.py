from aiogram import Bot
from nats.js.client import JetStreamContext
from datetime import datetime


async def publish_mailing_message(
    js: JetStreamContext,
    chat_id: int,
    subject: str,
    delay: float = 0
) -> None:
    headers = {
        'Tg-Delayed-Chat-ID': str(chat_id),
        'Tg-Delayed-Msg-Timestamp': str(datetime.now().timestamp()),
        'Tg-Delayed-Msg-Delay': str(delay),
    }
    await js.publish(subject=subject, headers=headers)