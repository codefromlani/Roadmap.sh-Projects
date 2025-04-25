from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
import json
from typing import Optional

load_dotenv()


app = FastAPI(title="Weather API", 
              description="API to fetch weather data from Visual Crossing"
            )