from sqlalchemy.ext.asyncio import AsyncSession

from crud.city import crud_city
from models import City, User
from schemas.city import CityCreate, CityCreateDB


async def create(
    db: AsyncSession, create_data: CityCreate, user: User
) -> City:
    try:
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
