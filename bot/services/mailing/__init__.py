import logging

from aiogram import Bot
from redis.asyncio import Redis

from .consumer import DelayedMessageConsumer

from nats.aio.client import Client
from nats.js.client import JetStreamContext

logger = logging.getLogger(__name__)


async def start_delayed_consumer(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    r: Redis,
    subject: str,
    stream: str,
    durable_name: str
) -> None:
    consumer = DelayedMessageConsumer(
        nc=nc,
        js=js,
        bot=bot,
        r=r,
        subject=subject,
        stream=stream,
        durable_name=durable_name
    )
    logger.info('Start delayed message consumer')
    await consumer.start()