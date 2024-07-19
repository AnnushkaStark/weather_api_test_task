from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.city import crud_city
from models.user import User
from schemas.city import CityCreate, CityResponse
from services import city as service_city
from services import users_city as users_city_service
from utilies.weather.get_weather import request_weather

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def get_weather_in_city(
    city: CityCreate,
    db: Session = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
) -> Optional[dict]:
    city.name = city.name.strip().title()
    if found_city := await crud_city.get_by_name(db=db, obj_name=city.name):
        await users_city_service.create_user_city(
            db=db, user_id=current_user.id, city_id=found_city.id
        )
        return await request_weather(city=found_city.name)
    weather = await request_weather(city=city.name)
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wrong city name"
        )
    await service_city.create(db=db, create_data=city, user_id=current_user.id)
    return weather


@router.get("/", response_model=List[CityResponse])
async def read_search_history(
    db: Session = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    found_cities = await crud_city.get_multi_by_user_id(
        db=db, user_id=current_user.id
    )
    return found_cities
