# Weather API

A FastAPI-based weather API that fetches and caches weather data from Visual Crossing's API.

## Features

- Weather data retrieval for any city
- Redis caching with 12-hour expiration
- Rate limiting (5 requests per minute)
- Support for metric and imperial units
- Error handling and proper response formatting
- CORS support

## Prerequisites

- Python 3.12+
- Redis server
- Visual Crossing API key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/codefromlani/Roadmap.sh-Projects.git
cd beginner
cd weather-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `.env` file:
   - Set your Visual Crossing API key
   - Configure Redis connection details if different from defaults

## Running the API

1. Make sure Redis is running

2. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

3. The API will be available at `http://localhost:8000`

## API Endpoints

### GET /weather/{city}

Get weather data for a specific city.

Query Parameters:
- `units` (optional): "metric" (default) or "imperial"

Example:
```bash
curl "http://localhost:8000/weather/london?units=metric"
```

Response format:
```json
{
  "city": "london",
  "current": {
    "temperature": 15.5,
    "humidity": 75,
    "wind_speed": 10.5,
    "conditions": "Partly cloudy",
    "datetime": "2024-02-20T14:30:00"
  },
  "forecast": [
    {
      "date": "2024-02-20",
      "max_temp": 18.5,
      "min_temp": 12.0,
      "conditions": "Partly cloudy"
    },
    // ... more days
  ]
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- 400: Invalid request
- 429: Rate limit exceeded
- 500: Internal server error
- 503: Weather service unavailable 