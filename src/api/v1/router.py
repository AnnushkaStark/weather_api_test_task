from fastapi import APIRouter

from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.weather import router as weather_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(weather_router, prefix="/weather", tags=["Weather"])
