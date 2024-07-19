from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temp: str
    feels_like: str
    pressure: str
    rain: str
    snow: str
