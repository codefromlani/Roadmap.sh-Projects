import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

print("MONGODB_URL:", os.getenv("MONGODB_URL"))


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.blog

posts_collection = db.get_collection("posts")