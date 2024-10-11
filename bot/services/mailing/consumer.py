import logging

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter, TelegramAPIError
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import payload_type

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext
from redis.asyncio import Redis

from core.enums import LinksRedisKeys, MailingKeys

logger = logging.getLogger(__name__)


class DelayedMessageConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            r: Redis,
            bot: Bot,
            subject: str,
            stream: str,
            durable_name: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.r = r
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True
        )

    async def on_message(self, msg: Msg):
        message_raw = await self.r.get(MailingKeys.TEXT)

        if message_raw is None:
            await msg.ack()

        message_text = message_raw.decode('utf-8')
        chat_id = msg.headers.get('Tg-Delayed-Chat-ID')
        media_id, media_type = await self.get_media()
        buttons = await self.get_buttons()
        if await self.r.exists('WAIT_MAILING'):
            time_raw = await self.r.get('WAIT_MAILING')
            time = int(time_raw.decode('utf-8'))
            await msg.nak(delay=time)
            return
        try:
            if media_type is None:
                await self.bot.send_message(chat_id=chat_id, text=message_text, reply_markup=buttons)
                await msg.ack()

            elif media_type == ContentType.PHOTO.value:
                await self.bot.send_photo(chat_id=chat_id, photo=str(media_id), caption=message_text, reply_markup=buttons)
                await msg.ack()

            elif media_type == ContentType.VIDEO.value:
                await self.bot.send_video(chat_id=chat_id, video=str(media_id), caption=message_text, reply_markup=buttons)
                await msg.ack()
        except TelegramForbiddenError:
            await msg.ack()
        except TelegramRetryAfter as e:
            await self.r.setex('WAIT_MAILING', value=int(e.retry_after) + 50, time=int(e.retry_after) + 50)
        except TelegramAPIError:
            await msg.nak(delay=600)

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribed')

    async def get_media(self):
        media_raw = await self.r.get(MailingKeys.MEDIA)
        if media_raw:
            return media_raw.decode('utf-8').split(':')
        return None, None

    async def get_buttons(self):
        links_raw = await self.r.get(MailingKeys.LINKS)
        if links_raw:
            kb_builder = InlineKeyboardBuilder()
            buttons = []
            links = [i.split(':::', 1) for i in links_raw.decode('utf-8').split('|')]
            for link in links:
                buttons.append(
                    InlineKeyboardButton(
                        text=link[0],
                        url=link[1]
                    )
                )

            kb_builder.row(*buttons, width=1)

            return kb_builder.as_markup()