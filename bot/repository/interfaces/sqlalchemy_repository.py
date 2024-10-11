from typing import Type, Union, Any, Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Query
from typing_extensions import TypeVar

from core.enums import LanguageList
from repository.interfaces.base import AbstractSQLRepository

ModelType = TypeVar('ModelType', bound=DeclarativeBase)
DTOModel = TypeVar('DTOModel', bound=BaseModel)

class SQLAlchemyRepository(AbstractSQLRepository):
    def __init__(self,
                 session: AsyncSession,
                 model: Type[ModelType],
                 dto_model: Type[DTOModel],
                 lookup_field: Union[str, int]):
        self._session = session
        self._model = model
        self._lookup_field = lookup_field
        self._dto_model = dto_model

    async def retrieve(self, lookup_value: Any,
                       response_model: Optional[Type[DTOModel]] = None,
                       raise_for_none = True,
                       instance_returned = False) -> DTOModel:
        lookup_field = getattr(self._model, self._lookup_field)
        if lookup_field is None:
            raise ValueError("Model does not have a lookup field")
        query = select(self._model).where(lookup_field == lookup_value)
        result = await self._session.execute(query)
        instance: ModelType | None = result.scalars().first()
        if instance is None and raise_for_none:
            raise NoResultFound(f"Instance with {lookup_field} == {lookup_value} not found")
        if instance is None:
            return None
        if instance_returned:
            return instance
        if response_model is None:
            return self._dto_model.model_validate(instance, from_attributes=True)
        return response_model.model_validate(instance, from_attributes=True)

    async def create(self, model_data: BaseModel,
                     response_model: Optional[Type[DTOModel]] = None) -> DTOModel:
        new_model = self._model(**model_data.model_dump())
        self._session.add(new_model)
        await self._session.commit()
        await self._session.refresh(new_model)

        if response_model is None:
            return self._dto_model.model_validate(new_model, from_attributes=True)
        return response_model.model_validate(new_model, from_attributes=True)

    async def update(self, lookup_value,
                     update_data: BaseModel,
                     response_model: Optional[Type[DTOModel]] = None) -> DTOModel:
        obj = await self.retrieve(lookup_value, instance_returned=True)
        update_dict = update_data.model_dump()
        for key, value in update_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                raise AttributeError(f"Model does not have attribute {key}")
        await self._session.commit()
        await self._session.refresh(obj)
        if response_model is None:
            return self._dto_model.model_validate(obj, from_attributes=True)
        return response_model.model_validate(obj, from_attributes=True)

    async def destroy(self, lookup_value) -> None:
        obj = await self.retrieve(lookup_value, instance_returned=True)
        await self._session.delete(obj)
        await self._session.commit()

    async def list(self,
                   filter_query: Optional[Query] = None,
                   response_model: Optional[Type[DTOModel]] = None) -> list[DTOModel]:
        if filter_query is None:
            result = await self._session.execute(select(self._model))
        else:
            result = await self._session.execute(filter_query)
        resp_model = self._dto_model if response_model is None else response_model
        return [resp_model.model_validate(obj, from_attributes=True)
                for obj in result.scalars().all()]
