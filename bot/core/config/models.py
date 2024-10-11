from pydantic import BaseModel, RedisDsn, PostgresDsn, NatsDsn


class RedisConfig(BaseModel):
    dsn: RedisDsn

class Database(BaseModel):
    dsn: PostgresDsn

class BotConfig(BaseModel):
    token: str
    admins: list[int]
    subscribe_group_id: int

class NatsConfig(BaseModel):
    dsn: NatsDsn