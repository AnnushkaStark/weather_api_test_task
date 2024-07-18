import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from models.user import User
from schemas.user import UserCreate
from utilies.security.password_hasher import get_password_hash


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    schema = UserCreate(
        username="testuser",
        email="mytestmail@mail.ru",
        password=get_password_hash("qwerty"),
    )
    user = await crud_user.create(db=async_session, create_schema=schema)
    return user
