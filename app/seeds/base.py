from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete as sql_delete

from app.config.db import DBModel

T = TypeVar("T", bound=DBModel)

class Seeder(ABC, Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create_or_update(self, keyfield: str, **kwargs) -> T:
        model_field = getattr(self.model, keyfield)
        keyvalue = kwargs[keyfield]

        stmt = update(self.model).where(model_field == keyvalue).values(**kwargs)
        res = await self.session.execute(stmt)
        
        if res.rowcount == 0:
            model = self.model(**kwargs)
            self.session.add(model)
        
        await self.session.commit()

        return (await self.session.execute(select(self.model).where(model_field == keyvalue))).scalar_one()
    
    async def delete(self) -> None:
        await self.session.execute(sql_delete(self.model))
        await self.session.commit()

    @abstractmethod
    async def seed(self) -> None:
        pass

