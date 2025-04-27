from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
import os
import requests
from dotenv import load_dotenv
import json
from typing import Optional

load_dotenv()

VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = int(os.getenv("REDIS_DB", 0)),
CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 43200))


app = FastAPI(title="Weather API", 
              description="API to fetch weather data from Visual Crossing"
            )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_DB,
    decode_responses=True
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API. Use /weather/{city_code} to get weather data"}

@app.get("/weather/{city}")
@limiter.limit("5/minute")
async def get_weather(city: str, units: Optional[str] = "metric"):
    """
    Get weather data for a specific city.
    Rate limit: 5 requests per minute.
    """
    if not VISUAL_CROSSING_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Weather API key not configured"
        )
    
    cache_key = f"weather:{city}: {units}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)
    
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}"
        params = {
            "unitGroup": "metric" if units == "metric" else "us",
            "key": VISUAL_CROSSING_API_KEY,
            "contentType": "json"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        formatted_data = {
            "city": city,
            "current": {
                "temperature": weather_data["currentConditions"]["temp"],
                "humidity": weather_data["currentConditions"]["humidity"],
                "wind_speed": weather_data["currentConditions"]["windspeed"],
                "conditions": weather_data["currentConditions"]["conditions"],
                "datetime": weather_data["currentConditions"]["datetime"]
            },
            "forecast": [
                {
                    "date": day["datetime"],
                    "max_temp": day["tempmax"],
                    "min_temp": day["tempmin"],
                    "conditions": day["conditions"]
                }
                for day in weather_data["days"][:5] # Next 5 days forecast
            ]
        }

        redis_client.setex(
            cache_key,
            CACHE_EXPIRATION,
            json.dumps(formatted_data)
        )

        return formatted_data
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error fetching weather data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy"}