import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router as weather_api_router




app = FastAPI(
    title="WeatherAPI",
    openapi_url="/weather_api/openapi.json",
    docs_url="/weather_api/docs",
)


app.include_router(weather_api_router, prefix="/weather_api")
if __name__ == "__main__":
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
           
            reload=True,
            proxy_headers=True,
        )
       