from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson import ObjectId

class User(BaseModel):
    email: EmailStr
    password: str
    role: str  # "ops_user" or "client_user"
    verified: bool = False

class FileUpload(BaseModel):
    file_name: str
    file_type: str  # pptx, docx, xlsx
    uploaded_by: str  # User ID

class EncryptedLink(BaseModel):
    user_id: str
    file_id: str
    encrypted_url: str
