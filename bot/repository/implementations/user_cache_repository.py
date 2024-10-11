from datetime import timedelta
from typing import Optional, TypeAlias, Type

from pydantic import BaseModel
from typing_extensions import TypeVar

from core import dto
from core.enums import UserKeys
from repository.interfaces.redis_repository import RedisRepository

KeyType: TypeAlias = Optional[str]
ValueType: TypeAlias = Optional[str | bool | int]
ResponseModel = TypeVar('ResponseModel', bound=dto.UserBase, covariant=True)


class UserCacheRepository(RedisRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ex_time = 60 * 60 * 12


    async def hset(self, user_id: int, key: KeyType = None,
                   value: ValueType = None,
                   model_data: Optional[BaseModel] = None):
        user_key = UserKeys.USER_KEY.format(user_id)
        if model_data:
            set_data = {k: self._validate_value(v)
                        for k, v in model_data.model_dump().items()}
            await self.r.hset(name=user_key, mapping=set_data)
        else:
            if isinstance(value, bool):
                value = int(value)
            await self.r.hset(name=user_key, key=str(key), value=str(value))

        await self.r.expire(user_key, self.ex_time)

    async def hget(self, user_id: int, key: KeyType = None) -> ValueType:
        user_key = UserKeys.USER_KEY.format(user_id)

        user_bytes_value: Optional[bytes] = await self.r.hget(name=user_key, key=key)

        if not user_bytes_value:
            return
        user_value = user_bytes_value.decode('utf-8-sig')
        await self.r.expire(user_key, self.ex_time)
        return int(user_value) if user_value.isdigit() else user_value

    async def hget_all(self, user_id: int, response_model: Type[ResponseModel]) -> Optional[ResponseModel]:
        user_key = UserKeys.USER_KEY.format(user_id)

        user_bytes_data: Optional[dict[bytes, bytes]] = await self.r.hgetall(name=user_key)

        if not user_bytes_data:
            return

        mapping_values = {key.decode('utf-8-sig'): int(value.decode('utf-8-sig'))
        if value.isdigit() else value.decode('utf-8-sig')
                          for key, value in user_bytes_data.items()}
        await self.r.expire(user_key, self.ex_time)
        return response_model.model_validate(mapping_values, from_attributes=True)

    async def user_exists(self, user_id: int) -> bool:
        user_key = UserKeys.USER_KEY.format(user_id)
        return await self.r.exists(user_key)

    @staticmethod
    def _validate_value(value):
        if value is None:
            return ''
        if isinstance(value, bool):
            return '0' if not value else '1'
        return str(value)