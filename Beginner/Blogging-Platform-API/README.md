# Blogging Platform API

A RESTful API for a blogging platform built with FastAPI and MongoDB.

## Features

- Create, read, update, and delete blog posts
- Search/filter posts by term
- JSON responses with proper status codes
- MongoDB database for data persistence

## Requirements

- Python 3.12+
- MongoDB

## Installation

1. Clone the repository:
```bash
git clone https://github.com/codefromlani/Roadmap.sh-Projects.git
cd beginner
cd blogging-platform-api
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

4. Create a `.env` file in the project root with the following content:
```bash
MONGODB_URL=mongodb://localhost:27017
```

## Running the API

Start the server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Create a new blog post
- `POST /posts`

### Get all blog posts
- `GET /posts`
- `GET /posts?term=search_term` (with search filter)

### Get a specific blog post
- `GET /posts/{post_id}`

### Update a blog post
- `PUT /posts/{post_id}`

### Delete a blog post
- `DELETE /posts/{post_id}`