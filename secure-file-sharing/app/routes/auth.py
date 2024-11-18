from fastapi import APIRouter, HTTPException, Depends
from app.utils.auth import hash_password, verify_password, create_access_token
from app.models import User
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

router = APIRouter()

db = AsyncIOMotorClient("mongodb://localhost:27017")["file_sharing"]

@router.post("/login")
async def login(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(user["_id"]), "role": user["role"]})
    return {"token": token}
