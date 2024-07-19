import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models import City, User


@pytest_asyncio.fixture
async def city_fixture(
    async_session: AsyncSession, user_fixture: User
) -> City:
    city = City(name="Москва", users=[user_fixture])
    async_session.add(city)
    await async_session.commit()
    await async_session.refresh(city)
    return city


@pytest_asyncio.fixture
async def another_city_fixture(
    async_session: AsyncSession, user_fixture: User
) -> City:
    city = City(name="Рига", users=[user_fixture])
    async_session.add(city)
    await async_session.commit()
    await async_session.refresh(city)
    return city
