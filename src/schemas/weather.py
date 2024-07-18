from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temp: int
    feels_like: str
    pressure: int
    rain: str
    snow: str
