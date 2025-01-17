from schemas.weather import WeatherResponse


async def generate_result(data: dict, city: str) -> WeatherResponse:
    weather_in_city = WeatherResponse(
        city=city,
        temp=str(data["list"][0]["main"]["temp"]),
        feels_like=str(data["list"][0]["main"]["feels_like"]),
        pressure=str((data["list"][0]["main"]["pressure"]) * 0.75),
        wind_speed=str((data["list"][0]["wind"]["speed"])),
        rain="No" if data["list"][0]["rain"] is None else "Yes",
        snow="No" if data["list"][0]["snow"] is None else "Yes",
    )
    return weather_in_city.model_dump()
