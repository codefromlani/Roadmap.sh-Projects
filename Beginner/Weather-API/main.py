from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import redis
import os
from dotenv import load_dotenv
import json
from typing import Optional

load_dotenv()

VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
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

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API. Use /weather/{city_code} to get weather data"}


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy"}