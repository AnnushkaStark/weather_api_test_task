from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    ...


class CityCreateDB(CityBase):
    ...


class CityUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True


class CityResponse(CityBase):
    ...
