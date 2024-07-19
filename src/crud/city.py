from typing import List, Optional

from sqlalchemy import and_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from models.city import City
from schemas.city import CityBase, CityCreateDB

from .async_crud import BaseAsyncCRUD


class CityCRUD(BaseAsyncCRUD[City, CityBase, CityCreateDB]):
    async def get_by_name(
        self, db: AsyncSession, obj_name: str
    ) -> Optional[City]:
        statement = select(self.model).where(self.model.name == obj_name)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_multi_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> Optional[List[City]]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.users))
            .where(self.model.users.any(id=user_id))
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()

    async def get_by_id_and_user_id(
        self, db: AsyncSession, obj_id: int, user_id: int
    ) -> Optional[City]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.users))
            .where(
                and_(
                    self.model.id == obj_id,
                    self.model.users.any(id=user_id),
                )
            )
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def create(
        self,
        db: AsyncSession,
        create_schema: CityCreateDB,
        commit: bool = True,
    ) -> City:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(self.model)
            .options(
                selectinload(self.model.users),
            )
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()


crud_city = CityCRUD(City)
