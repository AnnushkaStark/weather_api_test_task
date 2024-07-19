from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from crud.city import crud_city
from models.user import User
from schemas.user import UserCreate, UserCreateDB
from utilies.security.password_hasher import get_password_hash


async def create(db: AsyncSession, create_data: UserCreate) -> User:
    create_data.password = get_password_hash(create_data.password)
    create_schema = UserCreateDB(**create_data.model_dump())
    return await crud_user.create(db=db, create_schema=create_schema)


async def update_search_history(
        db: AsyncSession, db_obj: User, city_id: int, user_id: int
) -> User:
    if found_city := await crud_city.get_by_id_and_user_id(
        db=db, obj_id=city_id, user_id=user_id
    ):
        pass
    db_obj.responsed_cities.append(found_city)
    await db.commit()
