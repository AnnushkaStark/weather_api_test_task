from httpx import AsyncClient as async_client
from weather_response import generate_result

from settings import WEATHER_API_KEY, WEATHER_URL


async def request_weather(city: str) -> str | None:
    url = (WEATHER_URL,)
    params = {
        "q": city,
        "type": "like",
        "units": "metric",
        "lang": "ru",
        "APPID": WEATHER_API_KEY,
    }
    result = await async_client.get(url=url, params=params)
    if result["count"] == 0:
        return None
    return await generate_result(data=result, city=city)
