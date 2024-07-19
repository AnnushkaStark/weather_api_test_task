from sqlalchemy.ext.asyncio import AsyncSession

from crud.city import crud_city
from crud.user import crud_user
from models import City
from schemas.city import CityCreate, CityCreateDB


async def create(
    db: AsyncSession, create_data: CityCreate, user_id: int
) -> City:
    try:
        user = await crud_user.get_by_id(db=db, obj_id=user_id)
        create_schema = CityCreateDB(
            **create_data.model_dump(exclude_unset=True)
        )
        city = await crud_city.create(
            db=db, create_schema=create_schema, commit=False
        )
        city.users.append(user)
        await db.commit()
        return city
    except Exception as ex:
        await db.rollback()
        raise ex
