from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models import City, User

ROOT_ENDPOINT = "/weather_api/api/v1/weather/"


class TestSearchHistory:
    async def test_hisory_by_user_with_history(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        get_auth_headers: Callable,
        user_fixture: User,
        city_fixture: City,
        another_city_fixture: City,
    ) -> None:
        user_auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]["name"] == city_fixture.name
        assert response_data[1]["name"] == another_city_fixture.name

    async def test_get_history_by_user_without_history(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        get_auth_headers: Callable,
        user_wuthout_responsed_cities_fixture: User,
    ) -> None:
        user_auth_headers = await get_auth_headers(
            user_wuthout_responsed_cities_fixture
        )
        response = await http_client.get(
            ROOT_ENDPOINT, headers=user_auth_headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data == []
