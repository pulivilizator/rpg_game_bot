import asyncio

import nats
from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import StreamConfig, StorageType, RetentionPolicy
from environs import Env

env = Env()
env.read_env()

async def migrate():
    nc: Client = await nats.connect(['nats://' + env.str("NATS_DSN")])
    js: JetStreamContext = nc.jetstream()

    payment_stream_config = StreamConfig(
        name='mailing_stream',
        subjects=['mailing'],
        storage=StorageType.FILE,
        retention=RetentionPolicy.WORK_QUEUE,
        allow_direct=True
    )
    resp = await js.add_stream(payment_stream_config)
    print(resp)


if __name__ == '__main__':
    asyncio.run(migrate())
