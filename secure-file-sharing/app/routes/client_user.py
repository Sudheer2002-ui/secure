from fastapi import APIRouter, HTTPException, Depends
from app.utils.encryption import encrypt_url, decrypt_url
from app.models import EncryptedLink
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/sign-up")
async def sign_up(email: str, password: str):
    hashed_password = hash_password(password)
    user = {"email": email, "password": hashed_password, "role": "client_user", "verified": False}
    result = await db["users"].insert_one(user)
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

@router.get("/verify-email/{user_id}")
async def verify_email(user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"verified": True}})
    return {"message": "Email verified"}

@router.get("/list-files")
async def list_files(current_user=Depends(get_current_user)):
    files = await db["files"].find().to_list(100)
    return {"files": files}

@router.get("/download-file/{file_id}")
async def download_file(file_id: str, current_user=Depends(get_current_user)):
    file = await db["files"].find_one({"_id": ObjectId(file_id)})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    encrypted_url = encrypt_url(f"{current_user['user_id']}:{file_id}")
    link = {"user_id": current_user["user_id"], "file_id": file_id, "encrypted_url": encrypted_url}
    await db["links"].insert_one(link)
    return {"download-link": f"/secure-download/{encrypted_url}"}
