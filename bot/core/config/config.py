from pathlib import Path

from environs import Env
from pydantic import BaseModel, HttpUrl

from core.config.models import RedisConfig, BotConfig, Database, NatsConfig

BASE_DIR = Path(__file__).parent.parent.parent

class ConfigModel(BaseModel):
    redis: RedisConfig
    bot: BotConfig
    db: Database
    nats: NatsConfig

def get_config(path: str = None) -> ConfigModel:
    env = Env()
    env.read_env(path)

    return ConfigModel(
        redis=RedisConfig(
            dsn='redis://' + env.str('REDIS_STORAGE_DSN'),
        ),
        bot=BotConfig(
            token=env.str('BOT_TOKEN'),
            admins=env.list('ADMINS', delimiter=' '),
            subscribe_group_id=env.int('SUBSCRIBE_GROUP_ID')
        ),
        db=Database(
            dsn=env.str('POSTGRES_DSN')
        ),
        nats=NatsConfig(
            dsn='nats://' + env.str('NATS_DSN')
        )
    )