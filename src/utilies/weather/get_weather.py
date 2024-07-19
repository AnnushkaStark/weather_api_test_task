from httpx import AsyncClient

from settings import WEATHER_API_KEY, WEATHER_URL

from .weather_response import generate_result

async_client = AsyncClient()


async def request_weather(city: str) -> str | None:
    url = WEATHER_URL
    params = {
        "q": city,
        "type": "like",
        "units": "metric",
        "lang": "ru",
        "APPID": WEATHER_API_KEY,
    }
    response = await async_client.get(url=url, params=params)
    response_data = response.json()
    if response_data["count"] == 0:
        return None
    return await generate_result(data=response_data, city=city)
