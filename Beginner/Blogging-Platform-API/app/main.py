from fastapi import FastAPI

from app.routes.post import router as posts_router

app = FastAPI(
    title="Personal Blog API",
    description="A RESTful API for a personal blogging platform",
    version="1.0.0"
)

app.include_router(posts_router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Personal Blog API"}