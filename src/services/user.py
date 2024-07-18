from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from models.user import User
from schemas.user import UserCreate, UserCreateDB
from utilies.security.password_hasher import get_password_hash


async def create(db: AsyncSession, create_data: UserCreate) -> User:
    create_data.password = get_password_hash(create_data.password)
    create_schema = UserCreateDB(**create_data.model_dump())
    return await crud_user.create(db=db, create_schema=create_schema)
