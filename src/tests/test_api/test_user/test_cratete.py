from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import crud_user
from models import User
from schemas.user import UserCreate

ROOT_ENDPOINT = "/weather_api/api/v1/users/"


class TestCreateUser:
    async def test_create(
        self, http_client: AsyncClient, async_session: AsyncSession
    ) -> None:
        data = UserCreate(
            username="Testuser",
            email="mytestmail@gmail.com",
            password="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 201
        await async_session.close()
        response_data = response.json()
        assert response_data["username"] == data.username
        created_user = await crud_user.get_by_email(
            db=async_session, email=data.email
        )
        assert created_user is not None
        assert created_user.username == data.username

    async def test_create_user_duplicate_username(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username=user_fixture.username,
            email="mytmail@mail.ru",
            password="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Username alredy exist!"
        not_created_user = await crud_user.get_by_email(
            db=async_session, email=data.email
        )
        assert not_created_user is None

    async def test_create_user_duplicate_email(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserCreate(
            username="MyUsername",
            email=user_fixture.email,
            password="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "E-mail alredy exist!"
        not_created_user = await crud_user.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None
