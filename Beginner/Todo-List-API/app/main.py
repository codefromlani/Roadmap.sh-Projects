from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.todos import router as todos_router
from app.db.database import Base, engine

app = FastAPI()

app.include_router(auth_router)
app.include_router(todos_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Todo List API"}
