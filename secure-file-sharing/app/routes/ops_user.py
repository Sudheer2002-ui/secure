from fastapi import APIRouter, Depends, UploadFile, HTTPException
from app.models import FileUpload
from app.utils.auth import get_current_user

router = APIRouter()

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}

@router.post("/upload-file")
async def upload_file(file: UploadFile, current_user=Depends(get_current_user)):
    if current_user["role"] != "ops_user":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if file.filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    file_record = {
        "file_name": file.filename,
        "file_type": file.filename.split(".")[-1],
        "uploaded_by": current_user["user_id"]
    }
    await db["files"].insert_one(file_record)
    return {"message": "File uploaded successfully"}
