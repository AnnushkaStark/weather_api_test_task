from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.city import crud_city
from models import UsersCities


async def create_user_city(
    db: AsyncSession, city_id: int, user_id: int
) -> Optional[UsersCities]:
    if foud_city := await crud_city.get_by_id_and_user_id(  # noqa F841
        db=db, obj_id=city_id, user_id=user_id
    ):
        pass
    user_city = UsersCities(city_id=city_id, user_id=user_id)
    db.add(user_city)
    await db.commit()
    await db.refresh(user_city)
