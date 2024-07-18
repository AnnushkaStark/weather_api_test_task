from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.dependencies.auth import refresh_security
from api.dependencies.database import get_async_db
from crud.user import crud_user
from models.user import User
from schemas.token import TokenAccessRefresh
from schemas.user import UserCreate, UserLogin
from services import user as service_user
from utilies.security.password_hasher import  verify_password
from utilies.security.security import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    TokenSubject,
    access_security,
    create_tokens,
)

router = APIRouter()


@router.post(
    "/",
    summary="Create new user",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_async_db)
) -> User:
    existing_username = await crud_user.get_by_username(
        db, username=user.username
    )
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username alredy exist!",
        )
    existing_email = await crud_user.get_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="E-mail alredy exist!",
        )
    return await service_user.create(db=db, create_data=user)


@router.post("/login/", response_model=TokenAccessRefresh)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    if found_user := await crud_user.get_by_username(
        db, username=login_data.username
    ):
        if verify_password(
            plain_password=login_data.password,
            hashed_password=found_user.password,
        ):
            subject = TokenSubject(
                username=str(found_user.username), password=found_user.password
            )
            return await create_tokens(subject)
        raise HTTPException(status_code=401, detail="User password is wrong")
    raise HTTPException(
        status_code=404, detail=f"User {login_data.username} not found."
    )


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)


@router.delete("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response()
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    return response
