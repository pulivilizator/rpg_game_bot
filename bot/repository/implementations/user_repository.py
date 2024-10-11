from sqlalchemy import select, func

from repository.interfaces.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    async def get_users_count(self):
        query = select(func.count(self._model.user_id))
        result = await self._session.execute(query)
        return result.scalar_one()